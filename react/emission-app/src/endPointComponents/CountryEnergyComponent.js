import React, { useState } from 'react';
import api from '../api';
import formatData from './DataFormatter';
import './Component.css';

const FetchCountryEnergyComponent = () => {
    const [dataType, setDataType] = useState('JSON');
    const [numCountries, setNoCountries] = useState('');
    const [yearid, setYearid] = useState('');
    const [page, setPage] = useState('');
    const [inCSV, setInCSV] = useState(false);
    const [energyData, setEnergyData] = useState(null);
    const [error, setError] = useState(null);

    const fetchEnergyData = async () => {
        try {
            const response = await api.get('/country/energy/', { 
                params: {
                    numCountries: numCountries ? parseInt(numCountries) : null,
                    yearid: yearid ? parseInt(yearid) : null,
                    page: page ? parseInt(page) : null,
                    inCSV
                }
            });
            if (response.headers.getContentType().includes('/csv')) {
              setDataType('CSV');
            } else {
              setDataType('JSON');
            }
            setEnergyData(response.data);
            setError(null);
        } catch (error) {
            setEnergyData(null);
            setError(error.response ? error.response.data : {detail : error.detail});
            const statusCode = error.response ? error.response.status : 500
            setError(prevError => ({
                ...prevError,
                status : statusCode
            }));
        }
    };

    const clearData = () => {
        setEnergyData(null);
    };

    return (
        <div className='Data-component'>
            <h2>Fetch Country Energy Data</h2>
            <div>
                <input
                    type="number"
                    value={numCountries}
                    onChange={(e) => setNoCountries(e.target.value)}
                    placeholder="Number of Countries"
                />
                <input
                    type="number"
                    value={yearid}
                    onChange={(e) => setYearid(e.target.value)}
                    placeholder="Year ID"
                />
                <input
                    type="number"
                    value={page}
                    onChange={(e) => setPage(e.target.value)}
                    placeholder="Page"
                />
                <label>
                    <input
                        type="checkbox"
                        checked={inCSV}
                        onChange={(e) => setInCSV(e.target.checked)}
                    />
                    in CSV
                </label>
                <button onClick={fetchEnergyData}>Fetch Data</button>
                <button onClick={clearData}>Clear Data</button>
            </div>
            {error && (
                <div style={{ color: 'red', marginTop: '10px' }}>
                    <strong>Error: {error.detail}</strong>
                    {error.status && <p> Status Code: {error.status}</p>}
                </div>
            )}
            {energyData && <div className='Data-data'>{formatData(energyData, dataType)}</div>}
        </div>
    );
};

export default FetchCountryEnergyComponent;
