import { CloudRain, CloudSun, CloudLightning, Snowflake, Cloud, Sun } from "lucide-react";

export function Forecast({ data }: { data: any }) {
  if (!data || !data.forecast || !data.forecast.list) return <div className="bg-[#1c1c21] rounded-3xl p-6 flex-1 text-center">Loading...</div>;

  const forecastList = data.forecast.list;

  // Next 24 hours (8 intervals of 3 hours)
  const dailyForecasts = forecastList.slice(0, 8);

  return (
    <div className="bg-[#1c1c21] rounded-3xl p-6 flex-1">
      <h3 className="text-lg font-medium mb-4">24-Hour Forecast</h3>
      <div className="flex space-x-4 overflow-x-auto pb-2 scrollbar-hide">
        {dailyForecasts.map((day: any, idx: number) => {
          const date = new Date(day.dt * 1000);
          const timeString = idx === 0 ? "Now" : date.toLocaleTimeString([], { hour: 'numeric', hour12: true });
          const tempMax = Math.round(day.main.temp);
          const description = day.weather[0].main;

          let Icon = Sun;
          let iconColor = "text-yellow-400";
          if (description === "Rain") {
            Icon = CloudRain;
            iconColor = "text-blue-400";
          } else if (description === "Clouds") {
            Icon = Cloud;
            iconColor = "text-gray-400";
          } else if (description === "Snow") {
            Icon = Snowflake;
            iconColor = "text-white";
          } else if (description === "Thunderstorm") {
            Icon = CloudLightning;
            iconColor = "text-yellow-500";
          }

          return (
             <div key={idx} className={`flex flex-col items-center justify-between p-4 rounded-2xl min-w-[80px] h-36 ${idx === 0 ? 'bg-[#2c2c31]' : 'bg-transparent border border-[#2c2c31]'}`}>
              <span className="text-sm text-gray-300">{timeString}</span>
              <div className="my-2"><Icon className={`w-8 h-8 ${iconColor}`} /></div>
              <span className="text-sm font-semibold">{tempMax}°C</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
