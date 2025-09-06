import Link from "next/link";

const chapters = [
  {
    id: "introduction",
    title: "Introduction",
    description: "Overview of English pronunciation challenges for Spanish-speaking developers",
    readingTime: "3 min read"
  },
  {
    id: "chapter-1-sound-brain-map-ipa",
    title: "Chapter 1: The Sound Brain Map and the IPA",
    description: "Learn the International Phonetic Alphabet and the Sound Brain Map pedagogical tool",
    readingTime: "15 min read"
  },
  {
    id: "chapter-2-schwa-front-vowels", 
    title: "Chapter 2: Schwa and Front Vowels",
    description: "Master the schwa sound and distinguish between front vowels /i/, /ɪ/, /ɛ/, and /æ/",
    readingTime: "12 min read",
    comingSoon: true
  },
  {
    id: "chapter-3-back-vowels",
    title: "Chapter 3: Back Vowels", 
    description: "Learn back vowels including the challenging 'gringou' sound /oʊ/",
    readingTime: "10 min read",
    comingSoon: true
  },
  {
    id: "chapter-4-consonants-syllabic-sounds",
    title: "Chapter 4: Consonants and Syllabic Sounds",
    description: "Master the 'pirate sound' /ɝ/ and syllabic consonants",
    readingTime: "12 min read",
    comingSoon: true
  }
];

export default function BookPage() {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8">
        <Link 
          href="/" 
          className="text-blue-600 hover:text-blue-800 no-underline mb-4 inline-block"
        >
          ← Back to Home
        </Link>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Towards Confident English Pronunciation for Spanish-Speaking Developers
        </h1>
        <p className="text-xl text-gray-600 mb-6">
          A comprehensive guide to mastering English pronunciation using the International Phonetic Alphabet and technical vocabulary
        </p>
      </div>

      <div className="grid gap-6">
        {chapters.map((chapter, index) => (
          <div 
            key={chapter.id}
            className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <span className="bg-blue-100 text-blue-800 text-sm font-medium px-2.5 py-0.5 rounded">
                    {index === 0 ? 'Intro' : `Ch. ${index}`}
                  </span>
                  <span className="text-gray-500 text-sm">{chapter.readingTime}</span>
                </div>
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  {chapter.comingSoon ? (
                    <span className="text-gray-500">
                      {chapter.title}
                    </span>
                  ) : (
                    <Link 
                      href={`/book/${chapter.id}`}
                      className="text-gray-900 hover:text-blue-600 no-underline"
                    >
                      {chapter.title}
                    </Link>
                  )}
                </h2>
                <p className="text-gray-600 mb-4">
                  {chapter.description}
                </p>
                {chapter.comingSoon ? (
                  <div className="inline-flex items-center text-gray-500 font-medium">
                    <span className="bg-gray-100 text-gray-600 text-sm font-medium px-3 py-1 rounded-full">
                      Coming Soon
                    </span>
                  </div>
                ) : (
                  <Link 
                    href={`/book/${chapter.id}`}
                    className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium"
                  >
                    Read Chapter
                    <svg className="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </Link>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-12 p-6 bg-gray-50 rounded-lg">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">About This Guide</h2>
        <p className="text-gray-700 mb-4">
          This pronunciation guide is specifically designed for Spanish-speaking software developers 
          who want to improve their English pronunciation for professional communication. Each chapter 
          builds upon the previous one, using technical vocabulary and programming concepts to make 
          learning more relevant and engaging.
        </p>
        <p className="text-gray-700">
          The guide uses the International Phonetic Alphabet (IPA) and introduces the Sound Brain Map, 
          a pedagogical tool that helps visualize how different sounds are produced in the mouth.
        </p>
      </div>
    </div>
  );
}