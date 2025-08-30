'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Code2, Globe, Rocket, Users } from "lucide-react";

const AboutUs = () => {
  return (
    <section className="py-16 bg-gradient-to-b from-background to-study-bg/50">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-foreground mb-4">The Recipe for Speaking Success</h2>
            <p className="text-xl text-muted-foreground">
              Master vocabulary in situations that matter to your developer career
            </p>
          </div>

          {/* What are Phrasal Verbs */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Code2 className="w-5 h-5 text-primary" />
                Developer Communication Patterns
              </CardTitle>
            </CardHeader>
            <CardContent className="prose prose-gray max-w-none">
              <p className="text-muted-foreground leading-relaxed mb-4">
                Success as a developer isn&apos;t just about coding skills. The ability to communicate clearly in 
                standups, code reviews, technical interviews, and cross-team collaborations directly impacts your 
                career trajectory. Studies show that developers with strong communication skills earn 30-50% more 
                than their technically equivalent peers.
              </p>
              <p className="text-muted-foreground leading-relaxed">
                VoiceCard focuses on the specific vocabulary and communication patterns that developers need: 
                explaining technical concepts, pushing back on unrealistic deadlines, advocating for best practices, 
                and presenting your ideas with confidence. We turn your technical knowledge into articulate communication.
              </p>
            </CardContent>
          </Card>

          {/* Why They Matter */}
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Globe className="w-5 h-5 text-primary" />
                  Practice with Global Developers
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Practice with AI tutors trained on voices from India, Brazil, Eastern Europe, and beyond. 
                  Master different accents and communication styles through realistic voice interactions that 
                  prepare you for international team collaboration.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Rocket className="w-5 h-5 text-success" />
                  Master Technical Jargon
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Learn how to use technical terms naturally in context. Bridge the gap between knowing 
                  what &quot;microservices&quot; are and confidently discussing their trade-offs in a system design interview.
                </p>
              </CardContent>
            </Card>
          </div>


          {/* Why VocabAi.CC */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-5 h-5 text-primary" />
                About VoiceCard
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground leading-relaxed mb-4">
                VoiceCard is built by developers, for developers. We understand that your time is valuable and your 
                career goals are specific. That&apos;s why we focus exclusively on the communication skills that directly 
                impact your professional growth: from acing technical interviews to leading architecture discussions.
              </p>
              <ul className="space-y-2 text-muted-foreground">
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  <span>Practice real developer scenarios: standups, PR reviews, incident post-mortems</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  <span>Get instant feedback on technical explanations and presentation skills</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  <span>Track your progress toward salary goals with measurable improvements</span>
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