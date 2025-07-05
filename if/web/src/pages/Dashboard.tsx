import WelcomeHeader from "@/components/WelcomeHeader";
import StatusCard from "@/components/StatusCard";
import ConfidenceDonut from "@/components/ConfidenceDonut";
import RecentFallbacks from "@/components/RecentFallbacks";
import { useDashboard } from "@/hooks/useDashboard";

export default function Dashboard() {
  const { confidence, fallbacks, botStatus } = useDashboard();

  return (
    <div className="min-h-screen p-6 bg-muted text-muted-foreground space-y-6">
      <WelcomeHeader />
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatusCard botStatus={botStatus} />
        <ConfidenceDonut fallbackPercent={confidence?.fallback_percent?.fallback || 0} />
        <div className="md:col-span-2 lg:col-span-1">
          <RecentFallbacks fallbacks={fallbacks} />
        </div>
      </div>
    </div>
  );
}