import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Dropdown } from 'react-bootstrap';
import { BsThreeDotsVertical } from 'react-icons/bs';
import styles from './SettingsPage.module.css';
import WindowFrame2 from '../window/WindowFrameV2';
import api from '../../api/axios';

const SettingsPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ name: '', description: '' });
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState({ text: '', type: '' });
  const [showForm, setShowForm] = useState(false);
  const [departments, setDepartments] = useState([]);
  const [allUsers, setAllUsers] = useState([]);
  const [deptUsers, setDeptUsers] = useState([]);
  const [selectedDeptId, setSelectedDeptId] = useState(null);
  const [selectedUserId, setSelectedUserId] = useState(null);

  useEffect(() => {
    const fetchAllUsers = async () => {
      try {
        const response = await api.get('api/users/all');
        setAllUsers(response.data);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    const fetchDepartments = async () => {
      try {
        const response = await api.get('api/dept/list/all');
        setDepartments(response.data);
      } catch (error) {
        console.error('Error fetching departments:', error);
      }
    };

    fetchAllUsers();
    fetchDepartments();
  }, []);

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

  const handleDeptClick = async (deptId) => {
    setSelectedDeptId(deptId);
    try {
      const response = await api.get(`api/users/dept/${deptId}`);
      setDeptUsers(response.data);
    } catch (error) {
      console.error(`Error fetching users in dept id -> ${deptId}:`, error);
      setDeptUsers([]);
    }
  };

  const handleUserClick = (userId) => {
    setSelectedUserId(userId);
  };

  const handleAddToDept = async (userId) => {
    if (!userId || !selectedDeptId) return;
    try {
      const response = await api.post(`api/dept/add_user/${selectedDeptId}/${userId}`);
      setMessage({ text: response.data.message, type: 'success' });
      handleDeptClick(selectedDeptId); // Refresh department users
    } catch (error) {
      setMessage({ text: 'Failed to add to department', type: 'error' });
    }
  };

  const handleAddAdmin = async () => {
    if (!selectedUserId) {
      setMessage({ text: 'No user selected', type: 'error' });
      return;
    }

    try {
      const userType = 'admin';
      const response = await api.post(`api/users/type/update/${selectedUserId}`, { user_type: userType });
      setMessage({ text: response.data.message, type: 'success' });
    } catch (error) {
      setMessage({ text: 'Failed to add admin', type: 'error' });
    }
  };

  return (
    <div className={styles.settingsPage}>
      <WindowFrame2 />
      <div className={styles.content}>
        <h1 className="dept-head">Settings Page</h1>
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
                  onClick={() => handleDeptClick(dept.id)}
                  className={selectedDeptId === dept.id ? styles.selected : ''}
                >
                  {dept.name}
                </li>
              ))}
            </ul>
          </div>
          <div className={styles.users}>
            <h2>Deparment Members</h2>
            {deptUsers.length === 0 ? (
              <p>No users in this department</p>
            ) : (
              <ul>
                {deptUsers.map((user) => (
                  <li key={user.id}
                    onClick={() => handleUserClick(user.id)}
                    className={selectedUserId === user.id ? styles.selected : ''}
                    >
                      {user.first_name} {user.second_name} - {user.user_type}
                   
                    <Dropdown>
                      <Dropdown.Toggle as={BsThreeDotsVertical} />
                      <Dropdown.Menu>
                        <Dropdown.Item className="addAsAdmin" onClick={() => handleAddAdmin()}>Add as Admin</Dropdown.Item>
                        <Dropdown.Item className='addToDept' onClick={() => handleAddToDept(user.id)}>Add to Dept</Dropdown.Item>
                        {/* Add more actions here */}
                      </Dropdown.Menu>
                    </Dropdown>
                 

                  </li>
                ))}
              </ul>
            )}
          </div>
          <div className={styles.allUsers}>
            <h2>All Users</h2>
            {allUsers.length === 0 ? (
              <p>No users available</p>
            ) : (
              <ul>
                {allUsers.map((user) => (
                  <li key={user.id} className={selectedUserId === user.id ? styles.selected : ''}
                  >
                    <span onClick={() => handleUserClick(user.id)}>
                      {user.first_name} {user.second_name} - {user.user_type}
                    </span>
                    <Dropdown>
                      <Dropdown.Toggle as={BsThreeDotsVertical} />
                      <Dropdown.Menu>
                        <Dropdown.Item onClick={() => handleAddAdmin()}>Add as Admin</Dropdown.Item>
                        <Dropdown.Item onClick={() => handleAddToDept(user.id)}>Add to Dept</Dropdown.Item>
                        {/* Add more actions here */}
                      </Dropdown.Menu>
                    </Dropdown>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
