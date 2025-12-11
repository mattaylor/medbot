'use client';

import { useState } from 'react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userMessage = { role: 'user', content: query };
    setMessages((prev) => [...prev, userMessage]);
    setQuery('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8001/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: query }),
      });
      const data = await res.json();
      const agentMessage = { role: 'agent', content: data.response };
      setMessages((prev) => [...prev, agentMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => [...prev, { role: 'agent', content: 'Error connecting to server.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24 bg-gray-900 text-white">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <h1 className="text-4xl font-bold mb-8">MedBot</h1>
      </div>

      <div className="flex-grow w-full max-w-2xl overflow-y-auto mb-8 border border-gray-700 rounded p-4 bg-gray-800">
        {messages.map((msg, idx) => (
          <div key={idx} className={`mb-4 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
            <span className={`inline-block p-2 rounded ${msg.role === 'user' ? 'bg-blue-600' : 'bg-green-600'}`}>
              {msg.content}
            </span>
          </div>
        ))}
        {loading && <div className="text-center">Thinking...</div>}
      </div>

      <form onSubmit={handleSubmit} className="w-full max-w-2xl flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-grow p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:border-blue-500"
          placeholder="Ask about treatments..."
        />
        <button
          type="submit"
          disabled={loading}
          className="p-2 bg-blue-600 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </main>
  );
}
