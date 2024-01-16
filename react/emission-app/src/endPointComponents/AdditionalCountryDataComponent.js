import React, { useState } from 'react';
import api from '../api';
import {formatData} from './DataFormatter';
import './Component.css';

const AdditionalCountryDataComponent = () => {
    const [countryName, setCountryName] = useState('');
    const [countryData, setCountryData] = useState(null);
    const [error, setError] = useState(null);

    const fetchCountryData = async () => {
        try {
            const response = await api.get('/country/addData/', {
                params: {
                    countryName
                }
            });
            console.log(response);
            setCountryData(response.data);
            setError(null);
        } catch (error) {
            setCountryData(null);
            setError(error.response ? error.response.data : {detail : error.detail});
            const statusCode = error.response ? error.response.status : 500
            setError(prevError => ({
                ...prevError,
                status : statusCode
            }));
            console.error('Error fetching country data:', error);
        }
    };

    const clearData = () => {
        setCountryData(null);
    };

    return (
        <div className="Data-component">
            <h2>Fetch Additional Country Data</h2>
            <input
                type="text"
                value={countryName}
                onChange={(e) => setCountryName(e.target.value)}
                placeholder="Country Name"
            />
            <button onClick={fetchCountryData}>Fetch Data</button>
            <button onClick={clearData}>Clear Data</button>
            {error && (
                <div style={{ color: 'red', marginTop: '10px' }}>
                    <strong>Error: {error.detail}</strong>
                    {error.status && <p> Status Code: {error.status}</p>}
                </div>
            )}
            {countryData && <pre className='Data-data'>{formatData(countryData, 'JSON')}</pre>}
        </div>
    );
};

export default AdditionalCountryDataComponent;
