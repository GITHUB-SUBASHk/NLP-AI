// if/web/src/components/RecentFallbacks.tsx 
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type Fallback = {
  intent?: string;
  message: string;
  id?: string | number;
};

export default function RecentFallbacks({ fallbacks = [] }: { fallbacks: Fallback[] }) {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Recent Fallbacks</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4 max-h-[300px] overflow-y-auto">
        {fallbacks.length === 0 ? (
          <p className="text-sm text-zinc-500">No fallbacks recorded.</p>
        ) : (
          <ul aria-label="Recent fallback messages" className="space-y-2">
            {fallbacks.map((fb, i) => (
              <li
                key={fb.id ?? i}
                className="rounded-lg bg-zinc-100 dark:bg-zinc-800 p-3"
              >
                <p className="text-sm font-medium">
                  Intent: <span className="text-primary">{fb.intent || "unknown"}</span>
                </p>
                <p className="text-xs text-zinc-500 mt-1">
                  Message: {fb.message}
                </p>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}

