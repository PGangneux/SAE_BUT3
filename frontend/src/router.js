import { createRouter, createWebHistory } from 'vue-router';


// certaines pages  soient chargées légèrement en avance (par ex. la page de login ou la page admin),
//{ 
//  path: "/connection", 
//  component: () => import(/* webpackPrefetch: true */ "./views/connection.vue") 
//}


const routes = [
  // Pages principales
  { path: "/", component: () => import("./views/acceuil.vue") },
  { path: "/propos", component: () => import("./views/a_propos.vue") },
  { path: "/conditiongeneral", component: () => import("./views/condition_general.vue") },
  { path: "/account", component: () => import("./views/account.vue") },
  { path: "/connexion", component: () => import("./views/connexion.vue") },
  { path: "/inscription", component: () => import("./views/inscription.vue") },
  { path: "/reset-password", component: () => import("./views/reset_password.vue") },
  { path: "/lecteur_video/", component: () => import("./components/lecteur_video/lecteur_video.vue"), props: true },

  // Admin pages
  { path: "/admin", component: () => import("./views/admin/admin_acceuil.vue") },
  { path: "/admin/user", component: () => import("./views/admin/list/admin_liste_user.vue") },
  { path: "/admin/user/:id", component: () => import("./views/admin/edit/admin_details_user.vue") },
  { path: "/admin/interview", component: () => import("./views/admin/list/admin_liste_interview.vue") },
  { path: "/admin/interview/:id", component: () => import("./views/admin/edit/admin_edit_interview.vue") },
  { path: "/admin/extrait", component: () => import("./views/admin/list/admin_liste_extrait.vue") },
  { path: "/admin/extrait/:id", component: () => import("./views/admin/edit/admin_edit_video.vue") },

  { path: "/admin/autres", component: () => import("./views/admin/autres.vue") },

  // creer admin 
    { path: "/admin/extrait/:id",  },
    { path: "/admin/extrait/:id",  },
    { path: "/admin/extrait/:id",  },
    { path: "/admin/extrait/:id",  },


    { path: "/admin/user/creer/",         component: () => import("./views/admin//creer/admin_creer_user.vue")},
    { path: "/admin/interview/creer/",    component: () => import("./views/admin/creer/admin_creer_interview.vue")},
    { path: "/admin/extrait/creer/",      component: () => import("./views/admin/creer/admin_creer_video.vue")},
    { path: "/admin/:type/supprimer/:id", component: () => import("./views/admin/supprimer.vue")},


];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;