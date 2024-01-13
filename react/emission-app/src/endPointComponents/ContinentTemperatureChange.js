import React, { useState } from 'react';
import api from '../api';

const ContinentTemperatureChange = () => {
    const [continent, setContinent] = useState('');
    const [year, setYear] = useState('');
    const [inCSV, setInCSV] = useState(false);
    const [data, setData] = useState(null);

    const fetchData = async () => {
        try {
            const parsedYear = year ? parseInt(year) : null;
            const response = await api.get('/continent/temperatureChange', { params: { continent, year: parsedYear, inCSV } });
            setData(response.data);
        } catch (error) {
            console.error('Error:', error);
            setData(error.response);
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
            {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
        </div>
    );
};

export default ContinentTemperatureChange;
