'use client';

import {
  ControlBar,
  GridLayout,
  ParticipantTile,
  RoomAudioRenderer,
  useTracks,
  RoomContext,
} from '@livekit/components-react';
import { Room, Track } from 'livekit-client';
import '@livekit/components-styles';
import { useEffect, useState } from 'react';

interface RoomInfo {
  name: string;
  numParticipants: number;
  creationTime: string;
  metadata?: string;
}

export default function Page() {
  const [room, setRoom] = useState('quickstart-room-5');
  const [name, setName] = useState('quickstart-user-5');
  const [, setToken] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [activeRooms, setActiveRooms] = useState<RoomInfo[]>([]);
  const [isLoadingRooms, setIsLoadingRooms] = useState(false);
  const [roomInstance] = useState(() => new Room({
    // Optimize video quality for each participant's screen
    adaptiveStream: true,
    // Enable automatic audio/video quality optimization
    dynacast: true,
  }));

  const connectToRoom = async (roomName: string, userName: string) => {
    if (isConnecting) return;
    
    setIsConnecting(true);
    try {
      console.log('getting token', roomName, userName);
      const resp = await fetch(`/api/token?room=${roomName}&username=${userName}`);
      const data = await resp.json();
      
      if (data.token) {
        setToken(data.token);
        await roomInstance.connect(process.env.NEXT_PUBLIC_LIVEKIT_URL!, data.token);
        setIsConnected(true);
      } else {
        console.error('Failed to get token:', data.error);
      }
    } catch (e) {
      console.error('Connection error:', e);
    } finally {
      setIsConnecting(false);
    }
  };

  const disconnectFromRoom = async () => {
    try {
      await roomInstance.disconnect();
      setToken('');
      setIsConnected(false);
      console.log('Disconnected from room');
    } catch (e) {
      console.error('Disconnect error:', e);
    }
  };

  const clearSession = async () => {
    await disconnectFromRoom();
    
    // Call server-side cleanup endpoint
    try {
      const response = await fetch(`/api/token?room=${room}&username=${name}`, {
        method: 'DELETE',
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('Server cleanup successful:', result);
        
        if (result.participantsDisconnected > 0) {
          console.log(`Disconnected ${result.participantsDisconnected} participants from room ${result.room}`);
        }
      } else {
        console.error('Server cleanup failed:', response.status, response.statusText);
      }
    } catch (e) {
      console.error('Server cleanup call failed:', e);
    }
    
    // Clear any stored session data
    localStorage.removeItem('livekit-session');
    sessionStorage.clear();
    
    // Clear any LiveKit-specific storage
    Object.keys(localStorage).forEach(key => {
      if (key.includes('livekit') || key.includes('room')) {
        localStorage.removeItem(key);
      }
    });
    
    // Force page reload to clear any cached state
    window.location.reload();
  };

  const loadActiveRooms = async () => {
    setIsLoadingRooms(true);
    try {
      console.log('Fetching active rooms...');
      const response = await fetch('/api/token', {
        method: 'POST',
      });
      
      console.log('Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Response data:', data);
        setActiveRooms(data.rooms || []);
        console.log(`Loaded ${data.rooms?.length || 0} active rooms`);
      } else {
        const errorData = await response.json().catch(() => ({}));
        console.error('Failed to load rooms:', response.status, errorData);
        alert(`Failed to load rooms: ${errorData.error || 'Unknown error'}`);
      }
    } catch (e) {
      console.error('Error loading rooms:', e);
      alert('Error loading rooms. Please check the console for details.');
    } finally {
      setIsLoadingRooms(false);
    }
  };

  const deleteRoom = async (roomName: string) => {
    if (!confirm(`Are you sure you want to delete room "${roomName}"? This will disconnect all participants.`)) {
      return;
    }

    try {
      const response = await fetch(`/api/token?room=${roomName}`, {
        method: 'DELETE',
      });
      
      const result = await response.json();
      
      if (response.ok) {
        console.log('Room deleted:', result);
        
        // Show success message
        alert(`Room "${roomName}" ${result.message}`);
        
        // Refresh the room list
        await loadActiveRooms();
        
        // If we're currently in the deleted room, disconnect
        if (isConnected && room === roomName) {
          await disconnectFromRoom();
        }
      } else {
        console.error('Failed to delete room:', response.status, result);
        alert(`Failed to delete room: ${result.error || 'Unknown error'}`);
      }
    } catch (e) {
      console.error('Error deleting room:', e);
      alert('Error deleting room. Please try again.');
    }
  };

  useEffect(() => {
    let mounted = true;
    
    // Set up room event listeners
    const handleDisconnect = () => {
      if (mounted) {
        setIsConnected(false);
        setToken('');
        console.log('Room disconnected');
      }
    };

    const handleConnect = () => {
      if (mounted) {
        setIsConnected(true);
        console.log('Room connected');
      }
    };

    roomInstance.on('disconnected', handleDisconnect);
    roomInstance.on('connected', handleConnect);

    return () => {
      mounted = false;
      roomInstance.off('disconnected', handleDisconnect);
      roomInstance.off('connected', handleConnect);
      roomInstance.disconnect();
    };
  }, [roomInstance]);

  if (!isConnected) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
                <p className="text-gray-600 mt-2">Manage LiveKit rooms and vocabulary content</p>
              </div>
              <a
                href="/admin/lexical"
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200 shadow-md hover:shadow-lg"
              >
                Manage Lexical Items
              </a>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">5</div>
                <div className="text-sm text-gray-600">Active Lexical Items</div>
              </div>
            </div>
            <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{activeRooms.length}</div>
                <div className="text-sm text-gray-600">Active Rooms</div>
              </div>
            </div>
            <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {activeRooms.reduce((sum, room) => sum + room.numParticipants, 0)}
                </div>
                <div className="text-sm text-gray-600">Total Participants</div>
              </div>
            </div>
          </div>

          {/* Active Rooms Section */}
          <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">LiveKit Room Management</h2>
              <button
                onClick={loadActiveRooms}
                disabled={isLoadingRooms}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                  isLoadingRooms
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-green-600 hover:bg-green-700 text-white shadow-md hover:shadow-lg'
                }`}
              >
                {isLoadingRooms ? 'Loading...' : 'Refresh Rooms'}
              </button>
            </div>

            {activeRooms.length === 0 ? (
              <div className="text-center py-8">
                <div className="text-gray-400 mb-2">
                  <svg className="w-12 h-12 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                </div>
                <p className="text-gray-500 italic">
                  {isLoadingRooms ? 'Loading rooms...' : 'No active rooms found'}
                </p>
              </div>
            ) : (
              <div className="grid gap-4">
                {activeRooms.map((roomInfo) => (
                  <div
                    key={roomInfo.name}
                    className="border border-gray-200 rounded-lg p-4 bg-gray-50 hover:bg-gray-100 transition-colors duration-200"
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900 text-lg">{roomInfo.name}</h3>
                        <div className="text-sm text-gray-600 mt-1 flex flex-wrap gap-4">
                          <span className="flex items-center">
                            <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                              <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM9 7a1 1 0 11-2 0 1 1 0 012 0zM7 14a3 3 0 00-3 3v2a1 1 0 001 1h6a1 1 0 001-1v-2a3 3 0 00-3-3H7zM13 10a2 2 0 11-4 0 2 2 0 014 0zM19 10a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                            {roomInfo.numParticipants} participants
                          </span>
                          {roomInfo.creationTime && (
                            <span className="flex items-center">
                              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                              </svg>
                              Created: {new Date(roomInfo.creationTime).toLocaleString()}
                            </span>
                          )}
                        </div>
                      </div>
                      <button
                        onClick={() => deleteRoom(roomInfo.name)}
                        className="ml-4 px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-medium rounded-lg transition-colors duration-200 shadow-md hover:shadow-lg"
                      >
                        Delete Room
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          {/* Connect to Room Section */}
          <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Connect to Room</h2>
            
            <div className="grid md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Room Name
                </label>
                <input
                  type="text"
                  value={room}
                  onChange={(e) => setRoom(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200"
                  placeholder="Enter room name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Username
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200"
                  placeholder="Enter username"
                />
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 mb-6">
              <button
                onClick={() => connectToRoom(room, name)}
                disabled={isConnecting || !room.trim() || !name.trim()}
                className={`flex-1 px-6 py-3 rounded-lg font-semibold transition-all duration-200 shadow-md hover:shadow-lg ${
                  isConnecting || !room.trim() || !name.trim()
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700 text-white'
                }`}
              >
                {isConnecting ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Connecting...
                  </span>
                ) : (
                  'Connect to Room'
                )}
              </button>

              <button
                onClick={clearSession}
                className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition-all duration-200 shadow-md hover:shadow-lg"
              >
                Clear Session
              </button>
            </div>

            {isConnecting && (
              <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-blue-400 animate-pulse" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm text-blue-700">
                      Connecting to room... Please wait while we establish the connection.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <RoomContext.Provider value={roomInstance}>
      <div data-lk-theme="default" className="h-screen bg-gray-900">
        {/* Header with disconnect button */}
        <div className="absolute top-4 right-4 z-50 flex gap-3">
          <button
            onClick={disconnectFromRoom}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-medium rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl backdrop-blur-sm bg-opacity-90"
          >
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 6.707 6.293a1 1 0 00-1.414 1.414L8.586 11l-3.293 3.293a1 1 0 001.414 1.414L10 12.414l3.293 3.293a1 1 0 001.414-1.414L11.414 11l3.293-3.293z" clipRule="evenodd" />
              </svg>
              Disconnect
            </span>
          </button>
          <button
            onClick={clearSession}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white text-sm font-medium rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl backdrop-blur-sm bg-opacity-90"
          >
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
              </svg>
              Clear Session
            </span>
          </button>
        </div>

        {/* Your custom component with basic video conferencing functionality. */}
        <MyVideoConference />
        {/* The RoomAudioRenderer takes care of room-wide audio for you. */}
        <RoomAudioRenderer />
        {/* Controls for the user to start/stop audio, video, and screen share tracks */}
        <ControlBar />
      </div>
    </RoomContext.Provider>
  );
}

function MyVideoConference() {
  // `useTracks` returns all camera and screen share tracks. If a user
  // joins without a published camera track, a placeholder track is returned.
  const tracks = useTracks(
    [
      { source: Track.Source.Camera, withPlaceholder: true },
      { source: Track.Source.ScreenShare, withPlaceholder: false },
    ],
    { onlySubscribed: false },
  );
  return (
    <GridLayout tracks={tracks} style={{ height: 'calc(100vh - var(--lk-control-bar-height))' }}>
      {/* The GridLayout accepts zero or one child. The child is used
      as a template to render all passed in tracks. */}
      <ParticipantTile />
    </GridLayout>
  );
}