// if/web/src/components/ConfidenceDonut.tsx 
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const COLORS = ["#22c55e", "#ef4444"];

export default function ConfidenceDonut({ fallbackPercent = 0 }: { fallbackPercent: number }) {
  const data = [
    { name: "Success", value: 100 - fallbackPercent },
    { name: "Fallback", value: fallbackPercent },
  ];

  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Bot Confidence</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-40 w-full flex flex-col items-center justify-center">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                dataKey="value"
                innerRadius={60}
                outerRadius={80}
                startAngle={90}
                endAngle={450}
              >
                {data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
          <p className="text-center text-sm text-zinc-500 mt-2">
            Success: {(100 - fallbackPercent).toFixed(1)}% &nbsp;|&nbsp; Fallbacks: {fallbackPercent.toFixed(1)}%
          </p>
        </div>
      </CardContent>
    </Card>
  );
}

