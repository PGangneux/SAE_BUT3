import { createRouter, createWebHistory } from 'vue-router';

import page_acceuil from "./views/Acceuil.vue";

import page_admin from "./views/admin/Admin.vue";
import page_admin_listextrait from "./views/admin/Admin_Liste_extrait.vue";
import page_admin_listuser from "./views/admin/Admin_Liste_user.vue";
import page_admin_listinterview from "./views/admin/Admin_Liste_interview.vue";


const routes = [
    { path : "/", component: page_acceuil},
    { path : "/admin", component: page_admin},
    { path : "/admin/extrait", component: page_admin_listextrait},
    { path : "/admin/user", component: page_admin_listuser},
    { path : "/admin/interview", component: page_admin_listinterview},
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;