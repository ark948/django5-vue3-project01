import { defineStore } from "pinia";
import router from "@/router";
import api from "@/api/api";

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        email: JSON.parse(localStorage.getItem('email')),
        access_token: JSON.parse(localStorage.getItem('access_token')),
        refresh_token: JSON.parse(localStorage.getItem('refresh_token')),
        returnUrl: null
    }),
    actions: {
        async login(email, password) {
            console.log('[auth.store.js] login called.')
            const res = await api.post('auth/api/login/', { email, password })
            if (res.status === 200) {
                console.log('[auth.store.js] Response 200. Setting data...')
                console.log(`[auth.store.js] Email: ${res.data.email}`)
                console.log('[auth.store.js] Setting info global state...')
                this.email = res.data.email
                this.access_token = res.data.access_token
                this.refresh_token = res.data.refresh_token
                console.log('[auth.store.js] Global State set complete.')
                console.log('auth.store.js] Pinia email: ', this.email)
                console.log('[auth.store.js] Pinia Access: ', this.access_token)
                console.log('[auth.store.js] Pinia Refresh: ', this.refresh_token)
                console.log('[auth.store.js] Setting localStorage...')
                localStorage.setItem('email', JSON.stringify(res.data.email));
                localStorage.setItem('access_token', JSON.stringify(res.data.access_token));
                localStorage.setItem('refresh_token', JSON.stringify(res.data.refresh_token));
                console.log('[auth.store.js] localStorage set complete.')
                console.log('[auth.store.js] localStorage Email: ', localStorage.getItem('email'))
                console.log('[auth.store.js] localStorage Access: ', localStorage.getItem('access_token'))
                console.log('[auth.store.js] localStorage Refresh: ', localStorage.getItem('refresh_token'))
                console.log('[auth.store.js] Redirecting to next...')
                router.push(this.returnUrl || '/');
            } else {
                console.log('[auth.store.js] res status NOT 200')
                console.log('[auht.store.js] res status: ', res.status)
            }
        },
        logout() {
            console.log('[auth.store.js] logout called')
            console.log('[auth.store.js] Removing global state...')
            this.email = null;
            this.access_token = null;
            this.refresh_token = null;
            console.log('[auth.store.js] Removing global finished.')
            console.log('[auth.store.js] Removing localStorage...')
            localStorage.removeItem('email');
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            console.log('[auth.store.js] Removing localStorage finished.')
            console.log('[auth.store.js] Redirecting...')
            router.push('/login');
        }
    }
});