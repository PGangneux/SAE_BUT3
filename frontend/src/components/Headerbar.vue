<script>
import comp_searchbar  from './Searchbar.vue';
export default {
    name: "comp_headerbar",
    components: {
        comp_searchbar,
    },
};
</script>

<template>
    <header class="bg-dark text-white py-3">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/">Accueil</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/propos">À propos</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/condition_general">Conditions générales</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/inscription">Inscription</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/connextion">Connexion</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/mdpreset">Mot de passe oublié</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/account">Compte</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/admin">Admin</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/video_admin">Vidéo Admin</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link" to="/video">Vidéo</RouterLink>
                    </li>
                </ul>
            </div>
        </nav>
        <searchbar />
    </header>
</template>