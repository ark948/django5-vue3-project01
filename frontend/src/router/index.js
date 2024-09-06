import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import Register from "@/components/Register.vue";
import GetData from "@/components/GetData.vue";
import SendData from "@/components/SendData.vue";
import VerifyEmail from "@/components/VerifyEmail.vue";
import VerifyEmail_v2 from "@/components/VerifyEmail_v2.vue";
import Login from "@/components/Login.vue";
import ProfileView from "@/views/ProfileView.vue";
import GetData_opt from "@/components/GetData_opt.vue";
import { useNotification } from "@kyvg/vue3-notification";
import TestAuth from "@/components/TestAuth.vue";

const { notify } = useNotification()

const routes = [
    { path: '/', component: HomeView, name: 'home' },
    { path: '/test-auth', component: TestAuth, name: 'test_auth'},
    { path: '/register', component: Register, name: 'register' },
    { path: '/verify-email', component: VerifyEmail_v2, name: 'verify_email' },
    { path: '/get-data', component: GetData, name: 'get_data' },
    { path: '/get-data-opt', component: GetData_opt, name: 'get_data_opt' },
    { path: '/post-data', component: SendData, name: 'post_data' },
    { path: '/login', component: Login, name: 'login' },
    { path: '/profile', component: ProfileView, name: "profile", 
        beforeEnter: (to, from) => {
            let user = JSON.parse(localStorage.getItem('user'))
            if (!user) {
                console.log("You cannot access this page.")
                notify({type: 'error', title: "Error", text: "You cannot access this page."})
                return false
            }
        }
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// navigation gaurds
// isAuth() will do the checking


export default router