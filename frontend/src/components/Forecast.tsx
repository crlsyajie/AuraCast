import { CloudRain, CloudSun, CloudLightning, Snowflake, Cloud, Sun } from "lucide-react";

export function Forecast({ data }: { data: any }) {
  if (!data) return <div className="bg-[#1c1c21] rounded-3xl p-6 flex-1 text-center">Loading...</div>;

  const forecastList = data.forecast.list;

  // Filter 1 item per day (e.g. at 12:00:00)
  const dailyForecasts = forecastList.filter((item: any) => item.dt_txt.includes("12:00:00")).slice(0, 5);

  return (
    <div className="bg-[#1c1c21] rounded-3xl p-6 flex-1">
      <h3 className="text-lg font-medium mb-4">5 Day Forecast</h3>
      <div className="flex space-x-4 overflow-x-auto pb-2 scrollbar-hide">
        {dailyForecasts.map((day: any, idx: number) => {
          const date = new Date(day.dt * 1000);
          const dayName = idx === 0 ? "Today" : date.toLocaleDateString('en-US', { weekday: 'short' });
          const tempMax = Math.round(day.main.temp_max);
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
              <span className="text-sm text-gray-300">{dayName}</span>
              <div className="my-2"><Icon className={`w-8 h-8 ${iconColor}`} /></div>
              <span className="text-sm font-semibold">{tempMax}°C</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
