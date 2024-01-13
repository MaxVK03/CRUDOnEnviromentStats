import axios from "axios";
import "./App.css"

const port = process.env.REACT_APP_FASTAPI_PORT || 8000;
console.log(port)

const api = axios.create({
    baseURL: `http://localhost:${port}`
})

export default api
