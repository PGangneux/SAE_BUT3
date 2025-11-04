<script>
import { markRaw } from 'vue';
import comp_headerbar from './components/headerbar.vue';
import comp_footerbar from './components/footerbar.vue';
import Lecteur_video from './components/lecteur_video/lecteur_video.vue';
import Utilisateur from './model/utilisateur';
import Interview from './model/interview';
import Extrait from './model/extrait';

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
            interview_current: markRaw({
                type: Interview,
                value: null,
            }),
            extrait_current: markRaw({
                type: Extrait,
                value: null,
            }),
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
            },
            interview_current: {
                get: async () => {
                    /// console.log("APP VUE Getting interview_current from provider...",this.interview_current);
                    if (this.interview_current.value){
                        /// console.log("APP VUE interview_current exists:", this.interview_current);
                        return this.interview_current;
                    } else {
                        let tmp =  markRaw(await Interview.detail(sessionStorage.getItem('interview_current')));
                        /// console.log("APP VUE Fetched interview_current from sessionStorage:", tmp);
                        return tmp;
                    }
                },
                set: (value) => {
                    this.interview_current = value ? markRaw(value) : null;
                    sessionStorage.setItem('interview_current', this.interview_current.uuid);
                }
            },
            extrait_current: {
                get: async () => {
                    /// console.log("APP VUE Getting extrait from provider...",this.extrait_current);

                    if (this.extrait_current.value) {
                        /// console.log("APP VUE extrait_current exists:", this.extrait_current);
                        return this.extrait_current;
                    } else {
                        let tmp = markRaw(await Extrait.detail(sessionStorage.getItem('extrait_current')));
                        //// console.log("APP VUE Fetched extrait_current from sessionStorage:", tmp);
                        return tmp;
                    } 
                },
                set: (value) => {
                    this.extrait_current = value ? markRaw(value) : null;
                    sessionStorage.setItem('extrait_current', this.extrait_current.uuid);
                }
                },
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