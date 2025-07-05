import React, { useState, useEffect } from "react";
import api, { triggerTraining } from "../api";
import LogsTable from "./LogsTable";
import FallbacksTable from "./FallbacksTable";
import SessionContextView from "./SessionContextView";
import FallbackSourceTag from "./FallbackSourceTag";

export default function Dashboard() {
  const [logs, setLogs] = useState([]);
  const [fallbacks, setFallbacks] = useState([]);
  const [userId, setUserId] = useState("");
  const [session, setSession] = useState({});
  const [trainingStatus, setTrainingStatus] = useState("");
  const [isTraining, setIsTraining] = useState(false);

  useEffect(() => {
    fetchFallbacks();
  }, []);

  const fetchLogs = async () => {
    if (!userId) return;
    const res = await api.get(`/logs/${userId}`);
    setLogs(res.data);
  };

  const fetchFallbacks = async () => {
    const res = await api.get(`/fallbacks`);
    setFallbacks(res.data);
  };

  const fetchSession = async () => {
    if (!userId) return;
    const res = await api.get(`/session/${userId}`);
    setSession(res.data);
  };

  const handleTrainClick = async () => {
    setIsTraining(true);
    setTrainingStatus("");
    try {
      const data = await triggerTraining();
      if (data.status === "success") {
        setTrainingStatus(`✅ Model trained: ${data.stdout || data.model || "Success"}`);
      } else {
        setTrainingStatus(`❌ Training failed: ${data.stderr || "Unknown error"}`);
      }
    } catch (err) {
      setTrainingStatus("❌ Training failed. Check server logs.");
    } finally {
      setIsTraining(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">AI Assistant Admin Dashboard</h1>
      {/* Admin Controls */}
      <div className="mb-4 flex flex-col sm:flex-row gap-2 items-start sm:items-center">
        <div className="flex gap-2 items-center">
          <input
            className="border p-2 rounded"
            placeholder="User ID"
            value={userId}
            onChange={e => setUserId(e.target.value)}
          />
          <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={fetchLogs}>View Logs</button>
          <button className="bg-green-500 text-white px-4 py-2 rounded" onClick={fetchSession}>View Session</button>
          {userId && <FallbackSourceTag userId={userId} />}
        </div>
        <div className="flex flex-col sm:flex-row gap-2 sm:ml-4">
          <button
            onClick={handleTrainClick}
            disabled={isTraining}
            className={`bg-purple-600 text-white px-4 py-2 rounded ${isTraining ? "opacity-50 cursor-not-allowed" : ""}`}
          >
            {isTraining ? "Training..." : "Trigger RASA Training"}
          </button>
          {trainingStatus && <p className="mt-2 text-sm">{trainingStatus}</p>}
        </div>
      </div>
      {/* Add a global FallbackSourceTag for admin quick check */}
      <FallbackSourceTag />
      <LogsTable logs={logs} />
      <FallbacksTable fallbacks={fallbacks} />
      <SessionContextView session={session} />
    </div>
  );
}