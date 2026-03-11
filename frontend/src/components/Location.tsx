import { MapPin, CloudRain, Sun, Cloud, Snowflake } from "lucide-react";

export function Location({ data }: { data: any }) {
  if (!data) return <div className="bg-[#1c1c21] rounded-3xl p-6 relative flex-1 text-center">Loading...</div>;

  const current = data.current;
  const temp = Math.round(current.main.temp);
  const feelsLike = Math.round(current.main.feels_like);
  const tempMin = Math.round(current.main.temp_min);
  const tempMax = Math.round(current.main.temp_max);
  const description = current.weather[0].main;

  const date = new Date(current.dt * 1000);
  const dayName = date.toLocaleDateString('en-US', { weekday: 'long' });
  const formattedDate = date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });

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
  }

  return (
    <div className="bg-[#1c1c21] rounded-3xl p-6 relative overflow-hidden flex-1">
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center space-x-2 text-gray-300 bg-[#2c2c31] rounded-full px-3 py-1">
          <MapPin className="w-4 h-4" />
          <span className="text-sm">{current.name}, {current.sys.country}</span>
        </div>
        <div className="bg-[#2c2c31] rounded-full px-2 py-1 flex items-center space-x-1 cursor-pointer">
            <span className="text-sm">°C</span>
            <span className="text-xs">v</span>
        </div>
      </div>

      <div className="mt-6">
        <h1 className="text-3xl font-semibold">{dayName}</h1>
        <p className="text-gray-400 text-sm mt-1">{formattedDate}</p>
      </div>

      <div className="flex justify-between items-end mt-12">
        <div className="relative">
            <Icon className={`w-24 h-24 ${iconColor}`} />
        </div>
        <div className="text-right">
          <h2 className="text-5xl font-bold">{temp}°C</h2>
          <p className="text-gray-400 text-xl">/{tempMax}°C</p>
          <p className="text-lg font-medium mt-2">{description}</p>
          <p className="text-gray-400 text-sm">Feels like {feelsLike}°</p>
        </div>
      </div>
    </div>
  );
}
