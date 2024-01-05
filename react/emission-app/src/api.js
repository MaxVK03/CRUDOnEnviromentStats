import axios from "axios";
import "./App.css"


const api = axios.create({
    baseURL: 'http://localhost:8000'
})

export default api
