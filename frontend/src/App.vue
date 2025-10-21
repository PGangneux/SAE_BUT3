<script>
import comp_headerbar from './components/headerbar.vue';
import comp_footerbar from './components/footerbar.vue';

export default {
    name: "page_router",
    components: {
        comp_headerbar,
        comp_footerbar,
    },
    data() {
        return {
            user_current: null, // user_t
            searchterm : "", // text de recherche
        }
    },
    provide() {
        return {
            user_current: {
                get: () => this.user_current,
                set: (value) => { this.user_current = value }
            },
            searchterm: {
                get: () => this.searchterm,
                set: (value) => { this.searchterm = value }
            }
        } 
    },
};
</script>

<template>
    <comp_headerbar :user_current="user_current" />
    <main>
        <KeepAlive include="lecteur_video">
        <RouterView />
        </KeepAlive>
    </main>
    <comp_footerbar />
</template>