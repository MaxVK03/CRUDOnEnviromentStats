import React, { useState } from 'react';
import api from '../api';

const FetchCountryEnergyComponent = () => {
    const [numCountries, setNoCountries] = useState('');
    const [yearid, setYearid] = useState('');
    const [page, setPage] = useState('');
    const [inCSV, setInCSV] = useState(false);
    const [energyData, setEnergyData] = useState(null);

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
            setEnergyData(response.data);
        } catch (error) {
            console.error('Error fetching energy data:', error);
            setEnergyData(error.response)
        }
    };

    return (
        <div>
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
            </div>
            {energyData && <pre>{JSON.stringify(energyData, null, 2)}</pre>}
        </div>
    );
};

export default FetchCountryEnergyComponent;
