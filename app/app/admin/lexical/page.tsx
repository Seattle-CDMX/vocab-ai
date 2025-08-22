'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TARGET_LEXICAL_ITEMS, type LexicalItem } from '@/lib/lexical-items';
import { ArrowLeft, Edit, Eye, Trash2 } from 'lucide-react';
import Link from 'next/link';

export default function LexicalItemsAdmin() {
  const [items, setItems] = useState<LexicalItem[]>(TARGET_LEXICAL_ITEMS);
  const [selectedItem, setSelectedItem] = useState<LexicalItem | null>(null);

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this lexical item?')) {
      setItems(items.filter(item => item.id !== id));
      if (selectedItem?.id === id) {
        setSelectedItem(null);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-4 mb-4">
            <Link href="/admin">
              <Button variant="ghost" className="flex items-center gap-2">
                <ArrowLeft className="w-4 h-4" />
                Back to Admin
              </Button>
            </Link>
            <h1 className="text-3xl font-bold text-gray-900">Lexical Items Management</h1>
          </div>
          <p className="text-gray-600">Manage target phrasal verbs for vocabulary practice sessions</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Items List */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">Current Items ({items.length})</h2>
              <Button variant="default">
                <Edit className="w-4 h-4 mr-2" />
                Add New Item
              </Button>
            </div>

            <div className="space-y-3">
              {items.map((item) => (
                <Card 
                  key={item.id} 
                  className={`cursor-pointer transition-all duration-200 hover:shadow-md ${
                    selectedItem?.id === item.id ? 'ring-2 ring-blue-500' : ''
                  }`}
                  onClick={() => setSelectedItem(item)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="font-semibold text-gray-900">{item.phrasal}</h3>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(item.difficulty)}`}>
                            {item.difficulty}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 line-clamp-2">{item.definition}</p>
                      </div>
                      <div className="flex items-center gap-2 ml-4">
                        <Button 
                          variant="ghost" 
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedItem(item);
                          }}
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                        <Button 
                          variant="ghost" 
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDelete(item.id);
                          }}
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Item Details */}
          <div>
            {selectedItem ? (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    {selectedItem.phrasal}
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(selectedItem.difficulty)}`}>
                      {selectedItem.difficulty}
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Definition</h4>
                    <p className="text-gray-700">{selectedItem.definition}</p>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Example</h4>
                    <p className="text-gray-700 italic">&ldquo;{selectedItem.example}&rdquo;</p>
                  </div>

                  {selectedItem.senses && selectedItem.senses.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Spanish Senses</h4>
                      <ul className="space-y-1">
                        {selectedItem.senses.map((sense, index) => (
                          <li key={index} className="text-gray-700 text-sm">
                            • {sense}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="pt-4 border-t">
                    <div className="flex gap-2">
                      <Button variant="outline" className="flex-1">
                        <Edit className="w-4 h-4 mr-2" />
                        Edit Item
                      </Button>
                      <Button 
                        variant="destructive" 
                        onClick={() => handleDelete(selectedItem.id)}
                      >
                        <Trash2 className="w-4 h-4 mr-2" />
                        Delete
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardContent className="p-8 text-center">
                  <div className="text-gray-400 mb-2">
                    <Eye className="w-12 h-12 mx-auto" />
                  </div>
                  <p className="text-gray-500">Select a lexical item to view details</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>

        {/* Statistics */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-green-600">
                {items.filter(item => item.difficulty === 'beginner').length}
              </div>
              <div className="text-sm text-gray-600">Beginner Items</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-yellow-600">
                {items.filter(item => item.difficulty === 'intermediate').length}
              </div>
              <div className="text-sm text-gray-600">Intermediate Items</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-red-600">
                {items.filter(item => item.difficulty === 'advanced').length}
              </div>
              <div className="text-sm text-gray-600">Advanced Items</div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}