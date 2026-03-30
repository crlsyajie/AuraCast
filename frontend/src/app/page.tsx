"use client";

import { useEffect, useState } from "react";
import { Location } from "@/components/Location";
import { ActionPlan } from "@/components/ActionPlan";
import { Highlight } from "@/components/Highlight";
import { Forecast } from "@/components/Forecast";
import { Sidebar } from "@/components/Sidebar";
import { RecentHistory } from "@/components/RecentHistory";

export default function Home() {
  const [weatherData, setWeatherData] = useState<any>(null);

  useEffect(() => {
    async function fetchWeather() {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/v1/weather?lat=13.75&lon=121.05`);
        const data = await res.json();
        setWeatherData(data);
      } catch (e) {
        console.error("Failed to fetch weather data", e);
      }
    }
    fetchWeather();
  }, []);

  return (
    <div className="flex min-h-screen bg-[#101014] text-white p-6 rounded-[2rem] m-4">
      <Sidebar />
      <main className="flex-1 flex flex-col ml-8 overflow-y-auto">
        {/* Header */}
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-gray-400 text-sm">Hi, Jules</h1>
            <h2 className="text-2xl font-bold">Good Morning</h2>
          </div>
          <div className="flex items-center space-x-4">
            <div className="bg-[#1c1c21] rounded-full px-4 py-2 flex items-center w-64">
              <span className="text-gray-400 mr-2">🔍</span>
              <input
                type="text"
                placeholder="Search your location"
                className="bg-transparent outline-none text-sm w-full"
              />
            </div>
            <div className="bg-[#1c1c21] rounded-full p-2 flex items-center space-x-2">
                <div className="text-gray-400 p-1">☀️</div>
                <div className="bg-[#2c2c31] rounded-full p-1 text-white">🌙</div>
            </div>
            <div className="w-10 h-10 rounded-full bg-gray-500 overflow-hidden">
                {/* User Avatar Placeholder */}
            </div>
          </div>
        </header>

        {/* Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1 h-[calc(100vh-140px)]">
          {/* Left Column (Location & Action Plan) */}
          <div className="lg:col-span-5 flex flex-col gap-6 h-full">
            <div className="flex-grow flex flex-col h-2/3">
              <Location data={weatherData} />
            </div>
            <div className="flex-shrink-0 h-1/3">
              <ActionPlan derived={weatherData?.derived} />
            </div>
          </div>

          {/* Right Column (Highlights & Forecast) */}
          <div className="lg:col-span-7 flex flex-col gap-6 h-full">
             <div className="flex-grow flex flex-col h-2/3">
               <Highlight data={weatherData} />
             </div>
             <div className="flex-shrink-0 h-1/3">
               <Forecast data={weatherData} />
             </div>
          </div>
        </div>

        {/* Recent History */}
        <div className="mt-8">
          <RecentHistory />
        </div>
      </main>
    </div>
  );
}
