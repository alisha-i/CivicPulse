"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

export default function StatusPage() {
  const params = useParams();
  const id = params.id as string;
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!id) return;

    const fetchStatus = async () => {
      try {
        const res = await fetch(`/api/complaints/${id}`);
        if (!res.ok) {
          if (res.status === 404) {
            throw new Error("Complaint not found.");
          }
          throw new Error(`Server error: ${res.status}`);
        }
        const json = await res.json();
        setData(json);
      } catch (err: any) {
        setError(err.message);
      }
    };

    fetchStatus();
    // Poll every 2 seconds
    const intervalId = setInterval(fetchStatus, 2000);
    return () => clearInterval(intervalId);
  }, [id]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "open": return "bg-yellow-100 text-yellow-800 border-yellow-300";
      case "in_progress": return "bg-blue-100 text-blue-800 border-blue-300";
      case "resolved": return "bg-green-100 text-green-800 border-green-300";
      case "rejected": return "bg-red-100 text-red-800 border-red-300";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <main className="min-h-screen p-8 max-w-2xl mx-auto text-black">
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-blue-800">Tracking Status</h1>
        <Link href="/" className="text-blue-600 hover:underline font-medium">← Back to Home</Link>
      </div>

      {error ? (
        <div className="bg-red-50 text-red-600 p-4 rounded-md border border-red-200 font-medium">
          {error}
        </div>
      ) : !data ? (
        <div className="text-gray-500 font-medium">Loading status...</div>
      ) : (
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="mb-4">
            <span className={`inline-block px-3 py-1 rounded-full border font-bold text-sm uppercase tracking-wide ${getStatusColor(data.status)}`}>
              Status: {data.status.replace("_", " ")}
            </span>
            <span className="ml-3 text-xs text-gray-500">Live Polling Active (Every 2s)</span>
          </div>

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-md border">
              <div>
                <h3 className="text-xs uppercase text-gray-500 font-bold mb-1">Category</h3>
                <p className="font-semibold text-gray-900">{data.category}</p>
              </div>
              <div>
                <h3 className="text-xs uppercase text-gray-500 font-bold mb-1">Priority</h3>
                <p className="font-semibold text-gray-900">{data.priority}</p>
              </div>
            </div>

            <div>
              <h3 className="text-xs uppercase text-gray-500 font-bold mb-1">AI Summary</h3>
              <p className="bg-gray-50 p-3 rounded-md border text-gray-800">{data.summary}</p>
            </div>

            <div>
              <h3 className="text-xs uppercase text-gray-500 font-bold mb-1">Original Text</h3>
              <p className="text-gray-700 italic border-l-4 border-gray-300 pl-3 py-1">{data.text}</p>
            </div>
            
            <div className="text-xs text-gray-400 pt-4 border-t">
              Complaint ID: {data.id} <br/>
              Created: {new Date(data.created_at).toLocaleString()}
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
