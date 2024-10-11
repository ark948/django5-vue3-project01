import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/public/HomeView.vue"
import Register from "@/components/auth/Register.vue";
import VerifyEmail from "@/components/auth/VerifyEmail.vue";
import { useNotification } from "@kyvg/vue3-notification";
import Login from "@/components/auth/Login.vue";
import ProfileView from "@/views/protected/ProfileView.vue"
import { useAuthStore } from '@/stores';
import ManualTokenRefresh from "@/views/protected/ManualTokenRefresh.vue";
import Bookmarks from "@/views/protected/Bookmarks.vue";
import NotFound from "@/views/public/NotFound.vue";
import ForgotPassword from "@/views/public/ForgotPassword.vue";
import PasswordResetConfirm from "@/components/auth/password_reset/PasswordResetConfirm.vue";

function removeQueryParams(to) {
    if (Object.keys(to.query).length)
        console.log(path);
        return { path: to.path, query: {}, hash: to.hash }
}

function removeHash(to) {
    console.log(path);
    if (to.hash) return { path: to.path, query: to.query, hash: '' }
}


const { notify } = useNotification();

const routes = [
    { path: '/', component: HomeView, name: 'home' },
    { path: '/home', redirect: '/' },
    { path: '/register', component: Register, name: 'register' },
    { path: '/verify-email', component: VerifyEmail, name: 'verify_email' },
    { path: '/login', component: Login, name: 'login' },
    { path: '/profile', component: ProfileView, name: "profile" },
    { path: '/manual-refresh', component: ManualTokenRefresh, name: 'manual_refresh' },
    { path: '/bookmarks-list', component: Bookmarks, name: 'bookmarks' },
    { path: '/forgot-password', component: ForgotPassword, nam: 'forgot_password' },
    { path: '/reset-password/:uidb64/:token/', component: PasswordResetConfirm, name: 'reset_password' },
    // { path: '/bookmarks-list-v2', component: BookmarksListV2, name: 'bookmarksv2' },

    { path: "/:catchall(.*)*", component: NotFound, name: "not_found" },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach(async (to) => {
    if (to.name == 'reset_password') {
        // special route (password reset)
        return
    }
    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/', '/login', '/register', '/verify-email', '/forgot-password'];
    const authRequired = !publicPages.includes(to.path);
    const auth = useAuthStore();

    if (authRequired && !auth.email) {
        console.log('[Router] access to a route blocked.')
        notify({
            title: "Restricted access.",
            text: "You need to log in to access this page.",
            type: "warn",
        });
        auth.returnUrl = to.fullPath;
        return '/login';
    } else if (auth.access_token && to.fullPath=='/login') {
        alert("You have already logged in.")
        console.log('[Router] Aleardy logged in, path blocked.');
        return '/';
    } else if (auth.access_token && to.fullPath == '/register') {
        alert("You have already registered.")
        console.log("[Router] Already registered, path blocked");
        return '/'
    }
});

export default router