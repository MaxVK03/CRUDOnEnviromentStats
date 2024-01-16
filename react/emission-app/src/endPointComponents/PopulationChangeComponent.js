import React, { useState } from 'react';
import api from '../api';
import {formatFloat} from './DataFormatter';
import './Component.css';

const ContinentTemperatureChange = () => {
    const [continent, setContinent] = useState('');
    const [startYear, setStartYear] = useState('');
    const [endYear, setEndYear] = useState('');
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    const fetchData = async () => {
        try {
            const parsedStartYear = startYear ? parseInt(startYear) : null;
            const parsedEndYear = endYear ? parseInt(endYear) : null;

            const response = await api.get('/continent/popChange', { params: { continent, startYear: parsedStartYear,
            endYear: parsedEndYear} });
            setData(response.data);
            setError(null);
        } catch (error) {
            setData(null);
            setError(error.response ? error.response.data : {detail : error.detail});
            const statusCode = error.response ? error.response.status : 500
            setError(prevError => ({
                ...prevError,
                status : statusCode
            }));
        }
    };

    const clearData = () => {
        setData(null);
    };

    return (
        <div className='Data-component'>
            <h2>Continent Population Change Data</h2>
            <input
                type="text"
                value={continent}
                onChange={(e) => setContinent(e.target.value)}
                placeholder="Continent"
            />
            <input
                type="number"
                value={startYear}
                onChange={(e) => setStartYear(e.target.value)}
                placeholder="Start Year"
            />
            <input
                type="number"
                value={endYear}
                onChange={(e) => setEndYear(e.target.value)}
                placeholder="End Year"
            />

            <button onClick={fetchData}>Fetch Data</button>
            <button onClick={clearData}>Clear Data</button>
            {error && (
                <div style={{ color: 'red', marginTop: '10px' }}>
                    <strong>Error: {error.detail}</strong>
                    {error.status && <p> Status Code: {error.status}</p>}
                </div>
            )}
            {data && (<div className='Data-data'> {formatFloat(data)} </div>)}
        </div>
    );
};

export default ContinentTemperatureChange;
