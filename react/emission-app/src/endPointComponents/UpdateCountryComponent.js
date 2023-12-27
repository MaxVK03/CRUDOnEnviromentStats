import React, { useState } from 'react';
import api from '../api'; // Make sure this points to your API configuration

const UpdateCountryComponent = () => {
    const [countryUpdateData, setCountryUpdateData] = useState({
        countryName: '',
        countryIsocode: '',
        countryData: {
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
        }
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        if (name === 'countryName' || name === 'countryIsocode') {
            setCountryUpdateData({ ...countryUpdateData, [name]: value });
        } else {
            setCountryUpdateData({
                ...countryUpdateData,
                countryData: { ...countryUpdateData.countryData, [name]: value }
            });
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.put('/country', {
                countryName: countryUpdateData.countryName,
                countryIsocode: countryUpdateData.countryIsocode,
                countrydt: countryUpdateData.countryData
            });
            console.log(response.data); // Handle the response appropriately
        } catch (error) {
            console.error('Error updating country data:', error);
        }
    };

    return (
        <div>
            <h2>Update Country Data</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Country Name (for update)</label>
                    <input
                        type="text"
                        name="countryName"
                        value={countryUpdateData.countryName}
                        onChange={handleInputChange}
                    />
                </div>
                <div>
                    <label>Country ISO Code (for update)</label>
                    <input
                        type="text"
                        name="countryIsocode"
                        value={countryUpdateData.countryIsocode}
                        onChange={handleInputChange}
                    />
                </div>
                {/* Generate input fields for each country data attribute */}
                {Object.keys(countryUpdateData.countryData).map((key) => (
                    <div key={key}>
                        <label>{key}</label>
                        <input
                            type="text"
                            name={key}
                            value={countryUpdateData.countryData[key]}
                            onChange={handleInputChange}
                        />
                    </div>
                ))}
                <button type="submit">Update</button>
            </form>
        </div>
    );
};

export default UpdateCountryComponent;
