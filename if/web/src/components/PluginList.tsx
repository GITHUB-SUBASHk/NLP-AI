import { useEffect, useState } from "react";
import { fetchPlugins, togglePlugin } from "@/api/plugins";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";

type Plugin = {
  name: string;
  enabled: boolean;
  description?: string;
};

export default function PluginList() {
  const [plugins, setPlugins] = useState<Plugin[]>([]);

  useEffect(() => {
    fetchPlugins().then(setPlugins);
  }, []);

  const handleToggle = async (plugin: Plugin) => {
    const updated = { ...plugin, enabled: !plugin.enabled };
    await togglePlugin(plugin.name, updated.enabled);
    setPlugins((prev) =>
      prev.map((p) => (p.name === plugin.name ? updated : p))
    );
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Plugin Manager</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {plugins.length === 0 ? (
          <p className="text-sm text-zinc-500">No plugins found.</p>
        ) : (
          <ul className="space-y-3">
            {plugins.map((plugin) => (
              <li key={plugin.name} className="flex justify-between items-center">
                <div>
                  <p className="text-base font-medium">{plugin.name}</p>
                  {plugin.description && (
                    <p className="text-sm text-zinc-500">{plugin.description}</p>
                  )}
                </div>
                <Switch
                  checked={plugin.enabled}
                  onCheckedChange={() => handleToggle(plugin)}
                />
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}