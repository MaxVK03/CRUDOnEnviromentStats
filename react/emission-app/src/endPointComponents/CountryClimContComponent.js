import React, { useState } from 'react';
import api from '../api';
import {formatData} from './DataFormatter';
import './Component.css';

const FetchCountryClimContComponent = () => {
    const [dataType, setDataType] = useState('JSON');
    const [noCountries, setNumCountries] = useState('');
    const [yearid, setYearid] = useState('');
    const [pastYears, setPastYears] = useState(''); 
    const [sort, setSort] = useState('');
    const [inCSV, setInCSV] = useState(false);
    const [climContData, setClimContData] = useState(null);
    const [error, setError] = useState(null);

    const fetchClimContData = async () => {
        try {
            const response = await api.get('/country/climCont/', { 
                params: {
                    noCountries: noCountries ? parseInt(noCountries) : null,
                    yearid: yearid ? parseInt(yearid) : null,
                    pastYears: pastYears ? parseInt(pastYears) : null,
                    sort: sort === '' ? null : sort,
                    inCSV
                }
            });
            if (response.headers.getContentType().includes('/csv')) {
              setDataType('CSV');
            } else {
              setDataType('JSON');
            }
            setClimContData(response.data);
            setError(null);
        } catch (error) {
            setClimContData(null);
            setError(error.response ? error.response.data : {detail : error.detail});
            const statusCode = error.response ? error.response.status : 500
            setError(prevError => ({
                ...prevError,
                status : statusCode
            }));
        }
    };

    const clearData = () => {
        setClimContData(null);
    };

    return (
        <div className='Data-component'>
            <h2>Fetch Contribution To Climate Change Data by Country</h2>
            <input
                type="number"
                value={noCountries}
                onChange={(e) => setNumCountries(e.target.value)}
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
                value={pastYears}
                onChange={(e) => setPastYears(e.target.value)}
                placeholder="Number of past years"
            />
            <input
                type="text"
                value={sort}
                onChange={(e) => setSort(e.target.value)}
                placeholder="Sort"
            />
            <label>
                <input
                    type="checkbox"
                    checked={inCSV}
                    onChange={(e) => setInCSV(e.target.checked)}
                />
                in CSV
            </label>
            <button onClick={fetchClimContData}>Fetch Data</button>
            <button onClick={clearData}>Clear Data</button>
            {error && (
                <div style={{ color: 'red', marginTop: '10px' }}>
                    <strong>Error: {error.detail}</strong>
                    {error.status && <p> Status Code: {error.status}</p>}
                </div>
            )}
            {climContData && <div className='Data-data'>{formatData(climContData, dataType)}</div>}
        </div>
    );
};

export default FetchCountryClimContComponent
