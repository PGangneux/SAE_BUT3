import { createRouter, createWebHistory } from 'vue-router';

import page_acceuil from "./views/Acceuil.vue";
import page_admin from "./views/Admin.vue";


const routes = [
    { path : "/", component: page_acceuil},
    { path : "/admin", component: page_admin},
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;