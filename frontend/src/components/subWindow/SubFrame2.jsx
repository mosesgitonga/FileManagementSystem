// src/components/subwindows/SubWindowFrame2.jsx
import React from 'react';
import './SubWindowFrame2.css';

const SubWindowFrame2 = () => {
  return (
    <div className="sub-window-frame">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" preserveAspectRatio="none">
        <path d="M0,0 L50,0 L60,10 L150,10 L160,0 L200,0 L200,80 L190,90 L10,90 L0,80 Z" className="glowing-path" />
      </svg>
    </div>
  );
};

export default SubWindowFrame2;
