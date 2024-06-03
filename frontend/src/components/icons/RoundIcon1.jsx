// src/components/icons/RoundIcon1.jsx
import React from 'react';
import './RoundIcon1.css';

const RoundIcon1 = () => {
  return (
    <div className="round-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
        <circle cx="50" cy="50" r="40" className="icon-circle" />
        <path d="M50 10 L50 50 L90 50" className="icon-path" />
        <otherPaths></otherPaths>
      </svg>
    </div>
  );
};

export default RoundIcon1;
