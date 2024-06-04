import React, { useEffect } from 'react';
import './WindowFrame.css';

const WindowFrame = () => {
  return (
    <div className="window-frame">
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap" rel="stylesheet"></link>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -1 200 100" preserveAspectRatio="none">
        <path className="glowing-path" d="M1,1 L199,1 L199,30 L180,35 L199,40 L199,70 L150,80 L199,90 L199,99 L1,99 Z" fill="none" stroke="#00ff00" strokeWidth="2"/>
        <path className="glowing-path" d="M1,1 L1,99 L50,90 L1,80 L1,40 L20,35 L1,30 Z" fill="none" stroke="#00ff00" strokeWidth="2"/>
      </svg>
    </div>
  );
};

export default WindowFrame;

