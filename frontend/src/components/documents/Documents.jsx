import React, { useEffect, useState } from 'react';
import api from '../../api/axios';
import styles from './Documents.module.css';

const Documents = () => {
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await api.get('/api/docs/all', {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      setDocuments(response.data);
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const handleSendToDept = (docId) => {
    // Handle the logic for sending the document to a department
    console.log(`Send document ${docId} to department`);
  };

  const handleDownload = async (filename) => {
    try {
      const response = await api.get(`/api/docs/download/${filename}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        responseType: 'blob'  //handle binary data
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename); 
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading document:', error);
    }
  };

  return (
    <div className={styles.documents}>
      <h2>Documents</h2>
      <table className={styles.documentsTable}>
        <thead>
          <tr>
            <th>Filename</th>
            <th>Description</th>
            <th>Created At</th>
            <th>Send to Dept</th>
            <th>Download</th>
          </tr>
        </thead>
        <tbody>
          {documents.map((doc) => (
            <tr key={doc.id}>
              <td>{doc.filename}</td>
              <td>{doc.description}</td>
              <td>{new Date(doc.created_at).toLocaleString()}</td>
              <td>
                <button onClick={() => handleSendToDept(doc.id)}>Send to Dept</button>
              </td>
              <td>
                <button onClick={() => handleDownload(doc.filename)}>Download</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Documents;
