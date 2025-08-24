'use client';

import { useState, useEffect } from 'react';
import Hero from '@/components/Hero';
import AboutUs from '@/components/AboutUs';

export default function HomePage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check authentication status using dedicated auth status endpoint
    fetch('/api/auth-status', { 
      method: 'GET',
      credentials: 'include' 
    })
    .then(response => response.json())
    .then(data => {
      setIsAuthenticated(data.isAuthenticated);
    })
    .catch(() => {
      setIsAuthenticated(false);
    })
    .finally(() => {
      setIsLoading(false);
    });
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-background via-study-bg to-primary/5 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4 mx-auto"></div>
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  const handleSignOut = () => {
    setIsAuthenticated(false);
  };

  return (
    <>
      <Hero isAuthenticated={isAuthenticated} onSignOut={handleSignOut} />
      <AboutUs />
    </>
  );
}