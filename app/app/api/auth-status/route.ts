import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  // Check for authentication cookie
  const authCookie = request.cookies.get('app-authenticated');
  
  const isAuthenticated = authCookie?.value === 'true';
  
  return NextResponse.json(
    { isAuthenticated },
    { status: 200 }
  );
}