import React, { useState } from 'react';
import api from '../api'; // Ensure this points to your API configuration

const FetchCountryEnergyComponent = () => {
    const [params, setParams] = useState({
        noCountries: '',
        yearid: '',
        page: '',
        inCSV: false
    });
    const [energyData, setEnergyData] = useState(null);

    const handleInputChange = (e) => {
        setParams({ ...params, [e.target.name]: e.target.value });
    };

    const handleCheckboxChange = (e) => {
        setParams({ ...params, inCSV: e.target.checked });
    };

    const fetchEnergyData = async () => {
        try {
            const response = await api.get('/country/energy/', { params });
            setEnergyData(response.data);
        } catch (error) {
            console.error('Error fetching energy data:', error);
        }
    };

    return (
        <div>
            <h2>Fetch Country Energy Data</h2>
            <div>
                <input
                    type="number"
                    name="noCountries"
                    value={params.noCountries}
                    onChange={handleInputChange}
                    placeholder="Number of Countries"
                />
                <input
                    type="number"
                    name="yearid"
                    value={params.yearid}
                    onChange={handleInputChange}
                    placeholder="Year ID"
                />
                <input
                    type="number"
                    name="page"
                    value={params.page}
                    onChange={handleInputChange}
                    placeholder="Page"
                />
                <label>
                    <input
                        type="checkbox"
                        checked={params.inCSV}
                        onChange={handleCheckboxChange}
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
