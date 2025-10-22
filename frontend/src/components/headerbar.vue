<script>
import comp_searchbar from './searchbar.vue';

export default {
    name: "comp_headerbar",
    components: {
        comp_searchbar,
    },
    inject: ['user_current'],
    data() {
        return {
            userKey: 0
        }
    },
    watch: {
        'user_current.get()': {
            handler() {
                /// console.log("current_user headerbar");
                /// console.log(this.user_current.get());
                this.userKey++; // Force re-render
            },
            deep: true
        }
    },
    computed: {
        isconnected() {
            // console.log("current_user headerbar");
            // console.log(this.user_current.get());
            this.userKey;
            return this.user_current.get()?.pseudo || false;
        },
        isadmin() {
            this.userKey;
            return this.user_current.get()?.admin || false;
        }
    }
};
</script>

<template>
    <header class="bg-dark text-white py-3">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="btn local">
                        <RouterLink class="nav-link" to="/">Accueil</RouterLink>
                    </li>
                    <comp_searchbar />
                    <li class="btn local" v-if="isconnected && isadmin">
                        <RouterLink class="nav-link" to="/admin">Admin</RouterLink>
                    </li>
                    <li class="btn local" v-if="isconnected">
                        <RouterLink class="nav-link" to="/account">Compte</RouterLink>
                    </li>

                    <li class="btn local" v-if="!isconnected">
                        <RouterLink class="nav-link" to="/inscription">Inscription</RouterLink>
                    </li>
                    <li class="btn local" v-if="!isconnected">
                        <RouterLink class="nav-link" to="/connection">Connection</RouterLink>
                    </li>
                </ul>
            </div>
        </nav>
    </header>
</template>

<style scoped>
.local {
    background-color: var(--vert-pale) !important;
    color: var(--blanc);
}

.local:hover {
    background-color: var(--vert-neon) !important;
}
</style>