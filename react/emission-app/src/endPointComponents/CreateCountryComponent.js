import React, { useState } from 'react';
import api from '../api'; // Ensure this is the correct path to your API configuration

const CreateCountryComponent = () => {
    const [countryData, setCountryData] = useState({
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

    const handleInputChange = (e) => {
        setCountryData({ ...countryData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/country', countryData);
            console.log(response.data); // Handle the response appropriately
        } catch (error) {
            console.error('Error creating country data:', error);
        }
    };

    return (
        <div>
            <h2>Create Country Data</h2>
            <form onSubmit={handleSubmit}>
                {/* Generate input fields for each attribute */}
                {Object.keys(countryData).map((key) => (
                    <div key={key}>
                        <label>{key}</label>
                        <input
                            type="text"
                            name={key}
                            value={countryData[key]}
                            onChange={handleInputChange}
                        />
                    </div>
                ))}
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default CreateCountryComponent;
