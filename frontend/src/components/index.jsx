// src/components/LandingPage.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import WindowFrame from './window/WindowFrame';
import './index.css';
import WindowFrame2 from './window/WindowFrameV2';

const LandingPage = () => {
  return (
    <div className="landing-page">
        <WindowFrame />
      <h1>Welcome to the Sci-Fi File Management System</h1>
      <p>This is a futuristic file management system.</p>
      <div class='buttons'>
        <Link to="/signup">
            <button>Sign Up</button>
        </Link>
        <Link to="/login">
            <button>Login</button>
        </Link>
      </div>
    </div>
  );
};

export default LandingPage;
