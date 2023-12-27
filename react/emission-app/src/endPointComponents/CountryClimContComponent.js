import React, { useState } from 'react';
import api from '../api';

const FetchCountryClimContComponent = () => {
    const [params, setParams] = useState({
        noCountries: '',
        yearid: '',
        sort: '',
        inCSV: false
    });
    const [climContData, setClimContData] = useState(null);

    const handleInputChange = (e) => {
        setParams({ ...params, [e.target.name]: e.target.value });
    };

    const handleCheckboxChange = (e) => {
        setParams({ ...params, inCSV: e.target.checked });
    };

    const fetchClimContData = async () => {
        try {
            const response = await api.get('/country/climCont/', { params });
            setClimContData(response.data);
        } catch (error) {
            console.error('Error fetching climate data:', error);
        }
    };

    return (
        <div>
            <h2>Fetch Climate Data by Continent</h2>
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
                    type="text"
                    name="sort"
                    value={params.sort}
                    onChange={handleInputChange}
                    placeholder="Sort"
                />
                <label>
                    <input
                        type="checkbox"
                        checked={params.inCSV}
                        onChange={handleCheckboxChange}
                    />
                    in CSV
                </label>
                <button onClick={fetchClimContData}>Fetch Data</button>
            </div>
            {climContData && <pre>{JSON.stringify(climContData, null, 2)}</pre>}
        </div>
    );
};

export default FetchCountryClimContComponent
