import React, { useState } from 'react';
import styles from './upload_doc.module.css';
import axios from 'axios';
import api from '../../api/axios';

const DocumentUpload = () => {
  const [showForm, setShowForm] = useState(false);
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState('');
  const [description, setDescription] = useState('');

  const toggleForm = () => {
    setShowForm(!showForm);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFilenameChange = (e) => {
    setFilename(e.target.value);
  };

  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      alert('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    if (filename) formData.append('filename', filename);
    if (description) formData.append('description', description);

    try {
      const response = await api.post('/api/docs/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });

      if (response.status === 200) {
        alert('File uploaded successfully');
        // Reset form
        setFile(null);
        setFilename('');
        setDescription('');
        setShowForm(false);
      } else {
        alert('Failed to upload file');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('An error occurred while uploading the file.');
    }
  };

  return (
    <div className={styles.documentUpload}>
      <button onClick={toggleForm} className={styles.uploadToggleBtn}>
        {showForm ? 'Hide Upload Form' : 'Upload Document'}
      </button>

      {showForm && (
        <div className={styles.uploadForm}>
          <form onSubmit={handleSubmit}>
            <div>
              <label htmlFor="file">Select File:</label>
              <input type="file" id="file" onChange={handleFileChange} />
            </div>
            <div>
              <label htmlFor="filename">Desired Filename (Optional):</label>
              <input
                type="text"
                id="filename"
                value={filename}
                onChange={handleFilenameChange}
              />
            </div>
            <div>
              <label htmlFor="description">Description (Optional):</label>
              <input
                type="text"
                id="description"
                value={description}
                onChange={handleDescriptionChange}
              />
            </div>
            <button type="submit" className={styles.uploadBtn}>Upload</button>
          </form>
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;
