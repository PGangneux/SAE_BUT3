import { createRouter, createWebHistory } from 'vue-router';

import page_acceuil from "./views/acceuil.vue";
import page_propos from "./views/propos.vue";
import page_condition_general from "./views/condition_general.vue";
import page_inscription from "./views/inscription.vue";
import page_connextion from "./views/connextion.vue";
import page_mdpreset from "./views/mdpreset.vue";
import page_account from "./views/account.vue";
import page_admin from "./views/admin.vue";
import page_video_admin from "./views/video_admin.vue";
import page_video from "./views/video.vue";


const routes = [
    { path : "/", component: page_acceuil},
    { path : "/propos", component: page_propos},
    { path : "/condition_general", component: page_condition_general},
    { path : "/inscription", component: page_inscription},
    { path : "/connextion", component: page_connextion},
    { path : "/mdpreset", component: page_mdpreset},
    { path : "/account", component: page_account},
    { path : "/admin", component: page_admin},
    { path : "/video_admin", component: page_video_admin},
    { path : "/video", component: page_video},
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;