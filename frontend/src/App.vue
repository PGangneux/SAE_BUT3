<script>
import { markRaw } from 'vue';
import comp_headerbar from './components/headerbar.vue';
import comp_footerbar from './components/footerbar.vue';
import Lecteur_video from './components/lecteur_video/lecteur_video.vue';
import Utilisateur from './model/utilisateur';

export default {
    name: "page_router",
    components: {
        comp_headerbar,
        comp_footerbar,
    },
    data() {
        return {
            user_current: {
                type: Utilisateur,
                value: null,
            },
            searchterm: "", // text de recherche
        }
    },
    provide() {
        return {
            user_current: {
                get: () => this.user_current,
                set: (value) => { this.user_current = value ? markRaw(value) : null; }
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
    <comp_headerbar />
    <main>
        <router-view :key="$route.fullPath"></router-view>
        <!--
            <router-view v-slot="lecteur_video">
            <keep-alive>
                <Lecteur_video :is="lecteur_video" />
            </keep-alive>
        -->
    </main>
    <comp_footerbar />
</template>