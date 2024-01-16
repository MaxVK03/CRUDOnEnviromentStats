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
        const processedData = Object.entries(countryData).reduce((acc, [key, value]) => {
            if (value === '') {
                acc[key] = null;
            } else {
                switch (key) {
                    case 'year':
                    case 'population':
                        acc[key] = parseInt(value, 10);
                        break;
                    case 'gdp':
                    case 'co2':
                    case 'energy_per_capita':
                    case 'energy_per_gdp':
                    case 'methane':
                    case 'nitrous_oxide':
                    case 'share_of_temperature_change_from_ghg':
                    case 'temperature_change_from_ch4':
                    case 'temperature_change_from_co2':
                    case 'temperature_change_from_ghg':
                    case 'temperature_change_from_n2o':
                    case 'total_ghg':
                        acc[key] = parseFloat(value);
                        break;
                    default:
                        acc[key] = value;
                }
            }
            return acc;
        }, {});
        try {
            const response = await api.post('/country', processedData);
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
