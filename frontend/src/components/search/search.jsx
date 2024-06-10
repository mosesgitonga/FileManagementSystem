/** 
import React, {useEffect, useState} from "react";
import api from '../../api/axios';

function Search() {
    const [query, serQuery] = useState('')
    const [results, setResults] = useState([]);

    useEffect(() => {
        const fetchResults = () => {
            if (query) {
                const response = api.get(`http://localhost:5000/search?query=${query}`)

                setResults(response.data)
            } else {
                setResults([])
            }
        }

    fetchResults()
    }, [query])

    const handleChange = (e) => {
        setQuery(e.target.value)
    };

    return (
        
    )

}
*/