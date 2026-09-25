"use client";
import { useState } from "react";
import Link from "next/link";

export default function Home() {
  const [text, setText] = useState("");
  const [location, setLocation] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setResult(null);

    // Client-side validation
    if (text.length < 10 || text.length > 2000) {
      setError("Text must be between 10 and 2000 characters.");
      return;
    }
    if (location.length < 3 || location.length > 200) {
      setError("Location must be between 3 and 200 characters.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("/api/complaints", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text, location }),
      });

      if (!res.ok) {
        if (res.status === 429) {
          throw new Error(`Rate limit exceeded. Try again in ${res.headers.get("Retry-After")}s.`);
        }
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Failed to connect to the backend server. Is it running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8 max-w-2xl mx-auto text-black">
      <h1 className="text-3xl font-bold mb-6 text-blue-800">Report a Civic Issue</h1>
      
      {result ? (
        <div className="bg-green-50 p-6 rounded-lg border border-green-200">
          <h2 className="text-2xl text-green-700 font-semibold mb-4">Complaint Submitted Successfully!</h2>
          <div className="space-y-2 text-gray-800 mb-6">
            <p><strong>Tracking ID:</strong> <span className="font-mono bg-white px-2 py-1 rounded">{result.id}</span></p>
            <p><strong>Category:</strong> {result.category}</p>
            <p><strong>Priority:</strong> {result.priority}</p>
            <p><strong>AI Summary:</strong> {result.summary}</p>
          </div>
          <div>
            <Link 
              href={`/status/${result.id}`}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 font-semibold"
            >
              Track Status
            </Link>
            <button 
              onClick={() => {setResult(null); setText(""); setLocation("");}}
              className="ml-6 text-blue-600 hover:underline font-medium"
            >
              Submit Another
            </button>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4 bg-gray-50 p-6 rounded-lg shadow-sm border border-gray-200">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">Issue Description (min 10 chars)</label>
            <textarea
              className="w-full border border-gray-300 rounded-md p-2 min-h-[120px] focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="e.g., The streetlight is broken in my street..."
              required
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">Location (min 3 chars)</label>
            <input
              type="text"
              className="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g., Sector 4, Street 12"
              required
            />
          </div>
          
          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded-md border border-red-200 font-medium">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {loading ? "Submitting..." : "Submit Complaint"}
          </button>
        </form>
      )}
    </main>
  );
}
