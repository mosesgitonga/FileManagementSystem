import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ReactDOM from 'react-dom/client'
import WindowFrame from './components/window/WindowFrame';
import SignupPage from './components/Signup/SignupPage';
import './App.css'
import LandingPage from './components';
import Dashboard from './components/Dashboard';
import LoginPage from './components/login/login';
import SettingsPage from './components/settings/settings';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Router>
  </React.StrictMode>
)
