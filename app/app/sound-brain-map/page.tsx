'use client';

import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { SoundBrainMapWrapper } from '@/components/SoundBrainMap';

export default function SoundBrainMapPage() {
  return (
    <div className="fixed inset-0 w-full h-full">
      {/* Minimal Navigation - Only Back Button */}
      <div className="absolute top-4 left-4 z-10">
        <Link href="/">
          <Button variant="ghost" className="flex items-center gap-2 text-white/80 hover:text-white hover:bg-black/20 backdrop-blur-sm">
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Button>
        </Link>
      </div>

      {/* Full-Screen Sound Brain Map */}
      <SoundBrainMapWrapper className="w-full h-full" />
    </div>
  );
}