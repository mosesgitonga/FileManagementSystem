import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import WindowFrame from '../window/WindowFrame'; 
import WindowFrame2 from '../window/WindowFrameV2';
import styles from './LoginPage.module.css'
import api from '../../api/axios'; 

const LoginPage = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: '',
        password: ''
      });
    const [errors, setErrors] = useState({});
    const [message, setMessage] = useState('');

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
    
        try {
          const response = await api.post('api/auth/user/login', formData);

          if (response.status === 200) {
            if (response.data.access_token) {
              localStorage.setItem('access_token', response.data.access_token); // Or sessionStorage.setItem('access_token', response.data.access_token);
              navigate('/dashboard'); 
            }
            console.log('access token not found in the response')
          }
        } catch (error) {
          if (error.response && error.response.data) {
            setErrors(error.response.data.errors || {});
            setMessage(error.response.data.message);
          } else {
            setMessage('An unexpected error occurred');
          }
        }
      };
    
    return (
    <div className={styles.loginPage}>
        <WindowFrame />
        <WindowFrame2 />
        <div className={styles.content}>
        {message && <p>{message}</p>}
        <h1 className="login-head" >Login</h1>

        <form onSubmit={handleSubmit}>
            <div className={styles.formGroup}>
            <label htmlFor="email">Email:</label>
            <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
            />
            {errors.email && <span className={styles.error}>{errors.email}</span>}
            </div>
            <div className={styles.formGroup}>
            <label htmlFor="password">Password:</label>
            <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
            />
            {errors.password && <span className={styles.error}>{errors.password}</span>}
            </div>
            <button type="submit">Login</button>
        </form>
        </div>
    </div>
    );
}

export default LoginPage;