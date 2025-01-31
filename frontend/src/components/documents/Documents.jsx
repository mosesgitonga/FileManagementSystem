import React, { useEffect, useState } from 'react';
import api from '../../api/axios';
import styles from './Documents.module.css';

const Documents = () => {
  const [documents, setDocuments] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [selectedDeptId, setSelectedDeptId] = useState('');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    fetchDocuments();
    fetchDepartments();
  }, []);

  useEffect(() => {
    const fetchResults = async () => {
      if (query) {
        try {
          const response = await api.get(`http://localhost:5000/api/search/dept/docs?query=${query}`);
          setResults(response.data);
        } catch (error) {
          console.error('Error fetching search results:', error);
        }
      } else {
        setResults([]);
      }
    };

    fetchResults();
  }, [query]);

  const fetchDocuments = async () => {
    try {
      const response = await api.get('/api/docs/all', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      setDocuments(response.data);
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const handleChange = (e) => {
    setQuery(e.target.value);
  };

  const fetchDepartments = async () => {
    try {
      const response = await api.get('/api/dept/list/all', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      setDepartments(response.data);
    } catch (error) {
      console.error('Error fetching departments:', error);
    }
  };

  const handleSendToDept = async (docId) => {
    if (!selectedDeptId) {
      alert('Please select a department to send the document.');
      return;
    }

    try {
      const response = await api.post(`/api/docs/share/${docId}/${selectedDeptId}`, null, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });

      if (response.status === 200) {
        console.log(`Document ${docId} sent to department ${selectedDeptId}`);
        fetchDocuments();
        setSelectedDeptId('');
        alert('Document sent successfully.');
      } else if (response.status === 403) {
        alert('Unauthorized: You do not have permission to send documents to this department.');
      } else {
        alert('Failed to send document: Something unexpected happened.');
      }
    } catch (error) {
      console.error('Error sending document to department:', error);
      alert('Error sending document: Internal server error.');
    }
  };

  const handleDownload = async (filename) => {
    try {
      const response = await api.get(`/api/docs/download/${filename}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        },
        responseType: 'blob'
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
      alert('Error downloading document: Internal server error.');
    }
  };

  const handleDeptChange = (event) => {
    setSelectedDeptId(event.target.value);
  };

  return (
    <div className={styles.documents}>
      <h2>Documents in your Department</h2>
      <input className={styles.search} type="text" value={query} onChange={handleChange} placeholder="Search..." />
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
          {(query ? results : documents).map((doc) => (
            <tr key={doc.id}>
              <td>{doc.filename}</td>
              <td>{doc.description}</td>
              <td>{new Date(doc.created_at).toLocaleString()}</td>
              <td>
                <div>
                  <select onChange={handleDeptChange} value={selectedDeptId}>
                    <option value="">Select Department</option>
                    {departments.map((dept) => (
                      <option key={dept.id} value={dept.id}>
                        {dept.name}
                      </option>
                    ))}
                  </select>
                  <button onClick={() => handleSendToDept(doc.id)}>Send</button>
                </div>
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
