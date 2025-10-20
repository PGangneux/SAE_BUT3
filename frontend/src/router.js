import { createRouter, createWebHistory } from 'vue-router';

import page_acceuil from "./views/acceuil.vue";
import page_account from "./views/account.vue";
import page_connection from "./views/connection.vue";
import page_inscription from "./views/inscription.vue";
import page_reset_password from "./views/reset_password.vue";

// ADMIN PAGES
import page_admin from "./views/admin/admin_acceuil.vue";
import page_admin_listextrait from "./views/admin/admin_liste_extrait.vue";
import page_admin_listuser from "./views/admin/admin_liste_user.vue";

// Lecteur Video Pages
import lecteur_video from './components/lecteur_video/lecteur_video.vue';

const routes = [
    { path: "/", component: page_acceuil },
    { path: "/account", component: page_account },
    { path: "/connection", component: page_connection },
    { path: "/inscription", component: page_inscription },
    { path: "/reset-password", component: page_reset_password },
    { path: "/admin", component: page_admin },
    { path: "/admin/extrait", component: page_admin_listextrait },
    { path: "/admin/user", component: page_admin_listuser },
    { path: "/admin/interview", component: page_admin },
    { path: "/lecteur_video", component: lecteur_video },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;