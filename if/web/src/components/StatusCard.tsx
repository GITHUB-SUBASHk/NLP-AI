// File: if/web/src/components/StatusCard.tsx 
import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { toggleAutoReply, triggerTrain, fetchBotStats } from "@/api/bot";

type BotStatus = {
  online?: boolean;
  auto_reply?: boolean;
  status?: string;
};

export default function StatusCard({ botStatus: initialStatus }: { botStatus?: BotStatus }) {
  const [botStatus, setBotStatus] = useState<BotStatus>(initialStatus || {});
  const [autoReply, setAutoReply] = useState(initialStatus?.auto_reply ?? false);
  const [loading, setLoading] = useState(false);

  // Fetch status if not provided
  useEffect(() => {
    if (!initialStatus && fetchBotStats) {
      fetchBotStats().then((data: BotStatus) => {
        setBotStatus(data);
        setAutoReply(data.auto_reply ?? false);
      });
    }
  }, [initialStatus]);

  const handleToggle = async () => {
    const newState = !autoReply;
    await toggleAutoReply(newState);
    setAutoReply(newState);
    setBotStatus((prev) => ({ ...prev, auto_reply: newState }));
  };

  const handleTrainClick = async () => {
    setLoading(true);
    try {
      await triggerTrain();
      alert("Training triggered!");
    } catch {
      alert("Failed to trigger training");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      className="bg-white dark:bg-zinc-900 rounded-2xl shadow p-6"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      <Card>
        <CardContent className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold">Bot Status</h2>
            <span
              className={`font-medium ${
                botStatus?.online ? "text-green-500" : "text-yellow-500"
              }`}
            >
              {botStatus?.online ? "Online" : "Offline"}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span>Auto-reply</span>
            <Switch checked={autoReply} onCheckedChange={handleToggle} />
          </div>
          <div className="text-right">
            <Button className="mt-4 w-full" onClick={handleTrainClick} disabled={loading}>
              {loading ? "Training..." : "Train Bot"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

