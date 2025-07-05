// src/hooks/useDashboard.ts

import { useEffect, useState } from "react";
import { getBotConfidence } from "@/api/analytics";
import { getRecentFallbacks } from "@/api/fallbacks";
import { getBotStatus } from "@/api/bot";

export const useDashboard = () => {
  const [confidence, setConfidence] = useState(null);
  const [fallbacks, setFallbacks] = useState([]);
  const [botStatus, setBotStatus] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const [conf, fb, status] = await Promise.all([
        getBotConfidence(),
        getRecentFallbacks(),
        getBotStatus(),
      ]);
      setConfidence(conf);
      setFallbacks(fb);
      setBotStatus(status);
    };

    fetchData();
  }, []);

  return {
    confidence,
    fallbacks,
    botStatus,
  };
};