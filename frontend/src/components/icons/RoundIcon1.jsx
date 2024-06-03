// src/components/icons/RoundIcon1.jsx
import React from 'react';
import './RoundIcon1.css';

const RoundIcon1 = () => {
  return (
    <div className="round-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" preserveAspectRatio="xMidYMid meet">
        {/* Outer glowing circle */}
        <circle cx="100" cy="100" r="90" className="icon-outer-circle" />

        {/* Inner circle */}
        <circle cx="100" cy="100" r="80" className="icon-inner-circle" />

        {/* Text inside the circle */}
        <text x="100" y="110" textAnchor="middle" dominantBaseline="middle" className="icon-text">
          Organization X
        </text>

        {/* Futuristic path */}
        <path d="M100 10 L100 100" className="icon-path" />
      </svg>
    </div>
  );
};

export default RoundIcon1;
