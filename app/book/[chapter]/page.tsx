import fs from 'fs';
import path from 'path';
import Link from 'next/link';
import { notFound } from 'next/navigation';

// Define the available chapters
const chapters = [
  { id: 'introduction', title: 'Introduction' },
  { id: 'chapter-1-sound-brain-map-ipa', title: 'Chapter 1: The Sound Brain Map and the IPA' },
  { id: 'chapter-2-schwa-front-vowels', title: 'Chapter 2: Schwa and Front Vowels' },
  { id: 'chapter-3-back-vowels', title: 'Chapter 3: Back Vowels' },
  { id: 'chapter-4-consonants-syllabic-sounds', title: 'Chapter 4: Consonants and Syllabic Sounds' }
];

// Simple markdown to HTML converter for basic formatting
function markdownToHtml(markdown: string): string {
  return markdown
    // Headers
    .replace(/^# (.+)$/gm, '<h1 class="text-4xl font-bold text-gray-900 mb-6">$1</h1>')
    .replace(/^## (.+)$/gm, '<h2 class="text-3xl font-semibold text-gray-900 mb-4 mt-8">$1</h2>')
    .replace(/^### (.+)$/gm, '<h3 class="text-2xl font-semibold text-gray-900 mb-3 mt-6">$1</h3>')
    .replace(/^#### (.+)$/gm, '<h4 class="text-xl font-semibold text-gray-900 mb-2 mt-4">$1</h4>')
    
    // Bold and italic
    .replace(/\*\*(.+?)\*\*/g, '<strong class="font-semibold">$1</strong>')
    .replace(/\*(.+?)\*/g, '<em class="italic">$1</em>')
    
    // Links
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-blue-600 hover:text-blue-800 underline">$1</a>')
    
    // Code blocks
    .replace(/```[\s\S]*?```/g, (match) => {
      const code = match.replace(/```/g, '').trim();
      return `<pre class="bg-gray-100 rounded p-4 overflow-x-auto mb-4"><code class="text-sm">${code}</code></pre>`;
    })
    
    // Inline code
    .replace(/`([^`]+)`/g, '<code class="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono">$1</code>')
    
    // Tables
    .replace(/^\|(.+)\|$/gm, (match) => {
      if (match.includes('---')) {
        return ''; // Skip separator rows
      }
      const cells = match.split('|').slice(1, -1).map(cell => cell.trim());
      const isHeader = match === match.match(/^\|(.+)\|$/m)?.[0]; // First table row
      const tag = isHeader ? 'th' : 'td';
      const className = isHeader ? 'border border-gray-300 px-4 py-2 bg-gray-50 font-semibold text-left' : 'border border-gray-300 px-4 py-2';
      
      return `<tr>${cells.map(cell => `<${tag} class="${className}">${cell}</${tag}>`).join('')}</tr>`;
    })
    
    // Wrap tables
    .replace(/<tr>.*<\/tr>/s, (match) => {
      return `<div class="overflow-x-auto mb-6"><table class="min-w-full border-collapse border border-gray-300">${match}</table></div>`;
    })
    
    // Lists
    .replace(/^\* (.+)$/gm, '<li class="mb-1">$1</li>')
    .replace(/^- (.+)$/gm, '<li class="mb-1">$1</li>')
    .replace(/^\d+\. (.+)$/gm, '<li class="mb-1">$1</li>')
    
    // Wrap consecutive list items in ul/ol
    .replace(/(<li class="mb-1">.*<\/li>\n?)+/g, (match) => {
      return `<ul class="list-disc list-inside mb-4 ml-4">${match}</ul>`;
    })
    
    // Paragraphs
    .replace(/^([^<\n].+)$/gm, '<p class="mb-4 leading-relaxed">$1</p>')
    
    // Horizontal rules
    .replace(/^---$/gm, '<hr class="my-8 border-gray-300">')
    
    // Line breaks
    .replace(/\n/g, '');
}

interface PageProps {
  params: {
    chapter: string;
  };
}

export default function ChapterPage({ params }: PageProps) {
  const { chapter } = params;
  
  // Find the chapter info
  const currentChapter = chapters.find(ch => ch.id === chapter);
  if (!currentChapter) {
    notFound();
  }
  
  // Get current chapter index for navigation
  const currentIndex = chapters.findIndex(ch => ch.id === chapter);
  const prevChapter = currentIndex > 0 ? chapters[currentIndex - 1] : null;
  const nextChapter = currentIndex < chapters.length - 1 ? chapters[currentIndex + 1] : null;
  
  // Read the markdown file
  let content = '';
  try {
    const filePath = path.join(process.cwd(), 'book', `${chapter}.md`);
    content = fs.readFileSync(filePath, 'utf8');
  } catch (error) {
    console.error(`Error reading file: ${path.join(process.cwd(), 'book', `${chapter}.md`)}`, error);
    notFound();
  }
  
  // Convert markdown to HTML
  const htmlContent = markdownToHtml(content);
  
  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8">
        <Link 
          href="/book" 
          className="text-blue-600 hover:text-blue-800 no-underline mb-4 inline-block"
        >
          ← Back to Table of Contents
        </Link>
      </div>

      <article className="prose prose-lg max-w-none">
        <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
      </article>
      
      {/* Navigation */}
      <div className="flex justify-between items-center mt-12 pt-8 border-t border-gray-200">
        <div className="flex-1">
          {prevChapter && (
            <Link 
              href={`/book/${prevChapter.id}`}
              className="inline-flex items-center text-blue-600 hover:text-blue-800 no-underline"
            >
              <svg className="mr-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              <div>
                <div className="text-sm text-gray-500">Previous</div>
                <div className="font-medium">{prevChapter.title}</div>
              </div>
            </Link>
          )}
        </div>
        
        <div className="flex-1 text-right">
          {nextChapter && (
            <Link 
              href={`/book/${nextChapter.id}`}
              className="inline-flex items-center text-blue-600 hover:text-blue-800 no-underline"
            >
              <div>
                <div className="text-sm text-gray-500">Next</div>
                <div className="font-medium">{nextChapter.title}</div>
              </div>
              <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}

// Generate static params for all chapters
export async function generateStaticParams() {
  return chapters.map((chapter) => ({
    chapter: chapter.id,
  }));
}