import React from 'react';
import { Heart, Leaf } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-ayur-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-6">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-12 h-12 bg-ayur-600 rounded-xl">
              <Leaf className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-ayur-800">AyurAI</h1>
              <p className="text-sm text-ayur-600">Ayurvedic Health Assistant</p>
            </div>
          </div>
          
          <div className="hidden md:flex items-center space-x-6">
            <div className="flex items-center space-x-2 text-ayur-700">
              <Heart className="w-5 h-5" />
              <span className="text-sm font-medium">Holistic Wellness</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;