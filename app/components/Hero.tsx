'use client';

import { Button } from "@/components/ui/button";
import { BookOpen, Brain, Trophy, Zap, LogOut } from "lucide-react";
import { useRouter } from "next/navigation";

const Hero = ({ isAuthenticated, onSignOut }: { isAuthenticated: boolean; onSignOut: () => void }) => {
  const router = useRouter();

  const handleSignOut = async () => {
    try {
      const response = await fetch('/api/auth', {
        method: 'DELETE',
        credentials: 'include'
      });

      if (response.ok) {
        onSignOut();
      }
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-study-bg to-primary/5">
      <div className="container mx-auto px-4 py-16">
        {/* Navigation */}
        <nav className="flex items-center justify-between mb-16">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-primary to-primary-glow rounded-lg flex items-center justify-center">
              <Brain className="w-5 h-5 text-primary-foreground" />
            </div>
            <h1 className="text-xl font-bold text-foreground">VocabAi.CC</h1>
          </div>
          <div className="flex gap-3">
            {isAuthenticated ? (
              <>
                <div className="flex items-center gap-2 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                  <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                  Signed In
                </div>
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => router.push('/dashboard')}
                >
                  Dashboard
                </Button>
                <Button 
                  variant="default" 
                  size="sm"
                  onClick={() => router.push('/study')}
                >
                  Start Session
                </Button>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={handleSignOut}
                  className="text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                  <LogOut className="w-4 h-4 mr-1" />
                  Sign Out
                </Button>
              </>
            ) : (
              <>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => router.push('/login')}
                >
                  Sign In
                </Button>
                <Button 
                  variant="default" 
                  size="sm"
                  onClick={() => router.push('/login')}
                >
                  Get Started
                </Button>
              </>
            )}
          </div>
        </nav>

        {/* Hero Content */}
        <div className="max-w-4xl mx-auto text-center">
          <div className="mb-8">
            <h1 className="text-5xl md:text-6xl font-bold text-foreground mb-6 leading-tight">
              Master <span className="text-primary">Vocab</span>
              <span className="block">Like Never Before</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto leading-relaxed">
              Master phrasal verbs for <span className="text-primary font-semibold">speaking</span> - this vocabulary will 
              skyrocket your spoken English understanding. Learn multiple meanings, get assessed on your 
              pronunciation, and conquer the trickiest part of English fluency.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <Button 
              variant="default" 
              size="lg" 
              className="text-lg px-8 py-6"
              onClick={() => router.push(isAuthenticated ? '/study' : '/login')}
            >
              <BookOpen className="w-5 h-5 mr-2" />
              {isAuthenticated ? 'Start Learning' : 'Sign In to Start'}
            </Button>
            <Button 
              variant="outline" 
              size="lg" 
              className="text-lg px-8 py-6"
              onClick={() => router.push(isAuthenticated ? '/dashboard' : '/login')}
            >
              <Zap className="w-5 h-5 mr-2" />
              {isAuthenticated ? 'View Dashboard' : 'Sign In for Demo'}
            </Button>
          </div>

          {/* Feature Cards */}
          <div className="grid md:grid-cols-3 gap-6 mb-16">
            <div className="bg-card rounded-xl p-6 shadow-lg border border-border hover:shadow-xl transition-shadow duration-300">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <Brain className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Smart Repetition</h3>
              <p className="text-muted-foreground">
                Advanced algorithm adapts to your learning pace and remembers what you struggle with
              </p>
            </div>

            <div className="bg-card rounded-xl p-6 shadow-lg border border-border hover:shadow-xl transition-shadow duration-300">
              <div className="w-12 h-12 bg-success/10 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <BookOpen className="w-6 h-6 text-success" />
              </div>
              <h3 className="text-lg font-semibold mb-2">AI Tutors & Pronunciation</h3>
              <p className="text-muted-foreground">
                Practice using phrasal verbs in context with AI tutors and get real-time pronunciation evaluation
              </p>
            </div>

            <div className="bg-card rounded-xl p-6 shadow-lg border border-border hover:shadow-xl transition-shadow duration-300">
              <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <Trophy className="w-6 h-6 text-accent" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Track Progress</h3>
              <p className="text-muted-foreground">
                Visual progress tracking and achievement system keeps you motivated
              </p>
            </div>
          </div>

          {/* Stats */}
          <div className="bg-card/50 backdrop-blur-sm rounded-2xl p-8 border border-border">
            <div className="grid grid-cols-3 gap-8 text-center">
              <div>
                <div className="text-3xl font-bold text-primary mb-1">500+</div>
                <div className="text-sm text-muted-foreground">Phrasal Verbs</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-success mb-1">10k+</div>
                <div className="text-sm text-muted-foreground">Learners</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-accent mb-1">95%</div>
                <div className="text-sm text-muted-foreground">Success Rate</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;