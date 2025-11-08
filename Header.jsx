import React from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Menu, X, Bell, Settings, User } from 'lucide-react';

const Header = ({ setSidebarOpen }) => {
  return (
    <header className="header">
      <div className="flex items-center justify-between w-full">
        <div className="flex items-center">
          <Button 
            variant="ghost" 
            size="icon" 
            className="md:hidden mr-2" 
            onClick={() => setSidebarOpen(prev => !prev)}
          >
            <Menu className="h-5 w-5" />
          </Button>
          <h2 className="text-xl font-semibold">AdGenius AI</h2>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="icon">
            <Bell className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon">
            <Settings className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon">
            <User className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;
