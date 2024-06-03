// src/components/icons/RoundIcon2.jsx
import React from 'react';
import './RoundIcon2.css';

const RoundIcon2 = () => {
  return (
    <div className="round-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
        <circle cx="50" cy="50" r="40" className="icon-circle" />
        <circle cx="50" cy="50" r="30" className="icon-inner-circle" />
        <path d="M50 20 A30 30 0 0 1 80 50" className="icon-path" />
        <otherPaths></otherPaths>
      </svg>
    </div>
  );
};

export default RoundIcon2;
