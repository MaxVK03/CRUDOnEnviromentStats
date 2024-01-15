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

        const processedData = Object.entries(updateData).reduce((acc, [key, value]) => {
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

        console.log('processedData:', processedData);
        try {
            const response = await api.put(`/country/${selectedCountry}/${selectedYear}`, processedData);
            setResponseCode(response.status);
        } catch (error) {
            setResponseCode(error.response ? error.response.status : 500);
             console.error('Error updating country data:', error);
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

