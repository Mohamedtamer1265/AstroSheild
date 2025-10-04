import React, { useState } from 'react';
import { useAccessibility } from '../contexts/AccessibilityContext';

const AccessibilityToggle = () => {
  const {
    colorBlindMode,
    colorBlindType,
    toggleColorBlindMode,
    changeColorBlindType
  } = useAccessibility();
  
  const [isOpen, setIsOpen] = useState(false);

  const colorBlindTypes = [
    { id: 'protanopia', name: 'Protanopia', description: 'Red-Green (No L cones)' },
    { id: 'deuteranopia', name: 'Deuteranopia', description: 'Red-Green (No M cones)' },
    { id: 'tritanopia', name: 'Tritanopia', description: 'Blue-Yellow (No S cones)' }
  ];

  return (
    <div className="fixed top-4 right-4 z-50">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-600 hover:bg-gray-700 transition-colors shadow-lg"
        title="Accessibility Options"
      >
        <span>♿</span>
        <span className="text-sm">Accessibility</span>
        <span className={`transform transition-transform ${isOpen ? 'rotate-180' : ''}`}>
          ↓
        </span>
      </button>
      
      {isOpen && (
        <div className="absolute right-0 top-full mt-2 w-80 bg-gray-800 rounded-lg border border-gray-600 shadow-xl p-4">
          <h3 className="text-white font-semibold mb-3">Accessibility Settings</h3>
          
          {/* Color Blind Mode Toggle */}
          <div className="mb-4">
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={colorBlindMode}
                onChange={toggleColorBlindMode}
                className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"
              />
              <div>
                <span className="text-white text-sm font-medium">Color Blind Friendly Mode</span>
                <p className="text-gray-400 text-xs">Use alternative colors and patterns</p>
              </div>
            </label>
          </div>
          
          {/* Color Blind Type Selection */}
          {colorBlindMode && (
            <div className="mb-4">
              <label className="block text-white text-sm font-medium mb-2">
                Color Blindness Type:
              </label>
              <div className="space-y-2">
                {colorBlindTypes.map((type) => (
                  <label key={type.id} className="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="radio"
                      name="colorBlindType"
                      value={type.id}
                      checked={colorBlindType === type.id}
                      onChange={(e) => changeColorBlindType(e.target.value)}
                      className="w-3 h-3 text-blue-600 bg-gray-700 border-gray-600 focus:ring-blue-500"
                    />
                    <div>
                      <span className="text-white text-xs font-medium">{type.name}</span>
                      <p className="text-gray-400 text-xs">{type.description}</p>
                    </div>
                  </label>
                ))}
              </div>
            </div>
          )}
          
          {/* Info */}
          <div className="mt-4 p-3 bg-blue-900/30 rounded border border-blue-700">
            <p className="text-blue-200 text-xs">
              💡 This mode uses high-contrast colors and patterns to improve visibility for users with color vision deficiencies.
            </p>
          </div>
          
          {/* Close button */}
          <button
            onClick={() => setIsOpen(false)}
            className="w-full mt-3 px-3 py-2 text-sm bg-gray-700 text-white rounded hover:bg-gray-600 transition-colors"
          >
            Close
          </button>
        </div>
      )}
    </div>
  );
};

export default AccessibilityToggle;