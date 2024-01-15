import React, { useState } from 'react';
import api from '../api';
import './Component.css';

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
    const [responseCode, setResponseCode] = useState(null); // New state for storing response code

    const handleInputChange = (e) => {
        setCountryData({ ...countryData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/country', countryData);
            setResponseCode(response.status); // Set response code on successful submission
            console.log(response.data); // Handle the response appropriately
        } catch (error) {
            setResponseCode(error.response ? error.response.status : 500); // Set error code if submission fails
            console.error('Error creating country data:', error);
        }
    };

    return (
        <div className='Data-component'>
            <h2>Create Country Data</h2>
            <form onSubmit={handleSubmit}>
                {/* Generate input fields for each attribute */}
                {Object.keys(countryData).map((key) => (
                    <div key={key}>
                        <label>{key}:&nbsp;&nbsp;</label>
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
            {responseCode !== null && <p>Response Code: {responseCode}</p>} {/* Display response code */}
        </div>
    );
};

export default CreateCountryComponent;
