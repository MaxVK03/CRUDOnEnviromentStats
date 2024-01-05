import React, { useState } from 'react';
import api from '../api';

const FetchCountryEmissionsComponent = () => {
    const [emissionParams, setEmissionParams] = useState({
        countryName: '',
        countryIsocode: '',
        yearid: '',
        timeFrame: '',
        inCSV: false
    });
    const [emissionData, setEmissionData] = useState(null);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setEmissionParams({ ...emissionParams, [name]: value });
    };

    const handleCheckboxChange = (e) => {
        setEmissionParams({ ...emissionParams, inCSV: e.target.checked });
    };

    const fetchEmissions = async () => {
        try {
            const response = await api.get('/country/emissions', { params: emissionParams });
            setEmissionData(response.data);
        } catch (error) {
            console.error('Error fetching emissions data:', error);
        }
    };

    return (
        <div>
            <h2>Fetch Country Emissions Data</h2>
            <div>
                <input
                    type="text"
                    name="countryName"
                    value={emissionParams.countryName}
                    onChange={handleInputChange}
                    placeholder="Country Name"
                />
                <input
                    type="text"
                    name="countryIsocode"
                    value={emissionParams.countryIsocode}
                    onChange={handleInputChange}
                    placeholder="Country ISO Code"
                />
                <input
                    type="number"
                    name="yearid"
                    value={emissionParams.yearid}
                    onChange={handleInputChange}
                    placeholder="Year ID"
                />
                <input
                    type="text"
                    name="timeFrame"
                    value={emissionParams.timeFrame}
                    onChange={handleInputChange}
                    placeholder="Time Frame"
                />
                <label>
                    <input
                        type="checkbox"
                        checked={emissionParams.inCSV}
                        onChange={handleCheckboxChange}
                    />
                    in CSV
                </label>
                <button onClick={fetchEmissions}>Fetch Data</button>
            </div>
            {emissionData && <pre>{JSON.stringify(emissionData, null, 2)}</pre>}
        </div>
    );
};

export default FetchCountryEmissionsComponent;
