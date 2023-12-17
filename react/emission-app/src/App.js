import React, {useState, useEffect} from "react";
import api from './api'

const App = () => {
    const [envData, setEnvData] = useState([]);
    const [envFormData, setEnvFormData] = useState({
        id: '',
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
    })


    const fetchCO2Data = async () => {
        try {
            const response = await api.get('/country/data?countryName=Canada');
            if (Array.isArray(response.data)) {
                setEnvData(response.data);
                console.log(response.data)
            } else {
                setEnvData([]); // Set to empty array if response is not an array
            }
        } catch (error) {
            console.error("Error fetching data:", error);
            setEnvData([{
                "country": "Error fetching the country",
                "iso_code": "ERR",
                "gdp": null,
                "energy_per_capita": null,
                "methane": null,
                "share_of_temperature_change_from_ghg":null,
                "temperature_change_from_ch4": null,
                "temperature_change_from_ghg": null,
                "total_ghg": null,
                "population": 3752993,
                "id": 1,
                "year": 1250,
                "co2": null,
                "energy_per_gdp": null,
                "nitrous_oxide": null,
                "temperature_change_from_co2": null,
                "temperature_change_from_n2o": null
            }]); // Set to empty array in case of error
        }
    };

    useEffect(() => {
        fetchCO2Data();
    }, [])

    return (
        <div>
            <nav className='navbar navbar-dark bg-primary'>
                <div className='container-fluid'>
                    <a className='navbar-brand' href='#'>
                        Enviro app
                    </a>
                </div>
            </nav>
            <table className='table table-striped table-bordered table-hover'>
                <thead>
                    <tr>
                        <th>id</th>
                        <th>country</th>
                        <th>year</th>
                        <th>iso_code</th>
                        <th>population</th>
                        <th>gdp</th>
                        <th>co2</th>
                        <th>energy_per_capita</th>
                        <th>energy_per_gdp</th>
                        <th>methane</th>
                        <th>nitrous_oxide</th>
                        <th>temperature_change_from_ch4</th>
                        <th>temperature_change_from_co2</th>
                        <th>temperature_change_from_ghg</th>
                        <th>temperature_change_from_n2o</th>
                        <th>total_ghg</th>
                    </tr>
                </thead>
                <tbody>
                {envData.map((dItem)=>(
                    <tr key={dItem.id}>
                        <td>{dItem.country}</td>
                        <td>{dItem.year}</td>
                        <td>{dItem.iso_code}</td>
                        <td>{dItem.gdp}</td>
                        <td>{dItem.co2}</td>
                        <td>{dItem.energy_per_capita}</td>
                        <td>{dItem.energy_per_gdp}</td>
                        <td>{dItem.methane}</td>
                        <td>{dItem.nitrous_oxide}</td>
                        <td>{dItem.temperature_change_from_ch4}</td>
                        <td>{dItem.temperature_change_from_co2}</td>
                        <td>{dItem.temperature_change_from_ghg}</td>
                        <td>{dItem.temperature_change_from_n2o}</td>
                        <td>{dItem.total_ghg}</td>
                    </tr>
                ))}
                </tbody>
            </table>

        </div>
    )


}

export default App;
