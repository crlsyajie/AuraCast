"use client";

import { useEffect, useState } from "react";
import { Info, AlertTriangle, ShieldCheck, Zap } from "lucide-react";

export function ActionPlan({ derived, forecast }: { derived?: any, forecast?: any }) {
  const [actionPlan, setActionPlan] = useState<string>("Waiting for weather data...");
  const [smartRecommendations, setSmartRecommendations] = useState<string[]>([]);
  const [scenario, setScenario] = useState<string>("");

  useEffect(() => {
    async function fetchActionPlan() {
      if (!derived || !forecast || !forecast.list) return;

      const forecast24h = forecast.list.slice(0, 8).map((item: any) => ({
        temp: item.main.temp,
        pop: (item.pop || 0) * 100,
        wind: item.wind.speed * 3.6, // convert m/s to km/h
        humidity: item.main.humidity,
      }));

      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/v1/analyze`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            temp: derived.temp,
            pop: derived.pop,
            uvi: derived.uvi,
            wind: derived.wind,
            humidity: derived.humidity,
            forecast_24h: forecast24h,
          }),
        });
        const data = await res.json();
        setActionPlan(data.action_plan);
        setSmartRecommendations(data.smart_recommendations || []);
        setScenario(data.scenario);
      } catch (error) {
        console.error("Failed to fetch action plan:", error);
        setActionPlan("Unable to load recommendation at this time.");
      }
    }

    fetchActionPlan();
  }, [derived, forecast]);

  let Icon = Info;
  let iconColor = "text-blue-400";
  let bgClass = "bg-blue-500/20";

  if (scenario === "Rain/Windy" || scenario === "Sunny/High UV") {
    Icon = AlertTriangle;
    iconColor = "text-yellow-400";
    bgClass = "bg-yellow-500/20";
  } else if (scenario === "Moderate") {
    Icon = ShieldCheck;
    iconColor = "text-green-400";
    bgClass = "bg-green-500/20";
  }

  return (
    <div className="bg-[#1c1c21] rounded-3xl p-6 flex flex-col h-full overflow-y-auto">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-medium">Daily Smart Recommendations</h3>
        <div className="flex items-center space-x-1 text-sm text-gray-400 cursor-pointer hover:text-white transition-colors">
          <span>See All</span>
          <span>v</span>
        </div>
      </div>

      <div className="flex flex-col gap-3">
        {/* Main Action Plan Card */}
        <div className="bg-[#2c2c31] rounded-2xl p-4 flex items-start space-x-4">
          <div className={`${bgClass} p-2 rounded-full mt-1`}>
            <Icon className={`w-5 h-5 ${iconColor}`} />
          </div>
          <div>
            <h4 className="font-semibold text-lg mb-1">Daily Action Plan</h4>
            <p className="text-gray-300 text-sm leading-relaxed">
              {actionPlan}
            </p>
          </div>
        </div>

        {/* Smart Recommendations List */}
        {smartRecommendations.map((rec, index) => (
          <div key={index} className="bg-[#2c2c31] rounded-2xl p-3 flex items-center space-x-3">
             <div className="bg-purple-500/20 p-2 rounded-full">
               <Zap className="w-4 h-4 text-purple-400" />
             </div>
             <p className="text-gray-200 text-sm font-medium">{rec}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
