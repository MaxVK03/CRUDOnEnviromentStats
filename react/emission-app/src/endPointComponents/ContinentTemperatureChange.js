import React, { useState } from 'react';
import api from '../api';
import formatData from './DataFormatter';

const ContinentTemperatureChange = () => {
    const [dataType, setDataType] = useState('JSON');
    const [continent, setContinent] = useState('');
    const [year, setYear] = useState('');
    const [inCSV, setInCSV] = useState(false);
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    const fetchData = async () => {
        try {
            const parsedYear = year ? parseInt(year) : null;
            const response = await api.get('/continent/temperatureChange', { params: { continent, year: parsedYear, inCSV } });
            if (response.headers.getContentType().includes('/csv')) {
              setDataType('CSV');
            } else {
              setDataType('JSON');
            }
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
        <div>
            <h2>Continent Temperature Change</h2>
            <input 
                type="text" 
                value={continent} 
                onChange={(e) => setContinent(e.target.value)} 
                placeholder="Continent"
            />
            <input 
                type="number" 
                value={year} 
                onChange={(e) => setYear(e.target.value)} 
                placeholder="Year" 
            />
            <label>
                <input 
                    type="checkbox" 
                    checked={inCSV} 
                    onChange={(e) => setInCSV(e.target.checked)}
                />
                in CSV
            </label>
            <button onClick={fetchData}>Fetch Data</button>
            <button onClick={clearData}>Clear Data</button>
            {error && (
                <div style={{ color: 'red', marginTop: '10px' }}>
                    <strong>Error: {error.detail}</strong>
                    {error.status && <p> Status Code: {error.status}</p>}
                </div>
            )}
            {data && (<div> {formatData(data, dataType)} </div>)}
        </div>
    );
};

export default ContinentTemperatureChange;
