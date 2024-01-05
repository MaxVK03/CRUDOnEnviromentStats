import React, { useState } from 'react';
import api from '../api';

const ContinentTemperatureChange = () => {
    const [continent, setContinent] = useState('');
    const [year, setYear] = useState('');
    const [timeFrame, setTimeFrame] = useState('');
    const [data, setData] = useState(null);

    const fetchData = async () => {
        try {
            const response = await api.get('/continent/temperatureChange', { params: { continent, year, timeFrame } });
            setData(response.data);
        } catch (error) {
            console.error('Error:', error);
            setData(null);
        }
    };

    return (
        <div>
            <h2>Continent Temperature Change</h2>
            <input type="text" value={continent} onChange={(e) => setContinent(e.target.value)} placeholder="Continent" />
            <input type="number" value={year} onChange={(e) => setYear(e.target.value)} placeholder="Year" />
            <input type="text" value={timeFrame} onChange={(e) => setTimeFrame(e.target.value)} placeholder="Time Frame" />
            <button onClick={fetchData}>Fetch Data</button>
            {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
        </div>
    );
};

export default ContinentTemperatureChange;
