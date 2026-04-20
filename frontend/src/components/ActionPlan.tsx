"use client";

import { useEffect, useState } from "react";
import { Info, AlertTriangle, ShieldCheck, CheckCircle2 } from "lucide-react";

export function ActionPlan({ derived }: { derived?: any }) {
  const [recommendation, setRecommendation] = useState<string>("Waiting for weather data...");
  const [scenario, setScenario] = useState<string>("");
  const [whatToBring, setWhatToBring] = useState<string[]>([]);
  const [howToPlan, setHowToPlan] = useState<string>("");

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
        setWhatToBring(data.what_to_bring || []);
        setHowToPlan(data.how_to_plan || "");
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
    <div className="bg-[#1c1c21] rounded-3xl p-6 flex flex-col justify-between h-full overflow-hidden">
      <div className="flex justify-between items-center mb-4 flex-shrink-0">
        <h3 className="text-lg font-medium">Daily Smart Recommendations</h3>
        <div className="flex items-center space-x-1 text-sm text-gray-400 cursor-pointer hover:text-white transition-colors">
          <span>See All</span>
          <span>v</span>
        </div>
      </div>

      <div className="flex flex-col space-y-4 overflow-y-auto pr-2 scrollbar-hide flex-grow">
        <div className="bg-[#2c2c31] rounded-2xl p-4 flex items-start space-x-4">
          <div className={`${bgClass} p-2 rounded-full mt-1`}>
            <Icon className={`w-5 h-5 ${iconColor}`} />
          </div>
          <div>
            <h4 className="font-semibold text-lg mb-1">Daily Action Plan</h4>
            <p className="text-gray-300 text-sm leading-relaxed">
              {howToPlan || recommendation}
            </p>
          </div>
        </div>

        {whatToBring.length > 0 && (
          <div className="bg-[#2c2c31] rounded-2xl p-4 flex items-start space-x-4">
            <div className="bg-purple-500/20 p-2 rounded-full mt-1">
              <CheckCircle2 className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <h4 className="font-semibold text-lg mb-2">What to Bring</h4>
              <div className="flex flex-wrap gap-2">
                {whatToBring.map((item, idx) => (
                  <span key={idx} className="bg-[#1c1c21] text-gray-300 text-xs px-3 py-1.5 rounded-full border border-gray-700">
                    {item}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
