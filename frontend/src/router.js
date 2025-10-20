import { createRouter, createWebHistory } from 'vue-router';

import page_acceuil from "./views/acceuil.vue";


const routes = [
    { path : "/", component: page_acceuil},
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;