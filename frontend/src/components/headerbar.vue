<script>
import comp_searchbar from './searchbar.vue';
import ClientAPI from "../model/clientAPI.js";
import { markRaw } from 'vue';

export default {
    name: "comp_headerbar",
    components: {
        comp_searchbar,
    },
    data() {
        return {
            current_user: null,
            unsubscribe_current_user: null,
        };
    },

    computed: {
        isconnected() {
            return !!(this.current_user && this.current_user.pseudo);
        },
        isadmin() {
            return !!(this.current_user && this.current_user.is_admin);
        }
    },

    mounted() {
        this.unsubscribe_current_user = ClientAPI.subscribe((u) => { this.current_user = u ? markRaw(u) : u; });
    },

    beforeUnmount() {
        if (this.unsubscribe_current_user) { this.unsubscribe_current_user = this.unsubscribe_current_user(); };
    }
};
</script>

<template>
    <header>
        <nav>
            <ul class="liste">
                <li class="btn local">
                    <RouterLink class="nav-link" to="/">Accueil</RouterLink>
                </li>
                <li style="flex-grow: 1;">
                    <comp_searchbar class="flex-grow-1" />
                </li>
                <li class="btn local" v-if="isconnected && isadmin">
                    <RouterLink class="nav-link" to="/admin">Admin</RouterLink>
                </li>
                <li class="btn local" v-if="isconnected">
                    <RouterLink class="nav-link" to="/account">
                        <img src="/imgs/compte.svg" style="max-height: 1.5em;" alt="">
                    </RouterLink>
                </li>

                <li class="btn local" v-if="!isconnected">
                    <RouterLink class="nav-link" to="/inscription">S'inscrire</RouterLink>
                </li>
                <li class="btn local" v-if="!isconnected">
                    <RouterLink class="nav-link" to="/connection">Se Connecter</RouterLink>
                </li>
            </ul>
        </nav>
    </header>
</template>

<style scoped>
.liste {
    gap: 2%;
    padding: 0.5em 1em 0.5em 2em;
    background-color: var(--gris-moyen);
    display: flex;
    flex-wrap: wrap;
    list-style: none;
    align-content: center;
    justify-content: space-around;
    align-items: center;
}
.local {
    background-color: var(--vert-pale) !important;
    color: var(--blanc);
}

.local:hover {
    background-color: var(--vert-neon) !important;
}

ul{
    margin: 0;
    border-bottom: 3px solid var(--gris-taupe);
}
</style>