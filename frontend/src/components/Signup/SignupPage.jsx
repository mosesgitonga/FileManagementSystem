import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import WindowFrame from '../window/WindowFrame'; 
import WindowFrame2 from '../window/WindowFrameV2';
import styles from './SignupPage.module.css';
import api from '../../api/axios'; 

const SignupPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    firstname: '',
    secondname: '',
    employee_id: '',
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
      const response = await api.post('api/auth/user/register', formData);
      setMessage(response.data.message);
      if (response.status === 201) {
        navigate('/login'); 
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
    <div className={styles.signupPage}>
      <WindowFrame />
      <WindowFrame2 />
      <div className={styles.content}>
        <h1 className='signup-head' >Sign Up</h1>
        {message && <p>{message}</p>}
        <form onSubmit={handleSubmit}>
          <div className={styles.formGroup}>
            <label htmlFor="firstname">First Name:</label>
            <input
              type="text"
              id="firstname"
              name="firstname"
              value={formData.firstname}
              onChange={handleChange}
              required
            />
            {errors.firstname && <span className={styles.error}>{errors.firstname}</span>}
          </div>
          <div className={styles.formGroup}>
            <label htmlFor="secondname">Second Name:</label>
            <input
              type="text"
              id="secondname"
              name="secondname"
              value={formData.secondname}
              onChange={handleChange}
              required
            />
            {errors.secondname && <span className={styles.error}>{errors.secondname}</span>}
          </div>
          <div className={styles.formGroup}>
            <label htmlFor="employee_id">Employee id:</label>
            <input
              type="text"
              id="employee_id"
              name="employee_id"
              value={formData.employee_id}
              onChange={handleChange}
              required
            />
            {errors.employee_id && <span className={styles.error}>{errors.employee_id}</span>}
          </div>
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
          <button type="submit">Sign Up</button>
        </form>
      </div>
    </div>
  );
};

export default SignupPage;
