import { defineStore } from "pinia";
import router from "@/router";
import api from "@/api/api";

import { useNotification } from "@kyvg/vue3-notification";
const { notify } = useNotification();

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        email: JSON.parse(localStorage.getItem('email')),
        access_token: JSON.parse(localStorage.getItem('access_token')),
        refresh_token: JSON.parse(localStorage.getItem('refresh_token')),
        first_name: JSON.parse(localStorage.getItem('first_name')),
        last_name: JSON.parse(localStorage.getItem('last_name')),
        returnUrl: null
    }),
    actions: {
        async login(email, password) {
            console.log('[auth.store.js] login called.')
            const res = await api.post('auth/api/login/', { email: email, password: password })
            .catch((error) => {
                console.log("auth.store ---> ERROR");
                notify({
                    title: "Login Error",
                    text: "Invalid crendentials."
                });
            })
            if (res.status === 200) {
                console.log('[auth.store.js] Response 200. Setting data...');
                console.log(`[auth.store.js] Email: ${res.data.email}`);
                this.email = res.data.email
                this.access_token = res.data.access_token
                this.refresh_token = res.data.refresh_token
                this.first_name = res.data.first_name
                this.last_name = res.data.last_name
                console.log('[auth.store.js] Global State set complete, Setting localStorage...');
                localStorage.setItem('email', JSON.stringify(res.data.email));
                localStorage.setItem('access_token', JSON.stringify(res.data.access_token));
                localStorage.setItem('refresh_token', JSON.stringify(res.data.refresh_token));
                localStorage.setItem('first_name', JSON.stringify(res.data.first_name));
                localStorage.setItem('last_name', JSON.stringify(res.data.last_name));
                console.log('[auth.store.js] localStorage Email: ', localStorage.getItem('email'))
                console.log('[auth.store.js] localStorage complete, Redirecting to next...')
                router.push(this.returnUrl || '/');
                notify({
                    title: 'ورود موفق',
                    text: 'با موفقیت وارد سایت شدید. خوش آمدید.'
                });
            } else {
                console.log('[auth.store.js] res status NOT 200', res.status);
            }
        },

        login_v2(email, password) {
            console.log('[auth.store.js] login v2 called.');
            api.post('auth/api/login/', { email, password })
                .then((res) => {
                    if (res.status === 200) {
                        console.log('200');
                        this.email = res.data.email
                        this.access_token = res.data.access_token
                        this.refresh_token = res.data.refresh_token
                        this.first_name = res.data.first_name
                        this.last_name = res.data.last_name
                        localStorage.setItem('email', JSON.stringify(res.data.email));
                        localStorage.setItem('access_token', JSON.stringify(res.data.access_token));
                        localStorage.setItem('refresh_token', JSON.stringify(res.data.refresh_token));
                        localStorage.setItem('first_name', JSON.stringify(res.data.first_name));
                        localStorage.setItem('last_name', JSON.stringify(res.data.last_name));
                        console.log('[auth.store.js] localStorage Email: ', localStorage.getItem('email'), 'localStorage complete, Redirecting to next...')
                        router.push(this.returnUrl || '/');
                    } else {
                        console.log('NOT 200 --> ', res.status);
                    }
                })
        },

        logout() {
            console.log('[auth.store.js] logout called, Removing global state...')
            this.email = null;
            this.access_token = null;
            this.refresh_token = null;
            this.first_name = null;
            this.last_name = null;
            console.log('[auth.store.js] Removing global finished, Removing localStorage...');
            localStorage.removeItem('email');
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('first_name');
            localStorage.removeItem('last_name');
            console.log('[auth.store.js] Removing localStorage finished, Redirecting...');
            router.push('/login');
        }
    }
});