import React, { useState } from 'react';
import api from '../api';

const FetchCountryClimContComponent = () => {
    const [noCountries, setNumCountries] = useState('');
    const [yearid, setYearid] = useState('');
    const [pastYears, setPastYears] = useState(''); 
    const [sort, setSort] = useState('');
    const [inCSV, setInCSV] = useState(false);
    const [climContData, setClimContData] = useState(null);

    const fetchClimContData = async () => {
        try {
            const response = await api.get('/country/climCont/', { 
                params: {
                    noCountries: noCountries ? parseInt(noCountries) : null,
                    yearid: yearid ? parseInt(yearid) : null,
                    pastYears: pastYears ? parseInt(pastYears) : null,
                    sort: sort === '' ? null : sort,
                    inCSV
                }
            });
            setClimContData(response.data);
        } catch (error) {
            console.error('Error fetching climate data:', error);
            setClimContData(error.response)
        }
    };

    const clearData = () => {
        setClimContData(null);
    };

    return (
        <div>
            <h2>Fetch Contribution To Climate Change Data by Country</h2>
            <input
                type="number"
                value={noCountries}
                onChange={(e) => setNumCountries(e.target.value)}
                placeholder="Number of Countries"
            />
            <input
                type="number"
                value={yearid}
                onChange={(e) => setYearid(e.target.value)}
                placeholder="Year ID"
            />
            <input
                type="number"
                value={pastYears}
                onChange={(e) => setPastYears(e.target.value)}
                placeholder="Number of past years"
            />
            <input
                type="text"
                value={sort}
                onChange={(e) => setSort(e.target.value)}
                placeholder="Sort"
            />
            <label>
                <input
                    type="checkbox"
                    checked={inCSV}
                    onChange={(e) => setInCSV(e.target.checked)}
                />
                in CSV
            </label>
            <button onClick={fetchClimContData}>Fetch Data</button>
            <button onClick={clearData}>Clear Data</button>
            {climContData && <pre>{JSON.stringify(climContData, null, 2)}</pre>}
        </div>
    );
};

export default FetchCountryClimContComponent
