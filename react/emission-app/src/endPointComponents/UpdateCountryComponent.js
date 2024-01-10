import React, { useState } from 'react';
import api from '../api'; // Make sure this points to your API configuration

const UpdateCountryComponent = () => {
    const [updateData, setUpdateData] = useState({
        countryName: '',
        iso: '',
        country: '',
        year: '',
        iso_code: '',
        population: '',
        gdp: '',
        co2: '',
        energy_per_capita: '',
        energy_per_gdp: '',
        methane: '',
        nitrous_oxide: '',
        share_of_temperature_change_from_ghg: '',
        temperature_change_from_ch4: '',
        temperature_change_from_co2: '',
        temperature_change_from_ghg: '',
        temperature_change_from_n2o: '',
        total_ghg: ''
    });
    const [responseCode, setResponseCode] = useState(null);

    const handleInputChange = (e) => {
        setUpdateData({ ...updateData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const { countryName, iso, ...countryData } = updateData;
        try {
            const response = await api.put('/country', { countryName, iso, countryData });
            setResponseCode(response.status);
            console.log('Country data updated successfully', response.data);
        } catch (error) {
            setResponseCode(error.response ? error.response.status : 500);
            console.error('Error updating country data:', error);
        }
    };

    return (
        <div>
            <h2>Update Country Data</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="countryName"
                    value={updateData.countryName}
                    onChange={handleInputChange}
                    placeholder="Country Name"
                />
                <input
                    type="text"
                    name="iso"
                    value={updateData.iso}
                    onChange={handleInputChange}
                    placeholder="ISO Code"
                />
                {/* Add other fields here */}
                {Object.keys(updateData).map(key => (
                    key !== 'countryName' && key !== 'iso' && (
                        <div key={key}>
                            <label>{key}</label>
                            <input
                                type="text"
                                name={key}
                                value={updateData[key]}
                                onChange={handleInputChange}
                            />
                        </div>
                    )
                ))}
                <button type="submit">Update Country</button>
            </form>
            {responseCode !== null && <p>Response Code: {responseCode}</p>}
        </div>
    );
};

export default UpdateCountryComponent;
