import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import Register from "@/components/Register.vue";
import GetData from "@/components/GetData.vue";
import SendData from "@/components/SendData.vue";

const routes = [
    { path: '/', component: HomeView, name: 'home' },
    { path: '/register', component: Register, name: 'register' },
    { path: '/get-data', component: GetData, name: 'get_data' },
    { path: '/post-data', component: SendData, name: 'post_data' },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router