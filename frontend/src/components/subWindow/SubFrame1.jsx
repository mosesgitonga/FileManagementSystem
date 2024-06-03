// src/components/subwindows/SubWindowFrame1.jsx
import React from 'react';
import './SubFrame1.css';

const SubWindowFrame1 = () => {
  return (
    <div className="sub-window-frame1">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" preserveAspectRatio="none">
        <path d="M0,0 L50,0 L60,10 L150,10 L160,0 L200,0 L200,100 L0,100 Z" className="glowing-path" />
      </svg>
    </div>
  );
};

export default SubWindowFrame1;
