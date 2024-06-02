// src/components/WindowFrame.js
import React, { useEffect } from 'react';
import gsap from 'gsap';
import './WindowFrame.css';

const WindowFrame = () => {
  useEffect(() => {
    gsap.fromTo('.glowing-path', { opacity: 0.5 }, { opacity: 1, duration: 1.5, repeat: -1, yoyo: true });
    gsap.fromTo('.content', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 1.5, ease: 'power3.out' });
  }, []);

  return (
    <div className="window-frame">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" preserveAspectRatio="none">
        <path className="glowing-path" d="M1,1 L199,1 L199,30 L180,35 L199,40 L199,70 L150,80 L199,90 L199,99 L1,99 Z" fill="none" stroke="#00ff00" strokeWidth="2"/>
        <path className="glowing-path" d="M1,1 L1,99 L50,90 L1,80 L1,40 L20,35 L1,30 Z" fill="none" stroke="#00ff00" strokeWidth="2"/>
      </svg>
      <div className="content">
        <h1>Welcome to the Sci-Fi App</h1>
        <p>This is a futuristic file management system.</p>
        <button>Register</button>
        <button>Login</button>
      </div>
    </div>
  );
};

export default WindowFrame;

