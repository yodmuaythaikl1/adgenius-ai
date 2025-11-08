import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button.jsx';
import { 
  LayoutDashboard, 
  Target, 
  Megaphone, 
  BarChart2, 
  Settings, 
  X,
  PieChart
} from 'lucide-react';

const Sidebar = ({ open, setOpen }) => {
  const location = useLocation();
  
  const menuItems = [
    { icon: <LayoutDashboard className="h-5 w-5" />, label: 'แดชบอร์ด', path: '/' },
    { icon: <PieChart className="h-5 w-5" />, label: 'แคมเปญ', path: '/campaigns' },
    { icon: <Target className="h-5 w-5" />, label: 'กลุ่มเป้าหมาย', path: '/targeting' },
    { icon: <Megaphone className="h-5 w-5" />, label: 'สร้างสรรค์โฆษณา', path: '/creative' },
    { icon: <BarChart2 className="h-5 w-5" />, label: 'วิเคราะห์ผล', path: '/analytics' },
    { icon: <Settings className="h-5 w-5" />, label: 'ตั้งค่า', path: '/settings' },
  ];
  
  return (
    <aside className={`sidebar ${open ? 'open' : 'closed'}`}>
      <div className="flex flex-col h-full p-4">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-xl font-bold text-primary">AdGenius AI</h1>
          <Button 
            variant="ghost" 
            size="icon" 
            className="md:hidden" 
            onClick={() => setOpen(false)}
          >
            <X className="h-5 w-5" />
          </Button>
        </div>
        
        <nav className="flex-1">
          <ul className="space-y-2">
            {menuItems.map((item, index) => (
              <li key={index}>
                <Link to={item.path}>
                  <Button
                    variant={location.pathname === item.path ? "default" : "ghost"}
                    className={`w-full justify-start ${location.pathname === item.path ? 'bg-primary text-primary-foreground' : ''}`}
                  >
                    {item.icon}
                    <span className="ml-2">{item.label}</span>
                  </Button>
                </Link>
              </li>
            ))}
          </ul>
        </nav>
        
        <div className="mt-auto pt-4 border-t border-border">
          <div className="text-sm text-muted-foreground">
            <p>AdGenius AI v0.1.0</p>
            <p>© 2025 AdGenius AI</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
