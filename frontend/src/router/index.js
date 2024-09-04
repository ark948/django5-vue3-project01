import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import Register from "@/components/Register.vue";

const routes = [
    { path: '/', component: HomeView, name: 'home' },
    { path: '/register', component: Register, name: 'register' },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router