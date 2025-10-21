<script>
import user_t from '../user.js';
import comp_searchbar from './searchbar.vue';
export default {
    name: "comp_headerbar",
    components: {
        comp_searchbar,
    },
    props : {
        user_current : {
            type : user_t,
            required : false,
        },
    },
    computed : {
        isconnected() {return this.user_current?.uuid || false;},
        isadmin() {return this.user_current?.isadmin || false;},
    },
    watch : {
        user_current(oldu,newu){
            console.log("UPDATE USER");
            console.log(oldu);
            console.log(newu);
        }
    },
    mounted() {
        console.log("this.user_current");
        console.log(this.user_current);
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
    color : var(--blanc);
}
.local:hover {
    background-color: var(--vert-neon) !important;
}
</style>