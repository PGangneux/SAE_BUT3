<script>
import comp_headerbar from './components/headerbar.vue';
import comp_footerbar from './components/footerbar.vue';
import Lecteur_video from './components/lecteur_video/lecteur_video.vue';

export default {
    name: "page_router",
    components: {
        comp_headerbar,
        comp_footerbar,
    },
    data() {
        return {
            searchterm: "", // text de recherche
        }
    },
    watch : {},
    provide() {
        return {
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