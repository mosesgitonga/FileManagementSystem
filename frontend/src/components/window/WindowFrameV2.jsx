// src/components/window/WindowFrame.jsx
import React from 'react';
import './WindowFrame.css';

const WindowFrame = () => {
  return (
    <div className="window-frame">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap" rel="stylesheet"></link>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" preserveAspectRatio="none">
        {/* Top Left */}
        <path d="M0,0 L30,0 L40,20 L70,20 L80,0 L200,0 L210,20 L240,20 L250,0 L350,0" className="glowing-path" />
        {/* Top Right */}
        <path d="M1000,0 L970,0 L960,20 L930,20 L920,0 L800,0 L790,20 L760,20 L750,0 L650,0" className="glowing-path" />
        {/* Bottom Right */}
        <path d="M1000,500 L970,500 L960,480 L930,480 L920,500 L800,500 L790,480 L760,480 L750,500 L650,500" className="glowing-path" />
        {/* Bottom Left */}
        <path d="M0,500 L30,500 L40,480 L70,480 L80,500 L200,500 L210,480 L240,480 L250,500 L350,500" className="glowing-path" />
        {/* Left Side */}
        <path d="M0,0 L0,30 L20,40 L20,70 L0,80 L0,200 L20,210 L20,240 L0,250 L0,350" className="glowing-path" />
        {/* Right Side */}
        <path d="M1000,0 L1000,30 L980,40 L980,70 L1000,80 L1000,200 L980,210 L980,240 L1000,250 L1000,350" className="glowing-path" />
      </svg>
    </div>
  );
};

export default WindowFrame;
