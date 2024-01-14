import React, { useState } from 'react';
import api from '../api';

const AdditionalCountryDataComponent = () => {
    const [countryName, setCountryName] = useState('');
    const [inCSV, setInCSV] = useState(false);
    const [countryData, setCountryData] = useState(null);

    const fetchCountryData = async () => {
        try {
            const response = await api.get('/country/addData/', {
                params: {
                    countryName,
                    inCSV
                }
            });
            console.log(response);
            setCountryData(response.data);
        } catch (error) {
            console.error('Error fetching country data:', error);
            setCountryData(error.response);
        }
    };

    const clearData = () => {
        setCountryData(null);
    };

    return (
        <div>
            <h2>Fetch Country Data</h2>
            <input
                type="text"
                value={countryName}
                onChange={(e) => setCountryName(e.target.value)}
                placeholder="Country Name"
            />
            <label>
                <input
                    type="checkbox"
                    checked={inCSV}
                    onChange={(e) => setInCSV(e.target.checked)}
                />
                in CSV
            </label>
            <button onClick={fetchCountryData}>Fetch Data</button>
            <button onClick={clearData}>Clear Data</button>
            {countryData && <pre>{JSON.stringify(countryData, null, 2)}</pre>}
        </div>
    );
};

export default AdditionalCountryDataComponent;
