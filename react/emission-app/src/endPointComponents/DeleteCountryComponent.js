import React, { useState } from 'react';
import api from '../api';
import './Component.css';

const DeleteCountryComponent = () => {
    const [deleteParams, setDeleteParams] = useState({
        countryName: '',
        countryIsocode: '',
        yearid: ''
    });

    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);
    const handleInputChange = (e) => {
        setDeleteParams({ ...deleteParams, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        const processedDeleteParams = {
            countryName: deleteParams.countryName,
            countryIsocode: deleteParams.countryIsocode,
            yearid: deleteParams.yearid === '' ? null : parseInt(deleteParams.yearid, 10)
        };
        e.preventDefault();
        try {
            await api.delete('/country', { params: processedDeleteParams });
            setSuccessMessage('Country data deleted successfully');
            console.log('Country data deleted successfully');
            setError(null)
        } catch (error) {
            setError(error.response ? error.response.data : {detail : error.detail});
            const statusCode = error.response ? error.response.status : 500
            setError(prevError => ({
                ...prevError,
                status : statusCode
            }));
            console.error('Error deleting country data:', error);
            setSuccessMessage(null)
        }
    };

    return (
        <div className='Data-component'>
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
                {successMessage && (
                    <div style={{ color: 'green', marginTop: '10px' }}>
                        <strong>{successMessage}</strong>
                    </div>
                )}
                {error && (
                    <div style={{ color: 'red', marginTop: '10px' }}>
                        <strong>Error: {error.detail}</strong>
                        {error.status && <p> Status Code: {error.status}</p>}
                    </div>
                )}
                <button type="submit">Delete</button>
            </form>
        </div>
    );
};

export default DeleteCountryComponent;
