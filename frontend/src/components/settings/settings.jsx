import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import WindowFrame2 from '../window/WindowFrameV2';
import styles from './SettingsPage.module.css';
import api from '../../api/axios';

const SettingsPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ name: '', description: '' });
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState({ text: '', type: '' });
  const [showForm, setShowForm] = useState(false);
  const [departments, setDepartments] = useState([]);
  const [users, setUsers] = useState([]);
  const [selectedDeptId, setSelectedDeptId] = useState(null);
  const [selectedUserId, setSelectedUserId] = useState(null);

  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const response = await api.get('api/dept/list/all');
        setDepartments(response.data);
      } catch (error) {
        console.error('Error fetching departments:', error);
      }
    };

    fetchDepartments();
  }, []);

  useEffect(() => {
    const fetchUsers = async () => {
      if (selectedDeptId) {
        try {
          const response = await api.get(`api/users/list_users_dept/${selectedDeptId}`);
          setUsers(response.data);
        } catch (error) {
          console.error('Error fetching users:', error);
        }
      }
    };

    fetchUsers();
  }, [selectedDeptId]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setErrors({});
    setMessage({ text: '', type: '' });

    try {
      const response = await api.post('api/dept/create', formData);
      if (response.status === 201) {
        setMessage({ text: response.data.message, type: 'success' });
        setFormData({ name: '', description: '' });
        setShowForm(false);
        const updatedDepartments = await api.get('api/dept/list/all');
        setDepartments(updatedDepartments.data);
      }
    } catch (error) {
      if (error.response && error.response.data) {
        setErrors(error.response.data.errors || {});
        setMessage({ text: error.response.data.message, type: 'error' });
      } else {
        setMessage({ text: 'An unexpected error occurred', type: 'error' });
      }
    }
  };

  const handleAddAdmin = async () => {
    if (selectedUserId) {
      try {
        const response = await api.post(`api/users/add_admin/${selectedUserId}`);
        if (response.status === 200) {
          setMessage({ text: response.data.message, type: 'success' });
        }
      } catch (error) {
        setMessage({ text: 'An error occurred while adding admin.', type: 'error' });
        console.error('Error adding admin:', error);
      }
    }
  };

  return (
    <div className={styles.settingsPage}>

      <div className={styles.content}>
        <h1 className='dept-head'>Settings Page</h1>
        <button onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Hide Form' : 'Create Department'}
        </button>
        {showForm && (
          <div className={styles.dropdownForm}>
            <form onSubmit={handleSubmit}>
              <div className={styles.formGroup}>
                <label htmlFor="name">Department Name:</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                />
                {errors.name && <span className={styles.error}>{errors.name}</span>}
              </div>
              <div className={styles.formGroup}>
                <label htmlFor="description">Description:</label>
                <input
                  type="text"
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  required
                />
                {errors.description && <span className={styles.error}>{errors.description}</span>}
              </div>
              
              <button type="submit">Create Department</button>
            </form>
          </div>
        )}
        {message.text && (
          <p className={message.type === 'success' ? styles.successMessage : styles.errorMessage}>
            {message.text}
          </p>
        )}
        <div className={styles.lists}>
          <div className={styles.departments}>
            <h2>Departments</h2>
            <ul>
              {departments.map((dept) => (
                <li 
                  key={dept.id} 
                  onClick={() => setSelectedDeptId(dept.id)}
                  className={selectedDeptId === dept.id ? styles.selected : ''}
                >
                  {dept.name}
                </li>
              ))}
            </ul>
          </div>
          <div className={styles.users}>
            <h2>Users</h2>
            {selectedDeptId ? (
              users.length > 0 ? (
                <ul>
                  {users.map((user) => (
                    <li 
                      key={user.id} 
                      onClick={() => setSelectedUserId(user.id)}
                      className={selectedUserId === user.id ? styles.selected : ''}
                    >
                      {user.name}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No users available.</p>
              )
            ) : (
              <p>Select a department to view users.</p>
            )}
          </div>
        </div>
        {selectedUserId && (
          <button onClick={handleAddAdmin}>Add Selected User as Admin</button>
        )}
      </div>
    </div>
  );
};

export default SettingsPage;
