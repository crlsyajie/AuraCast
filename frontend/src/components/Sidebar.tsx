import { Menu, LayoutDashboard, Map, Calendar, Bell, Settings, HelpCircle } from "lucide-react";

export function Sidebar() {
  return (
    <aside className="w-16 flex flex-col items-center py-8 bg-[#1c1c21] rounded-[2rem] h-[calc(100vh-2rem)]">
      <div className="flex-1 flex flex-col gap-8 text-gray-400">
        <Menu className="w-6 h-6 hover:text-white cursor-pointer" />
        <div className="bg-[#2c2c31] p-2 rounded-xl text-white">
          <LayoutDashboard className="w-6 h-6 cursor-pointer" />
        </div>
        <Map className="w-6 h-6 hover:text-white cursor-pointer" />
        <Calendar className="w-6 h-6 hover:text-white cursor-pointer" />
        <Bell className="w-6 h-6 hover:text-white cursor-pointer" />
        <Settings className="w-6 h-6 hover:text-white cursor-pointer" />
      </div>
      <HelpCircle className="w-6 h-6 text-gray-400 hover:text-white cursor-pointer mb-4" />
    </aside>
  );
}
