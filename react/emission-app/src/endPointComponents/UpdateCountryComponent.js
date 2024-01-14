import React, { useState, useEffect } from 'react';
import api from '../api';

const UpdateCountryComponent = () => {
    const [countryList, setCountryList] = useState([]);
    const [selectedCountry, setSelectedCountry] = useState('');
    const [selectedYear, setSelectedYear

    ] = useState('');
    const [originalData, setOriginalData] = useState({});
    const [updateData, setUpdateData] = useState({});
    const [responseCode, setResponseCode] = useState(null);


    useEffect(() => {
        const fetchCountries = async () => {
            try {
                const response = await api.get('/country/list');
                setCountryList(response.data);
            } catch (error) {
                console.error('Error fetching countries:', error);
            }
        };
        fetchCountries();
    }, []);

    const handleCountryChange = (e) => {
        setSelectedCountry(e.target.value);
    };

    const handleYearChange = (e) => {
        setSelectedYear(e.target.value);
    };

    const handleInputChange = (e) => {
        setUpdateData({ ...updateData, [e.target.name]: e.target.value });
    };

    const fetchAndPopulateData = async () => {
        if (!selectedCountry || !selectedYear) {
            alert('Please select a country and year');
            return;
        }
        try {
            const response = await api.get('/country/data', { params:
                    {
                        countryIsocode: selectedCountry,
                        yearid: selectedYear
                    } });
            const data = response.data[0];
            setOriginalData(data);
            setUpdateData(data);
        } catch (error) {
            console.error('Error fetching country data:', error);
        }
    };


    const handleSubmit = async (e) => {
        e.preventDefault();
        const processedData = {
            ...updateData,
            year: parseInt(updateData.year, 10),
            population: parseInt(updateData.population, 10),
            gdp: parseFloat(updateData.gdp),
            co2: parseFloat(updateData.co2),
            energy_per_capita: parseFloat(updateData.energy_per_capita),
            energy_per_gdp: parseFloat(updateData.energy_per_gdp),
            methane: parseFloat(updateData.methane),
            nitrous_oxide: parseFloat(updateData.nitrous_oxide),
            share_of_temperature_change_from_ghg: parseFloat(updateData.share_of_temperature_change_from_ghg),
            temperature_change_from_ch4: parseFloat(updateData.temperature_change_from_ch4),
            temperature_change_from_co2: parseFloat(updateData.temperature_change_from_co2),
            temperature_change_from_ghg: parseFloat(updateData.temperature_change_from_ghg),
            temperature_change_from_n2o: parseFloat(updateData.temperature_change_from_n2o),
            total_ghg: parseFloat(updateData.total_ghg)
        };

        console.log('Hello');
        console.log('processedData', processedData);
        try {
            const response = await api.put('/country', processedData);
            setResponseCode(response.status);
        } catch (error) {
            setResponseCode(error.response ? error.response.status : 500);
            // console.error('Error updating country data:', error);
        }
    };



    return (
        <div>
            <h2>Update Country Data</h2>
            <div>
                <select value={selectedCountry} onChange={handleCountryChange}>
                    <option value="">Select Country</option>
                    {countryList.map(country => (
                        <option key={country.iso} value={country.iso}>{country.name}</option>
                    ))}
                </select>
                <

                    input
                    type="text"
                    value={selectedYear}
                    onChange={handleYearChange}
                    placeholder="Year"
                />
                <button type="button" onClick={fetchAndPopulateData}>
                    Fetch Country Data
                </button>
            </div>
            <form onSubmit={handleSubmit}>
                {Object.keys(updateData).map((key, index) => (
                    <div key={originalData.id + '-' + key}>
                        <label>{key}</label>
                        <input
                            type="text"
                            name={key}
                            value={updateData[key] || ''}
                            onChange={handleInputChange}
                        />
                    </div>
                ))}
                <button type="submit">Update Country</button>
            </form>
            {responseCode !== null && <p>Response Code: {responseCode}</p>}
        </div>
    );
};

export default UpdateCountryComponent;

