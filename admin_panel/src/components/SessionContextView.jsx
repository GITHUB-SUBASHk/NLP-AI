import React from "react";
export default function SessionContextView({ session }) {
  if (!session || Object.keys(session).length === 0) return null;
  return (
    <div className="mb-6">
      <h2 className="font-bold mb-2">Session Context</h2>
      <pre className="bg-gray-100 p-2 rounded">{JSON.stringify(session, null, 2)}</pre>
    </div>
  );
}