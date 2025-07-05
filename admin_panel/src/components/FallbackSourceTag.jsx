import React, { useState } from "react";
import api from "../api";

export default function FallbackSourceTag() {
  const [userId, setUserId] = useState("");
  const [source, setSource] = useState(null);
  const [loading, setLoading] = useState(false);

  const getColor = (src) => {
    switch ((src || "").toUpperCase()) {
      case "RASA":
        return "bg-green-600";
      case "RAG":
        return "bg-blue-500";
      case "LLM":
        return "bg-purple-500";
      case "PLUGIN":
        return "bg-pink-600";
      case "LOCAL":
        return "bg-yellow-600";
      case "NONE":
        return "bg-gray-500";
      case "ERROR":
        return "bg-red-600";
      default:
        return "bg-gray-400";
    }
  };

  const fetchSource = async () => {
    if (!userId) return;
    setLoading(true);
    setSource(null);
    try {
      const res = await api.get(`/admin/fallback-source/${userId}`);
      setSource((res.data.source || "UNKNOWN").toUpperCase());
    } catch (err) {
      setSource("ERROR");
    }
    setLoading(false);
  };

  return (
    <div className="p-4 bg-white rounded shadow mt-4">
      <h3 className="text-lg font-semibold mb-2">View Fallback Engine</h3>
      <input
        type="text"
        placeholder="Enter User ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        className="border px-2 py-1 rounded mr-2"
      />
      <button
        onClick={fetchSource}
        className="bg-blue-600 text-white px-3 py-1 rounded"
        disabled={loading || !userId}
      >
        {loading ? "Checking..." : "Check"}
      </button>

      {source && (
        <div className="mt-2">
          <span className="font-bold">Engine Used:</span>{" "}
          <span className={`font-mono px-2 py-1 rounded text-white ${getColor(source)}`}>
            {source}
          </span>
        </div>
      )}
    </div>
  );
}