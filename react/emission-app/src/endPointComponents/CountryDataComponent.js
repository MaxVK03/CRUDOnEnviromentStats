import React, { useState } from 'react';
import api from '../api';

const CountryDataComponent = () => {
    const [countryName, setCountryName] = useState('');
    const [countryIsocode, setCountryIsocode] = useState('');
    const [yearid, setYearid] = useState('');
    const [timeFrame, setTimeFrame] = useState('');
    const [inCSV, setInCSV] = useState(false);
    const [countryData, setCountryData] = useState(null);

    const fetchCountryData = async () => {
        try {
            const response = await api.get('/country/data', {
                params: {
                    countryName,
                    countryIsocode,
                    yearid: yearid ? parseInt(yearid) : null,
                    timeFrame: timeFrame === '' ? null : timeFrame,
                    inCSV
                }
            });
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
            <button onClick={fetchCountryData}>Fetch Data</button>
            <button onClick={clearData}>Clear Data</button>
            {countryData && <pre>{JSON.stringify(countryData, null, 2)}</pre>}
        </div>
    );
};

export default CountryDataComponent;
