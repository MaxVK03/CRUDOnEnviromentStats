import React, { useState } from 'react';
import api from '../api'; // Make sure this points to your API configuration

const DeleteCountryComponent = () => {
    const [deleteParams, setDeleteParams] = useState({
        countryName: '',
        countryIsocode: '',
        yearid: '',
        timeFrame: ''
    });

    const handleInputChange = (e) => {
        setDeleteParams({ ...deleteParams, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.delete('/country', { params: deleteParams });
            console.log('Country data deleted successfully');
        } catch (error) {
            console.error('Error deleting country data:', error);
        }
    };

    return (
        <div>
            <h2>Delete Country Data</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="countryName"
                    value={deleteParams.countryName}
                    onChange={handleInputChange}
                    placeholder="Country Name"
                />
                <input
                    type="text"
                    name="countryIsocode"
                    value={deleteParams.countryIsocode}
                    onChange={handleInputChange}
                    placeholder="Country ISO Code"
                />
                <input
                    type="number"
                    name="yearid"
                    value={deleteParams.yearid}
                    onChange={handleInputChange}
                    placeholder="Year ID"
                />
                <input
                    type="text"
                    name="timeFrame"
                    value={deleteParams.timeFrame}
                    onChange={handleInputChange}
                    placeholder="Time Frame"
                />
                <button type="submit">Delete</button>
            </form>
        </div>
    );
};

export default DeleteCountryComponent;
