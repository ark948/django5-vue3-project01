import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import Register from "@/components/Register.vue";
import GetData from "@/components/GetData.vue";
import SendData from "@/components/SendData.vue";
import VerifyEmail_v2 from "@/components/VerifyEmail_v2.vue";
import GetData_opt from "@/components/GetData_opt.vue";
import { useNotification } from "@kyvg/vue3-notification";
import TestAuth from "@/components/TestAuth.vue";
import Login_v4 from "@/components/Login_v4.vue";
import ProfileView from "@/views/ProfileView.vue";
import { useAuthStore } from '@/stores';
import TestAuthRequiredView from "@/views/TestAuthRequiredView.vue";
import ManualTokenRefresh from "@/views/ManualTokenRefresh.vue";

const { notify } = useNotification()

const routes = [
    { path: '/', component: HomeView, name: 'home' },
    { path: '/test-auth', component: TestAuth, name: 'test_auth'},
    { path: '/register', component: Register, name: 'register' },
    { path: '/verify-email', component: VerifyEmail_v2, name: 'verify_email' },
    { path: '/get-data', component: GetData, name: 'get_data' },
    { path: '/get-data-opt', component: GetData_opt, name: 'get_data_opt' },
    { path: '/post-data', component: SendData, name: 'post_data' },
    { path: '/login', component: Login_v4, name: 'login' },
    { path: '/profile', component: ProfileView, name: "profile" },
    { path: '/secret', component: TestAuthRequiredView, name: 'test'},
    { path: '/manual-refresh', component: ManualTokenRefresh, name: 'manual_refresh' }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach(async (to) => {
    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/login', '/register', '/secret', '/verify-email'];
    const authRequired = !publicPages.includes(to.path);
    const auth = useAuthStore();

    if (authRequired && !auth.email) {
        console.log('[Router] access to a route blocked.')
        auth.returnUrl = to.fullPath;
        return '/login';
    } else if (auth.email && to.fullPath=='/login') {
        alert("You are already logged in.")
        console.log('[Router] Aleardy logged in, next path blocked.')
        return '/'
    }
});

export default router