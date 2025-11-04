import { createRouter, createWebHistory } from 'vue-router';

import page_acceuil from "./views/acceuil.vue";
import page_propos from "./views/a_propos.vue";
import page_condition_general from "./views/condition_general.vue";
import page_account from "./views/account.vue";
import page_connection from "./views/connection.vue";
import page_inscription from "./views/inscription.vue";
import page_reset_password from "./views/reset_password.vue";




// ADMIN PAGES
import page_admin from "./views/admin/admin_acceuil.vue";
import page_admin_listextrait from "./views/admin/list/admin_liste_extrait.vue";
import page_admin_listuser from "./views/admin/list/admin_liste_user.vue";
import page_admin_interview from "./views/admin/list/admin_liste_interview.vue";

import page_admin_edit_video from "./views/admin/edit/admin_edit_video.vue";
import page_admin_edit_client from "./views/admin/edit/admin_edit_client.vue";
import page_admin_edit_interview from "./views/admin/edit/admin_edit_interview.vue";


import page_admin_details_client from "./views/admin/admin_details_user.vue";



// Lecteur Video Pages
import lecteur_video from './components/lecteur_video/lecteur_video.vue';

const routes = [
    { path: "/", component: page_acceuil },
    { path: "/propos", component: page_propos },
    { path: "/conditiongeneral", component: page_condition_general },
    { path: "/account", component: page_account },
    { path: "/connection", component: page_connection },
    { path: "/inscription", component: page_inscription },
    { path: "/reset-password", component: page_reset_password },
    { path: "/lecteur_video/:Euuid", component: lecteur_video, props: true },// Euuid pour l'extrait
    { path: "/lecteur_video/:Iuuid/:Euuid", component: lecteur_video, props: true },// Iuuid pour l'interview


    
    
    { path: "/admin", component: page_admin },
    
    { path: "/admin/user", component: page_admin_listuser },
    { path: "/admin/user/edit", component: page_admin_edit_client },
    { path: "/admin/user/:id", component: page_admin_details_client },

    
    
    { path: "/admin/interview", component: page_admin_interview },
    { path: "/admin/interview/:id", component: page_admin_edit_interview },
    
    { path: "/admin/extrait", component: page_admin_listextrait },
    { path: "/admin/extrait/:id", component: page_admin_edit_video },


    
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;