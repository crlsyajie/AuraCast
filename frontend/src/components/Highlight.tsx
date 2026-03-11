import { Wind, Droplets, Sun, Eye, Sunrise, Sunset } from "lucide-react";

export function Highlight({ data }: { data: any }) {
  if (!data) return <div className="bg-[#1c1c21] rounded-3xl p-6 h-full flex items-center justify-center">Loading...</div>;

  const current = data.current;
  const windSpeed = (current.wind.speed * 3.6).toFixed(2); // m/s to km/h
  const humidity = current.main.humidity;
  const visibility = (current.visibility / 1000).toFixed(1); // m to km
  const uvi = data.derived.uvi;

  const sunrise = new Date(current.sys.sunrise * 1000).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
  const sunset = new Date(current.sys.sunset * 1000).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });

  return (
    <div className="bg-[#1c1c21] rounded-3xl p-6">
      <h3 className="text-lg font-medium mb-4">Today's Highlight</h3>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {/* Wind */}
        <div className="bg-[#2c2c31] p-4 rounded-2xl flex flex-col justify-between h-32">
          <div className="flex items-center space-x-2 text-gray-400">
            <Wind className="w-4 h-4" />
            <span className="text-sm">Wind Status</span>
          </div>
          <div>
             <span className="text-2xl font-semibold">{windSpeed}</span>
             <span className="text-sm ml-1 text-gray-400">km/h</span>
          </div>
          <span className="text-xs text-gray-400"></span>
        </div>

        {/* Humidity */}
        <div className="bg-[#2c2c31] p-4 rounded-2xl flex flex-col justify-between h-32">
          <div className="flex items-center space-x-2 text-gray-400">
            <Droplets className="w-4 h-4" />
            <span className="text-sm">Humidity</span>
          </div>
          <div>
            <span className="text-2xl font-semibold">{humidity}</span>
            <span className="text-sm ml-1 text-gray-400">%</span>
          </div>
          <span className="text-xs text-gray-400">{humidity > 60 ? "High humidity" : "Humidity is good"}</span>
        </div>

        {/* Sunrise */}
        <div className="bg-[#2c2c31] p-4 rounded-2xl flex items-center space-x-4 h-32">
          <Sunrise className="w-8 h-8 text-yellow-500" />
          <div className="flex flex-col">
            <span className="text-sm text-gray-400">Sunrise</span>
            <span className="text-lg font-semibold">{sunrise}</span>
          </div>
        </div>

        {/* UV Index */}
        <div className="bg-[#2c2c31] p-4 rounded-2xl flex flex-col justify-between h-32">
          <div className="flex items-center space-x-2 text-gray-400">
            <Sun className="w-4 h-4" />
            <span className="text-sm">UV Index</span>
          </div>
          <div>
             <span className="text-2xl font-semibold">{uvi}</span>
             <span className="text-sm ml-1 text-gray-400">uv</span>
          </div>
          <span className="text-xs text-gray-400">Moderate UV</span>
        </div>

        {/* Visibility */}
        <div className="bg-[#2c2c31] p-4 rounded-2xl flex flex-col justify-between h-32">
          <div className="flex items-center space-x-2 text-gray-400">
            <Eye className="w-4 h-4" />
            <span className="text-sm">Visibility</span>
          </div>
          <div>
             <span className="text-2xl font-semibold">{visibility}</span>
             <span className="text-sm ml-1 text-gray-400">km</span>
          </div>
          <span className="text-xs text-gray-400"></span>
        </div>

        {/* Sunset */}
        <div className="bg-[#2c2c31] p-4 rounded-2xl flex items-center space-x-4 h-32">
          <Sunset className="w-8 h-8 text-orange-500" />
          <div className="flex flex-col">
            <span className="text-sm text-gray-400">Sunset</span>
            <span className="text-lg font-semibold">{sunset}</span>
          </div>
        </div>

      </div>
    </div>
  );
}
