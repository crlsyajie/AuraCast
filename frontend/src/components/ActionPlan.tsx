"use client";

import { useEffect, useState } from "react";
import { Info, AlertTriangle, ShieldCheck, Umbrella, Flame, ThermometerSnowflake, Sun } from "lucide-react";

export function ActionPlan({ derived }: { derived?: any }) {
  const [recommendation, setRecommendation] = useState<string>("Waiting for weather data...");
  const [scenario, setScenario] = useState<string>("");

  useEffect(() => {
    async function fetchActionPlan() {
      if (!derived) return;

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
          }),
        });
        const data = await res.json();
        setRecommendation(data.recommendation);
        setScenario(data.scenario);
      } catch (error) {
        console.error("Failed to fetch action plan:", error);
        setRecommendation("Unable to load recommendation at this time.");
      }
    }

    fetchActionPlan();
  }, [derived]);

  let Icon = Info;
  let iconColor = "text-blue-400";
  let bgClass = "bg-blue-500/20";

  if (scenario === "Rain/Windy") {
    Icon = AlertTriangle;
    iconColor = "text-yellow-400";
    bgClass = "bg-yellow-500/20";
  } else if (scenario === "Rain") {
    Icon = Umbrella;
    iconColor = "text-blue-400";
    bgClass = "bg-blue-500/20";
  } else if (scenario === "Hot/Humid" || scenario === "Hot") {
    Icon = Flame;
    iconColor = "text-orange-400";
    bgClass = "bg-orange-500/20";
  } else if (scenario === "Sunny/High UV") {
    Icon = Sun;
    iconColor = "text-yellow-400";
    bgClass = "bg-yellow-500/20";
  } else if (scenario === "Cold") {
    Icon = ThermometerSnowflake;
    iconColor = "text-cyan-400";
    bgClass = "bg-cyan-500/20";
  } else if (scenario === "Moderate") {
    Icon = ShieldCheck;
    iconColor = "text-green-400";
    bgClass = "bg-green-500/20";
  }

  return (
    <div className="bg-[#1c1c21] rounded-3xl p-6 flex flex-col justify-between h-full">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-medium">Daily Smart Recommendations</h3>
        <div className="flex items-center space-x-1 text-sm text-gray-400 cursor-pointer hover:text-white transition-colors">
          <span>See All</span>
          <span>v</span>
        </div>
      </div>

      <div className="bg-[#2c2c31] rounded-2xl p-4 flex items-start space-x-4 h-full">
        <div className={`${bgClass} p-2 rounded-full mt-1`}>
          <Icon className={`w-5 h-5 ${iconColor}`} />
        </div>
        <div>
          <h4 className="font-semibold text-lg mb-1">Daily Action Plan</h4>
          <p className="text-gray-300 text-sm leading-relaxed">
            {recommendation}
          </p>
        </div>
      </div>
    </div>
  );
}
