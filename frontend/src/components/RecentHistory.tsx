"use client";

import { useEffect, useState } from "react";
import { History, Thermometer, Droplets, Sun } from "lucide-react";

type HistoryLog = {
  id: number;
  recommendation: string;
  scenario: string;
  is_followed: boolean;
  timestamp: string;
  weather: {
    temperature: number;
    humidity: number;
    uv_data: number;
  };
};

export function RecentHistory() {
  const [logs, setLogs] = useState<HistoryLog[]>([]);

  useEffect(() => {
    async function fetchHistory() {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/v1/history`);
        const data = await res.json();
        setLogs(data);
      } catch (error) {
        console.error("Failed to fetch history:", error);
      }
    }

    fetchHistory();
  }, []);

  return (
    <div className="bg-[#1c1c21] rounded-3xl p-6 mt-6">
      <div className="flex items-center mb-6 space-x-2">
        <History className="text-gray-400 w-5 h-5" />
        <h3 className="text-lg font-medium">Recent History</h3>
      </div>

      {logs.length === 0 ? (
        <p className="text-gray-400 text-sm">No history available yet.</p>
      ) : (
        <div className="space-y-4">
          {logs.map((log) => (
            <div key={log.id} className="bg-[#2c2c31] rounded-2xl p-4 flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0 md:space-x-4">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-1">
                  <span className="text-sm font-semibold text-blue-400">{log.scenario}</span>
                  <span className="text-xs text-gray-500">
                    {new Date(log.timestamp).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}
                  </span>
                </div>
                <p className="text-gray-300 text-sm">{log.recommendation}</p>
              </div>

              <div className="flex items-center space-x-4 shrink-0">
                <div className="flex items-center space-x-1 text-xs text-gray-400">
                  <Thermometer className="w-3 h-3" />
                  <span>{log.weather.temperature.toFixed(1)}°C</span>
                </div>
                <div className="flex items-center space-x-1 text-xs text-gray-400">
                  <Droplets className="w-3 h-3" />
                  <span>{log.weather.humidity.toFixed(0)}%</span>
                </div>
                <div className="flex items-center space-x-1 text-xs text-gray-400">
                  <Sun className="w-3 h-3" />
                  <span>UV {log.weather.uv_data.toFixed(1)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
