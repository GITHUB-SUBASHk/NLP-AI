import PluginList from "@/components/PluginList";
import { useAuth } from "@/auth/useAuth";
import { Navigate } from "react-router-dom";

export default function Plugins() {
  const { user } = useAuth();

  if (user?.role !== "admin") return <Navigate to="/" replace />;

  return (
    <div className="min-h-screen p-6 bg-muted text-muted-foreground space-y-6">
      <h1 className="text-2xl font-bold">Plugin Control Panel</h1>
      <PluginList />
    </div>
  );
}