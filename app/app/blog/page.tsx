import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const blogPosts = [
  {
    slug: "high-frequency-phrasal-verbs",
    title: "High-Frequency Phrasal Verbs: The Essential Guide for English Learners",
    description: "Discover the most common phrasal verbs based on corpus research, understand their importance in TESOL, and learn from authoritative resources.",
    date: "2024-01-24",
    readTime: "15 min read",
    tags: ["Phrasal Verbs", "TESOL", "Research", "Corpus Linguistics"]
  }
];

export default function BlogPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Language Learning Blog
        </h1>
        <p className="text-lg text-gray-600">
          Evidence-based insights and resources for mastering English
        </p>
      </div>

      <div className="grid gap-6">
        {blogPosts.map((post) => (
          <Link key={post.slug} href={`/blog/${post.slug}`}>
            <Card className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardHeader>
                <div className="flex justify-between items-start mb-2">
                  <CardTitle className="text-2xl">{post.title}</CardTitle>
                </div>
                <CardDescription className="text-base">
                  {post.description}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span>{post.date}</span>
                  <span>•</span>
                  <span>{post.readTime}</span>
                </div>
                <div className="flex gap-2 mt-4">
                  {post.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}