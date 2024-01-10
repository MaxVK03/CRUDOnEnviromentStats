import React, { useState } from 'react';
import api from '../api';

const UpdateCountryComponent = () => {
    const [countryUpdateData, setCountryUpdateData] = useState({
        countryName: '',
        countryIsocode: '',
        countryData: {
        }
    });
    const [responseCode, setResponseCode] = useState(null);

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
                countryData: countryUpdateData.countryData
            });
            setResponseCode(response.status);
            console.log(response.data);
        } catch (error) {
            setResponseCode(error.response ? error.response.status : 500); // Set error code if update fails
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
            {responseCode !== null && <p>Response Code: {responseCode}</p>}
        </div>
    );
};

export default UpdateCountryComponent;
