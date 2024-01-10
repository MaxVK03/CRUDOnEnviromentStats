import React, { useState } from 'react';
import api from '../api'; // Make sure this points to your API configuration

const FetchEnergyDataComponent = () => {
    const [queryParams, setQueryParams] = useState({
        numCountries: '',
        yearid: '',
        page: '',
        inCSV: false
    });
    const [energyData, setEnergyData] = useState(null);
    const [responseCode, setResponseCode] = useState(null);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setQueryParams({ ...queryParams, [name]: value });
    };

    const handleCheckboxChange = (e) => {
        setQueryParams({ ...queryParams, inCSV: e.target.checked });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.get('/country/energy/', { params: queryParams });
            setResponseCode(response.status);
            setEnergyData(response.data);
        } catch (error) {
            setResponseCode(error.response ? error.response.status : 500);
            console.error('Error fetching energy data:', error);
        }
    };

    return (
        <div>
            <h2>Fetch Energy Data</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="number"
                    name="numCountries"
                    value={queryParams.numCountries}
                    onChange={handleInputChange}
                    placeholder="Number of Countries"
                />
                <input
                    type="number"
                    name="yearid"
                    value={queryParams.yearid}
                    onChange={handleInputChange}
                    placeholder="Year ID"
                />
                <input
                    type="number"
                    name="page"
                    value={queryParams.page}
                    onChange={handleInputChange}
                    placeholder="Page Number"
                />
                <label>
                    <input
                        type="checkbox"
                        name="inCSV"
                        checked={queryParams.inCSV}
                        onChange={handleCheckboxChange}
                    />
                    Download as CSV
                </label>
                <button type="submit">Fetch Data</button>
            </form>
            {responseCode !== null && <p>Response Code: {responseCode}</p>}
            {energyData && <pre>{JSON.stringify(energyData, null, 2)}</pre>}
        </div>
    );
};

export default FetchEnergyDataComponent;
