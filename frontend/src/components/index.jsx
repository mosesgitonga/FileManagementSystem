// src/components/LandingPage.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import WindowFrame from './window/WindowFrame';
import './index.css';
import WindowFrame2 from './window/WindowFrameV2';
import SubWindowFrame2 from './subWindow/SubFrame2';

const LandingPage = () => {
  return (
    <div className="landing-page">
        <WindowFrame />
        <WindowFrame2 />
      <h1 className='index-head' >Galactic Document Management System</h1>
      <p>This is a futuristic document management system.</p>
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
