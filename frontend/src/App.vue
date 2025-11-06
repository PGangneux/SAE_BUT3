<script>
import { markRaw } from 'vue';
import comp_headerbar from './components/headerbar.vue';
import comp_footerbar from './components/footerbar.vue';
import Lecteur_video from './components/lecteur_video/lecteur_video.vue';
import Interview from './model/interview';
import Extrait from './model/extrait';
import { videoStore } from "./model/videoStore";

export default {
    name: "page_router",
    components: {
        comp_headerbar,
        comp_footerbar,
    },
    data() {
        return {
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
            searchterm: {
                get: () => this.searchterm,
                set: (value) => { this.searchterm = value }
            },
            interview_current: {
                get: async () => {
                    if (this.interview_current != null){
                        // console.log("icicicicici")
                        // console.log(this.interview_current)
                        /// console.log("APP VUE Getting interview_current from provider...",this.interview_current);
                        if (this.interview_current.value){
                            // console.log("APP VUE interview_current exists:", this.interview_current);
                            return this.interview_current;
                        } else {
                            const uuid = sessionStorage.getItem('interview_current');
                            if (uuid != "null"){
                                // console.log("avec uuid", uuid)
                                let tmp =  markRaw(await Interview.detail(uuid));
                                // console.log("APP VUE Fetched interview_current from sessionStorage:", tmp);
                                return tmp;
                            }
                            else{
                                // console.log("pas d'uuid", uuid)
                                return null;
                            }
                            
                        }
                    }
                    else{
                        // console.log("qkdqodqodqoz")
                        return null
                    }
                    
                },
                set: (value) => {
                    this.interview_current = value ? markRaw(value) : null;
                    sessionStorage.setItem('interview_current', this.interview_current ? this.interview_current.uuid: null);
                }
            },
            extrait_current: {
                get: async () => {

                    if (this.extrait_current.value) {
                        return this.extrait_current;
                    } else {
                        let tmp = markRaw(await Extrait.detail(sessionStorage.getItem('extrait_current')));
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