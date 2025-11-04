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