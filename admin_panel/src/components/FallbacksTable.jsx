import React from "react";
export default function FallbacksTable({ fallbacks }) {
  if (!fallbacks.length) return null;
  return (
    <div className="mb-6">
      <h2 className="font-bold mb-2">Fallback Events</h2>
      <table className="min-w-full bg-white border">
        <thead>
          <tr>
            <th className="border px-2 py-1">User</th>
            <th className="border px-2 py-1">Time</th>
            <th className="border px-2 py-1">Intent</th>
            <th className="border px-2 py-1">Message</th>
            <th className="border px-2 py-1">Confidence</th>
          </tr>
        </thead>
        <tbody>
          {fallbacks.map((fb, i) => (
            <tr key={i}>
              <td className="border px-2 py-1">{fb.user_id}</td>
              <td className="border px-2 py-1">{fb.timestamp}</td>
              <td className="border px-2 py-1">{fb.intent}</td>
              <td className="border px-2 py-1">{fb.message}</td>
              <td className="border px-2 py-1">{fb.confidence}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}