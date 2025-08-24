import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const GENERATED_DATA_DIR = path.join(process.cwd(), '..', 'agent', 'generated_data');

export async function GET(request: NextRequest) {
  try {
    // Check if generated_data directory exists
    if (!fs.existsSync(GENERATED_DATA_DIR)) {
      return NextResponse.json({ 
        error: 'No generated data directory found',
        latestFile: null,
        files: [] 
      }, { status: 404 });
    }

    // Get all voice-cards JSON files
    const files = fs.readdirSync(GENERATED_DATA_DIR)
      .filter(file => file.startsWith('voice-cards-') && file.endsWith('.json'))
      .map(file => {
        const filePath = path.join(GENERATED_DATA_DIR, file);
        const stats = fs.statSync(filePath);
        return {
          name: file,
          path: filePath,
          created: stats.birthtime,
          modified: stats.mtime,
          size: stats.size
        };
      })
      .sort((a, b) => b.modified.getTime() - a.modified.getTime());

    if (files.length === 0) {
      return NextResponse.json({ 
        error: 'No generated voice card files found',
        latestFile: null,
        files: [] 
      }, { status: 404 });
    }

    // Get the latest file
    const latestFile = files[0];
    
    // Check for specific file request
    const fileName = request.nextUrl.searchParams.get('file');
    
    if (fileName) {
      // Return specific file content
      const requestedFile = files.find(f => f.name === fileName);
      if (!requestedFile) {
        return NextResponse.json({ error: 'File not found' }, { status: 404 });
      }
      
      const content = fs.readFileSync(requestedFile.path, 'utf-8');
      return NextResponse.json(JSON.parse(content));
    }

    // Check if we should return the latest file content
    const getLatest = request.nextUrl.searchParams.get('latest');
    
    if (getLatest === 'true') {
      const content = fs.readFileSync(latestFile.path, 'utf-8');
      return NextResponse.json(JSON.parse(content));
    }

    // Return list of available files
    return NextResponse.json({
      latestFile: latestFile.name,
      files: files.map(f => ({
        name: f.name,
        created: f.created,
        modified: f.modified,
        size: f.size
      }))
    });

  } catch (error) {
    console.error('Error accessing generated data:', error);
    return NextResponse.json(
      { error: 'Failed to access generated data' },
      { status: 500 }
    );
  }
}

// Serve images from generated_data/images
export async function POST(request: NextRequest) {
  try {
    const { imagePath } = await request.json();
    
    if (!imagePath || !imagePath.startsWith('/generated_data/images/')) {
      return NextResponse.json({ error: 'Invalid image path' }, { status: 400 });
    }
    
    const fullPath = path.join(process.cwd(), '..', 'agent', imagePath.substring(1));
    
    if (!fs.existsSync(fullPath)) {
      return NextResponse.json({ error: 'Image not found' }, { status: 404 });
    }
    
    const imageBuffer = fs.readFileSync(fullPath);
    const base64Image = imageBuffer.toString('base64');
    
    return NextResponse.json({ 
      image: `data:image/png;base64,${base64Image}` 
    });
    
  } catch (error) {
    console.error('Error serving image:', error);
    return NextResponse.json(
      { error: 'Failed to serve image' },
      { status: 500 }
    );
  }
}