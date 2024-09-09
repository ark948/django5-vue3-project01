import axios from "axios";

const token = localStorage.getItem('access_token') ? JSON.parse(localStorage.getItem('access_token')) : "";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000/",
    'Content-Type': 'application/json',
    headers: {'Authorization': localStorage.getItem('access_token') ? `Bearer ${token}` : null}
});

api.interceptors.request.use(async req => {
    console.log("[api.js] Calling interceptor...")
    if (token) {
        console.log("[api.js] Token was found.")
        req.headers.Authorization = `Bearer ${token}`;
    }

    return req;
});

export default api