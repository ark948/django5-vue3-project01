import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import Register from "@/components/auth/Register.vue";
import VerifyEmail_v2 from "@/components/auth/VerifyEmail_v2.vue";
import { useNotification } from "@kyvg/vue3-notification";
import Login_v4 from "@/components/auth/Login_v4.vue";
import ProfileView from "@/views/ProfileView.vue";
import { useAuthStore } from '@/stores';
import ManualTokenRefresh from "@/views/ManualTokenRefresh.vue";
import Bookmarks from "@/views/Bookmarks.vue";
import BookmarkItem from "@/components/bookmarker/BookmarkItem.vue";
import NotFound from "@/views/NotFound.vue";
import TestTable from "@/views/testTable.vue";


const { notify } = useNotification();

const routes = [
    { path: '/', component: HomeView, name: 'home' },
    { path: '/home', redirect: '/' },
    { path: '/register', component: Register, name: 'register' },
    { path: '/verify-email', component: VerifyEmail_v2, name: 'verify_email' },
    { path: '/login', component: Login_v4, name: 'login' },
    { path: '/profile', component: ProfileView, name: "profile" },
    { path: '/manual-refresh', component: ManualTokenRefresh, name: 'manual_refresh' },
    { path: '/bookmarks-list', component: Bookmarks, name: 'bookmarks' },
    { path: '/test-table', component: TestTable, name: 'test_table' },

    { path: "/:catchall(.*)*", component: NotFound, name: "not_found" },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach(async (to) => {
    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/login', '/register', '/verify-email', '/'];
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