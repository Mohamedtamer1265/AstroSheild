import React, { createContext, useContext, useState, useEffect } from 'react';

const AccessibilityContext = createContext();

export const useAccessibility = () => {
  const context = useContext(AccessibilityContext);
  if (!context) {
    throw new Error('useAccessibility must be used within an AccessibilityProvider');
  }
  return context;
};

export const AccessibilityProvider = ({ children }) => {
  const [colorBlindMode, setColorBlindMode] = useState(false);
  const [colorBlindType, setColorBlindType] = useState('protanopia'); // protanopia, deuteranopia, tritanopia

  // Load settings from localStorage
  useEffect(() => {
    const savedColorBlindMode = localStorage.getItem('colorBlindMode') === 'true';
    const savedColorBlindType = localStorage.getItem('colorBlindType') || 'protanopia';
    
    setColorBlindMode(savedColorBlindMode);
    setColorBlindType(savedColorBlindType);
  }, []);

  // Save settings to localStorage
  useEffect(() => {
    localStorage.setItem('colorBlindMode', colorBlindMode.toString());
    localStorage.setItem('colorBlindType', colorBlindType);
  }, [colorBlindMode, colorBlindType]);

  // Apply color blind CSS class to body
  useEffect(() => {
    const body = document.body;
    
    if (colorBlindMode) {
      // Remove any existing filter
      body.classList.remove('protanopia-filter', 'deuteranopia-filter', 'tritanopia-filter');
      
      // Apply the selected filter
      body.classList.add(`${colorBlindType}-filter`);
    } else {
      // Remove all filters
      body.classList.remove('protanopia-filter', 'deuteranopia-filter', 'tritanopia-filter');
    }
    
    return () => {
      // Cleanup on unmount
      body.classList.remove('protanopia-filter', 'deuteranopia-filter', 'tritanopia-filter');
    };
  }, [colorBlindMode, colorBlindType]);

  const toggleColorBlindMode = () => {
    setColorBlindMode(!colorBlindMode);
  };

  const changeColorBlindType = (type) => {
    setColorBlindType(type);
  };

  // Get color blind friendly colors
  const getAccessibleColors = () => {
    if (!colorBlindMode) {
      return {
        success: 'bg-green-600',
        warning: 'bg-yellow-600',
        danger: 'bg-red-600',
        info: 'bg-blue-600',
        successText: 'text-green-400',
        warningText: 'text-yellow-400',
        dangerText: 'text-red-400',
        infoText: 'text-blue-400',
        successBorder: 'border-green-500',
        warningBorder: 'border-yellow-500',
        dangerBorder: 'border-red-500',
        infoBorder: 'border-blue-500'
      };
    }
    
    // Color blind friendly alternatives using distinct colors and patterns
    return {
      success: 'bg-blue-600', // Use blue instead of green
      warning: 'bg-orange-600', // Use orange instead of yellow  
      danger: 'bg-purple-600', // Use purple instead of red
      info: 'bg-cyan-600', // Use cyan for info
      successText: 'text-blue-400',
      warningText: 'text-orange-400',
      dangerText: 'text-purple-400',
      infoText: 'text-cyan-400',
      successBorder: 'border-blue-500',
      warningBorder: 'border-orange-500',
      dangerBorder: 'border-purple-500',
      infoBorder: 'border-cyan-500'
    };
  };

  const value = {
    colorBlindMode,
    colorBlindType,
    toggleColorBlindMode,
    changeColorBlindType,
    getAccessibleColors
  };

  return (
    <AccessibilityContext.Provider value={value}>
      {children}
    </AccessibilityContext.Provider>
  );
};