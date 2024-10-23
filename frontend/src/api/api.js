import axios from "axios";
import dayjs from "dayjs";
import { jwtDecode } from "jwt-decode";
import { useAuthStore } from "@/stores/auth.store";

const token = localStorage.getItem('access_token') ? JSON.parse(localStorage.getItem('access_token')) : "";
const refresh_token = localStorage.getItem('refresh_token') ? JSON.parse(localStorage.getItem('refresh_token')) : "";

const baseUrl = "http://127.0.0.1:8000/";
const api = axios.create({
    baseURL: baseUrl,
    'Content-Type': 'application/json',
    headers: {'Authorization': localStorage.getItem('access_token') ? `Bearer ${token}` : null}
});

// in request:
//      if token existsed
//      check for exp
//      if exp
//      send refresh request
//      if fail -> logout
//      if ok -> add to store, and request

// in response:

api.interceptors.request.use(async req => {
    console.log("[api.js] ----> Intercept request.");
    const authStore = useAuthStore();
    if (token) {
        req.headers.Authorization = `Bearer ${token}`;
        const user = jwtDecode(token)
        const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;
        if (!isExpired) {
            console.log('[api.js] Token is not expired.')
            return req;
        } else {
            const res = await axios.post(`${baseUrl}auth/token/refresh/`, {
                refresh: refresh_token
            })
            .catch((e) => {
                console.log('[api.js] was unable to refresh the token automatically.');
                console.log(e);
                alert("We are sorry, Please login again.");
                authStore.logout();
            });
            if (res.status === 200) {
                console.log('[api.js]: New Token aquired. Setting it now...');
                localStorage.setItem('access_token', JSON.stringify(res.data.access))
                authStore.access_token = res.data.access
                req.headers.Authorization = `Bearer ${res.data.access}`;
                return req;
            } else {
                console.log("[api.js]: Refreshing token failed, logging out...");
                const res = await axios.post(`${baseUrl}/auth/logout/`, {refresh_token: refresh_token})
                .catch((e) => {
                    console.log("[api.js] Logout request failed.");
                    console.log(e);
                    authStore.logout();
                });
                if (res.status === 200) {
                    const authStore = useAuthStore();
                    authStore.logout()
                    console.log("[api.js] Successfully logged out. Removed all info.")
                }
            }
        }
    }

    return req;
});

export default api