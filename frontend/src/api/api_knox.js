import axios from "axios";
import dayjs from "dayjs";
import { jwtDecode } from "jwt-decode";
import { useAuthStore } from "@/stores/auth.store";

const token = localStorage.getItem('token') ? JSON.parse(localStorage.getItem('token')) : "";
const refresh_token = localStorage.getItem('token') ? JSON.parse(localStorage.getItem('token')) : "";

const baseUrl = "http://127.0.0.1:8000/";
const api = axios.create({
    baseURL: baseUrl,
    'Content-Type': 'application/json',
    headers: {'Authorization': localStorage.getItem('token') ? `Bearer ${token}` : null}
});

api.interceptors.request.use(async req => {
    console.log("[api.js] Calling interceptor...");
    const authStore = useAuthStore();
    if (token) {
        console.log("[api.js] Token was found.")
        req.headers.Authorization = `Bearer ${token}`;
        console.log("[api.js] Checking token for expiration...")
        const user = jwtDecode(token)
        const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;
        if (!isExpired) {
            console.log('[api.js] Token is not expired.')
            return req;
        } else {
            console.log('[api.js] Token is expired. Trying to refresh...')
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
                console.log("[api.js] Token Refresh complete.")
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