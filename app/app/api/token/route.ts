import { NextRequest, NextResponse } from 'next/server';
import { AccessToken, RoomServiceClient } from 'livekit-server-sdk';

// Do not cache endpoint result
export const revalidate = 0;

// Initialize RoomServiceClient for server-side operations
const getRoomServiceClient = () => {
  const apiKey = process.env.LIVEKIT_API_KEY;
  const apiSecret = process.env.LIVEKIT_API_SECRET;
  const wsUrl = process.env.LIVEKIT_URL;

  if (!apiKey || !apiSecret || !wsUrl) {
    throw new Error('LiveKit configuration missing');
  }

  console.log('LiveKit config:', {
    apiKey: apiKey ? '***' : 'missing',
    apiSecret: apiSecret ? '***' : 'missing',
    wsUrl: wsUrl
  });

  // Extract host from wsUrl (remove ws:// or wss:// prefix)
  const host = wsUrl.replace(/^wss?:\/\//, '');
  const httpUrl = `https://${host}`;
  
  console.log('Constructed HTTP URL for RoomServiceClient:', httpUrl);
  
  return new RoomServiceClient(httpUrl, apiKey, apiSecret);
};

export async function GET(req: NextRequest) {
  const room = req.nextUrl.searchParams.get('room');
  const username = req.nextUrl.searchParams.get('username');
  const voiceCardData = req.nextUrl.searchParams.get('voiceCardData');
  
  if (!room) {
    return NextResponse.json({ error: 'Missing "room" query parameter' }, { status: 400 });
  } else if (!username) {
    return NextResponse.json({ error: 'Missing "username" query parameter' }, { status: 400 });
  }

  const apiKey = process.env.LIVEKIT_API_KEY;
  const apiSecret = process.env.LIVEKIT_API_SECRET;
  const wsUrl = process.env.LIVEKIT_URL;

  if (!apiKey || !apiSecret || !wsUrl) {
    return NextResponse.json({ error: 'Server misconfigured' }, { status: 500 });
  }

  try {
    // Parse voice card data if provided
    let parsedVoiceCardData = null;
    if (voiceCardData) {
      try {
        parsedVoiceCardData = JSON.parse(decodeURIComponent(voiceCardData));
        console.log(`Voice card data received for token: ${parsedVoiceCardData.title}`);
      } catch (e) {
        console.error('Failed to parse voice card data:', e);
        return NextResponse.json({ error: 'Invalid voice card data format' }, { status: 400 });
      }
    }

    const at = new AccessToken(apiKey, apiSecret, { 
      identity: username,
      // Add voice card data as metadata in the token
      metadata: parsedVoiceCardData ? JSON.stringify(parsedVoiceCardData) : undefined
    });
    
    at.addGrant({ 
      room, 
      roomJoin: true, 
      canPublish: true, 
      canSubscribe: true
    });

    const token = await at.toJwt();
    
    console.log(`Token generated for room: ${room}, user: ${username}${parsedVoiceCardData ? `, voice card: ${parsedVoiceCardData.title}` : ''}`);
    
    return NextResponse.json(
      { token },
      { 
        headers: { 
          "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate",
          "Pragma": "no-cache",
          "Expires": "0"
        } 
      },
    );
  } catch (error) {
    console.error('Error generating token:', error);
    return NextResponse.json({ error: 'Failed to generate token' }, { status: 500 });
  }
}

// List all rooms
export async function POST() {
  try {
    console.log('Attempting to list rooms...');
    
    const roomServiceClient = getRoomServiceClient();
    console.log('RoomServiceClient created successfully');
    
    const rooms = await roomServiceClient.listRooms();
    console.log(`Found ${rooms.length} active rooms:`, rooms.map(r => ({ name: r.name, participants: r.numParticipants })));
    
    return NextResponse.json(
      { 
        rooms: rooms.map(room => ({
          name: room.name,
          numParticipants: Number(room.numParticipants), // Convert BigInt to number
          creationTime: room.creationTime ? new Date(Number(room.creationTime)).toISOString() : undefined, // Convert BigInt timestamp to ISO string
          metadata: room.metadata
        }))
      },
      { 
        headers: { 
          "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate",
          "Pragma": "no-cache",
          "Expires": "0"
        } 
      }
    );
  } catch (error) {
    console.error('Error listing rooms:', error);
    console.error('Error details:', {
      message: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined,
      name: error instanceof Error ? error.name : undefined
    });
    
    return NextResponse.json(
      { 
        error: 'Failed to list rooms',
        details: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      }, 
      { status: 500 }
    );
  }
}

// Delete a room (disconnects all participants)
export async function DELETE(req: NextRequest) {
  const room = req.nextUrl.searchParams.get('room');
  const username = req.nextUrl.searchParams.get('username');
  
  if (!room) {
    return NextResponse.json({ error: 'Missing "room" query parameter' }, { status: 400 });
  }
  
  console.log(`Room deletion requested for room: ${room}, user: ${username}`);
  
  try {
    const roomServiceClient = getRoomServiceClient();
    
    // Try to delete the room directly - if it doesn't exist, the API will return an error
    try {
      await roomServiceClient.deleteRoom(room);
      console.log(`Room ${room} successfully deleted`);
      
      return NextResponse.json(
        { 
          message: 'Room deleted successfully', 
          room: room,
          participantsDisconnected: 'unknown' // We don't know the count since we deleted directly
        },
        { 
          headers: { 
            "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
          } 
        }
      );
    } catch (deleteError: unknown) {
      // Check if the error is because the room doesn't exist
      const error = deleteError as { status?: number; code?: string; message?: string };
      if (error.status === 404 || error.code === 'not_found' || 
          error.message?.includes('does not exist') || 
          error.message?.includes('not found')) {
        console.log(`Room ${room} not found or already deleted`);
        return NextResponse.json(
          { 
            message: 'Room not found or already deleted', 
            room: room 
          },
          { 
            headers: { 
              "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate",
              "Pragma": "no-cache",
              "Expires": "0"
            } 
          }
        );
      } else {
        // Re-throw other errors
        throw deleteError;
      }
    }
  } catch (error) {
    console.error('Error during room deletion:', error);
    return NextResponse.json(
      { 
        error: 'Failed to delete room',
        details: error instanceof Error ? error.message : 'Unknown error'
      }, 
      { status: 500 }
    );
  }
}