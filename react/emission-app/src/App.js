import React from 'react';
import ContinentTemperatureChange from './endPointComponents/ContinentTemperatureChange';
import CountryDataComponent from './endPointComponents/CountryDataComponent';
import CreateCountryComponent from "./endPointComponents/CreateCountryComponent";
import UpdateCountryComponent from "./endPointComponents/UpdateCountryComponent";
import DeleteCountryComponent from "./endPointComponents/DeleteCountryComponent";
import CountryEmissionsComponent from "./endPointComponents/CountryEmissionsComponent";
import CountryEnergyComponent from "./endPointComponents/CountryEnergyComponent";
import CountryClimContComponent from "./endPointComponents/CountryClimContComponent";
import AdditionalCountryDataComponent from "./endPointComponents/AdditionalCountryDataComponent";
import './App.css' 


const App = () => {
    return (
        <div className="App-main">
            <h1>Data Fetching App</h1>
            <ContinentTemperatureChange />
            <CountryDataComponent />
            <CreateCountryComponent />
            <UpdateCountryComponent />
            <DeleteCountryComponent />
            <CountryEmissionsComponent />
            <CountryEnergyComponent />
            <CountryClimContComponent />
            <AdditionalCountryDataComponent />
        </div>
    );
};

export default App;
