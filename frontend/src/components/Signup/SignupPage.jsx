// src/components/SignupPage.js
import React from 'react';
import './SignupPage.css';
import WindowFrame from '../window/WindowFrame'; 
const SignupPage = () => {
  return (
    <div className="signup-page">
      <WindowFrame />
      <div className="content">
        <h1>Sign Up</h1>
        <form>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input type="text" id="username" name="username" required />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input type="email" id="email" name="email" required />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input type="password" id="password" name="password" required />
          </div>
          <button type="submit">Sign Up</button>
        </form>
      </div>
    </div>
  );
};

export default SignupPage;
