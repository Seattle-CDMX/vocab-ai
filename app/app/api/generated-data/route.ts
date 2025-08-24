import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

// Try multiple paths for different deployment environments
const GENERATED_DATA_PATHS = [
  path.join(process.cwd(), '..', 'agent', 'generated_data'), // Local development (monorepo)
  path.join(process.cwd(), 'generated_data'), // Vercel deployment (copied to app dir)
];

const GENERATED_DATA_DIR = GENERATED_DATA_PATHS.find(dir => fs.existsSync(dir)) || GENERATED_DATA_PATHS[0];

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

    // Check for the main voice cards file
    const mainFilePath = path.join(GENERATED_DATA_DIR, 'voice-cards.json');
    
    if (!fs.existsSync(mainFilePath)) {
      return NextResponse.json({ 
        error: 'Voice cards file not found. Run the demo generator to create voice-cards.json',
        latestFile: null,
        files: [] 
      }, { status: 404 });
    }

    // Get the main file stats
    const stats = fs.statSync(mainFilePath);
    const mainFile = {
      name: 'voice-cards.json',
      path: mainFilePath,
      created: stats.birthtime,
      modified: stats.mtime,
      size: stats.size
    };
    
    // Check for specific file request
    const fileName = request.nextUrl.searchParams.get('file');
    
    if (fileName && fileName === 'voice-cards.json') {
      const content = fs.readFileSync(mainFilePath, 'utf-8');
      return NextResponse.json(JSON.parse(content));
    }

    // Check if we should return the latest file content
    const getLatest = request.nextUrl.searchParams.get('latest');
    
    if (getLatest === 'true') {
      const content = fs.readFileSync(mainFilePath, 'utf-8');
      return NextResponse.json(JSON.parse(content));
    }

    // Return file info
    return NextResponse.json({
      latestFile: mainFile.name,
      files: [mainFile]
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
    
    // Try multiple paths for image serving
    const imagePaths = [
      path.join(process.cwd(), '..', 'agent', imagePath.substring(1)), // Local development
      path.join(process.cwd(), imagePath.substring(1)), // Vercel deployment
    ];
    
    const fullPath = imagePaths.find(imgPath => fs.existsSync(imgPath)) || imagePaths[0];
    
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