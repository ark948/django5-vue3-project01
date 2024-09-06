import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import Register from "@/components/Register.vue";
import GetData from "@/components/GetData.vue";
import SendData from "@/components/SendData.vue";
import VerifyEmail from "@/components/VerifyEmail.vue";
import VerifyEmail_v2 from "@/components/VerifyEmail_v2.vue";
import Login from "@/components/Login.vue";

const routes = [
    { path: '/', component: HomeView, name: 'home' },
    { path: '/register', component: Register, name: 'register' },
    { path: '/verify-email', component: VerifyEmail_v2, name: 'verify_email' },
    { path: '/get-data', component: GetData, name: 'get_data' },
    { path: '/post-data', component: SendData, name: 'post_data' },
    { path: '/login', component: Login, name: 'login' },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router