'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BookOpen, MessageSquare, Target, Users } from "lucide-react";

const AboutUs = () => {
  return (
    <section className="py-16 bg-gradient-to-b from-background to-study-bg/50">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-foreground mb-4">About Phrasal Verbs</h2>
            <p className="text-xl text-muted-foreground">
              Understanding the building blocks of fluent English conversation
            </p>
          </div>

          {/* What are Phrasal Verbs */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-primary" />
                What Are Phrasal Verbs?
              </CardTitle>
            </CardHeader>
            <CardContent className="prose prose-gray max-w-none">
              <p className="text-muted-foreground leading-relaxed mb-4">
                Phrasal verbs are combinations of verbs with prepositions or adverbs that create entirely new meanings. 
                For example, &quot;get up&quot; means to rise from bed, while &quot;get along with&quot; means to have a good relationship. 
                These combinations are essential for natural English communication but can be challenging because their 
                meanings often can&#39;t be guessed from the individual words.
              </p>
              <p className="text-muted-foreground leading-relaxed">
                Native English speakers use phrasal verbs constantly in everyday conversation. Mastering them is the 
                difference between textbook English and speaking like a native. They make your speech more natural, 
                expressive, and authentic.
              </p>
            </CardContent>
          </Card>

          {/* Why They Matter */}
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <MessageSquare className="w-5 h-5 text-primary" />
                  Essential for Conversation
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Over 80% of everyday English conversations include phrasal verbs. Without them, 
                  your English might be grammatically correct but sound unnatural or overly formal.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Target className="w-5 h-5 text-success" />
                  Multiple Meanings
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  A single phrasal verb can have multiple meanings depending on context. &quot;Break down&quot; 
                  can mean to stop working, to cry, or to analyze something into parts.
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Examples */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Common Examples You Use Every Day</CardTitle>
              <CardDescription>These phrasal verbs appear in almost every English conversation</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-3">
                  <div className="p-3 bg-primary/5 rounded-lg">
                    <strong className="text-primary">Look up</strong>
                    <p className="text-sm text-muted-foreground mt-1">Search for information</p>
                    <p className="text-xs italic mt-1">&quot;I&#39;ll look up the answer online&quot;</p>
                  </div>
                  <div className="p-3 bg-primary/5 rounded-lg">
                    <strong className="text-primary">Put off</strong>
                    <p className="text-sm text-muted-foreground mt-1">Postpone or delay</p>
                    <p className="text-xs italic mt-1">&quot;Don&#39;t put off your homework&quot;</p>
                  </div>
                  <div className="p-3 bg-primary/5 rounded-lg">
                    <strong className="text-primary">Figure out</strong>
                    <p className="text-sm text-muted-foreground mt-1">Understand or solve</p>
                    <p className="text-xs italic mt-1">&quot;I can&#39;t figure out this problem&quot;</p>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="p-3 bg-primary/5 rounded-lg">
                    <strong className="text-primary">Give up</strong>
                    <p className="text-sm text-muted-foreground mt-1">Stop trying</p>
                    <p className="text-xs italic mt-1">&quot;Never give up on your dreams&quot;</p>
                  </div>
                  <div className="p-3 bg-primary/5 rounded-lg">
                    <strong className="text-primary">Turn down</strong>
                    <p className="text-sm text-muted-foreground mt-1">Reject or reduce</p>
                    <p className="text-xs italic mt-1">&quot;Please turn down the music&quot;</p>
                  </div>
                  <div className="p-3 bg-primary/5 rounded-lg">
                    <strong className="text-primary">Run into</strong>
                    <p className="text-sm text-muted-foreground mt-1">Meet unexpectedly</p>
                    <p className="text-xs italic mt-1">&quot;I ran into an old friend today&quot;</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Why VocabAi.CC */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-5 h-5 text-primary" />
                Why Learn with VocabAi.CC?
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground leading-relaxed mb-4">
                Traditional methods of learning phrasal verbs through lists and memorization don&#39;t work because 
                they lack context and practice. VocabAi.CC uses AI-powered conversation practice to help you 
                learn phrasal verbs the way native speakers do - through actual usage.
              </p>
              <ul className="space-y-2 text-muted-foreground">
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  <span>Practice explaining meanings in your own words to AI tutors</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  <span>Get instant feedback on your pronunciation and usage</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  <span>Learn multiple meanings of each phrasal verb with real examples</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  <span>Track your progress with spaced repetition for long-term retention</span>
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default AboutUs;