import { createRouter, createWebHistory } from 'vue-router'



const routes = [
    { path: '/', component: HomePage, name: 'home' },
    { path: '/home', redirect: '/' },
]


const router = createRouter({
    history: createWebHistory(),
    routes,
});


export default router