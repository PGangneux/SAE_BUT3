<script>

export default {
    name: "comp_headerbaradmin",
    components: {
    },
};
</script>

<template>
    <header class="bg-dark text-white py-3">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">

                    <li class="nav-item">
                        <RouterLink class="nav-link btn btn-secondary" to="/admin"> Accueil Admin </RouterLink>
                    </li>

                    <li class="nav-item">
                        <RouterLink class="nav-link btn btn-secondary" to="/admin/extrait"> Extrait </RouterLink>
                    </li>

                    <li class="nav-item">
                        <RouterLink class="nav-link btn btn-secondary" to="/admin/user"> User </RouterLink>
                    </li>

                    <li class="nav-item">
                        <RouterLink class="nav-link btn btn-secondary" to="/admin/interview">Playlist</RouterLink>
                    </li>

                </ul>
            </div>
        </nav>
    </header>
</template>