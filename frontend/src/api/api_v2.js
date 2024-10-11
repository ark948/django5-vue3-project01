import { useAuthStore } from '@/stores';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import dayjs from 'dayjs';

// get token from localStorage if exists
// difference from api (v1): no checking if exists
const token = JSON.parse(localStorage.getItem('access_token'));
const refresh_token = JSON.parse(localStorage.getItem('refresh_token'));

// localStorage.getItem() returns null if not found

const baseURL = 'http://127.0.0.1:8000/';
// diff: no check
const api  = axios.create({
    baseURL: baseURL,
    'Content-Type': 'application/json',
    headers: {'Authorization': `Bearer ${token}`}
});

// run for every request
api.interceptors.request.use(async req => {
    console.log("[api_v2.js] ---> Request Intercept.");
    // diff: authStore defined outside, caused error: probably because of hoisting
    const authStore = useAuthStore();
    if (token) {
        console.log("--> Token was found. Checking for exp...");
        req.headers.Authorization = `Bearer ${token}`;
        const user = jwtDecode(token)
        const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;
        if (!isExpired) {
            // if access token is expired
            return req;
        } else {
            // attempt to get a new one, using refresh token
            console.log("--> token expired.");
            const res = await axios.post(`${baseURL}auth/token/refresh/`, {
                refresh: refresh_token
            })
            .catch((e) => {
                console.log("--> Failed to refresh token. Please login again.");
                authStore.logout();
            });
            if (res.status === 200) {
                localStorage.setItem('access_token', JSON.stringify(res.data.access))
                authStore.access_token = res.data.access
                req.headers.Authorization = `Bearer ${res.data.access}`;
                return req;
            } else {
                console.log("--> Manual logout.");
                // if refresh token failed, attempt to logout
                const res = await axios.post(`${baseURL}auth/logout/`, {refresh_token: refresh_token})
                .catch((e) => {
                    console.log("--> Manual logout failed.");
                    authStore.logout();
                });
                if (res.status === 200) {
                    // diff: no re-defining authStore?
                    authStore.logout()
                    console.log('--> Successful manual logout.');
                }
            }
        }
    }

    return req;
});

export default api