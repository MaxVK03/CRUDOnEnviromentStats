import React, { useState } from 'react';
import api from '../api';
import {formatData} from './DataFormatter';
import './Component.css';

const FetchCountryEmissionsComponent = () => {
    const [dataType, setDataType] = useState('JSON');
    const [countryName, setCountryName] = useState('');
    const [countryIsocode, setCountryIsocode] = useState('');
    const [yearid, setYearid] = useState('');
    const [timeFrame, setTimeFrame] = useState('');
    const [inCSV, setInCSV] = useState(false);
    const [emissionData, setEmissionData] = useState(null);
    const [error, setError] = useState(null);


    const fetchEmissions = async () => {
        try {
            const response = await api.get('/country/emissions', { 
                params: {
                    countryName,
                    countryIsocode,
                    yearid: yearid ? parseInt(yearid) : null,
                    timeFrame: timeFrame === '' ? null : timeFrame,
                    inCSV
                }
            });
            if (response.headers.getContentType().includes('/csv')) {
              setDataType('CSV');
            } else {
              setDataType('JSON');
            }
            setEmissionData(response.data);
            setError(null);
        } catch (error) {
            setEmissionData(null);
            setError(error.response ? error.response.data : {detail : error.detail});
            const statusCode = error.response ? error.response.status : 500
            setError(prevError => ({
                ...prevError,
                status : statusCode
            }));
        }
    };

    const clearData = () => {
        setEmissionData(null);
    };

    return (
        <div className='Data-component'>
            <h2>Fetch Country Emissions Data</h2>
            <input
                type="text"
                value={countryName}
                onChange={(e) => setCountryName(e.target.value)}
                placeholder="Country Name"
            />
            <input
                type="text"
                value={countryIsocode}
                onChange={(e) => setCountryIsocode(e.target.value)}
                placeholder="Country ISO Code"
            />
            <input
                type="number"
                value={yearid}
                onChange={(e) => setYearid(e.target.value)}
                placeholder="Year ID"
            />
            <input
                type="text"
                value={timeFrame}
                onChange={(e) => setTimeFrame(e.target.value)}
                placeholder="Time Frame"
            />
            <label>
                <input
                    type="checkbox"
                    checked={inCSV}
                    onChange={(e) => setInCSV(e.target.checked)}
                />
                in CSV
            </label>
            <button onClick={fetchEmissions}>Fetch Data</button>
            <button onClick={clearData}>Clear Data</button>
            {error && (
                <div style={{ color: 'red', marginTop: '10px' }}>
                    <strong>Error: {error.detail}</strong>
                    {error.status && <p> Status Code: {error.status}</p>}
                </div>
            )}
            {emissionData && <div className='Data-data'>{formatData(emissionData, dataType)}</div>}
        </div>
    );
};

export default FetchCountryEmissionsComponent;
