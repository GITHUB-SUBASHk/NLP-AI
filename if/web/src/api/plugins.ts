import api from "./api";

// Fetch plugin list
export async function fetchPlugins() {
  const res = await api.get("/admin/plugins");
  return res.data;
}

// Toggle plugin (enable/disable)
export async function togglePlugin(pluginName: string, enabled: boolean) {
  const res = await api.post("/admin/plugins/toggle", { plugin: pluginName, enabled });
  return res.data;
}

// Plugin usage analytics
export async function fetchPluginUsage() {
  const res = await api.get("/analytics/plugins");
  return res.data.plugin_usage;
}