<script>
import { markRaw } from 'vue';
import { prefetcher } from "../../model/prefetcher";
import { videoStore } from "../../model/videoStore";

export default {
  props: {
    current_interview: {type: Object,},
    current_extrait: {type: Object,},
  },

  data() {
    return {
      videos: null,
      selected : ""

    };
  },

  methods : {
    

    async interview_current_extrait(){
      this.selected = "extrait_in_playlists"
      //this.videos = markRaw(await prefetcher.interview_extrait(this.current_extrait.uuid))    
    },

    async extraits_current_question(){
      console.log(this.current_extrait)
      this.selected = "questions"
      this.videos = markRaw(await prefetcher.extraits_question(this.current_extrait.question))
    },

    reset_videoStore() {
      console.log("avant reset:", JSON.parse(JSON.stringify(videoStore)))
      
      videoStore.currentTime = 0
      videoStore.isPlaying = true
      
      console.log("après reset:", JSON.parse(JSON.stringify(videoStore)))
    }
  },




  async mounted() {
    this.videos = markRaw(await prefetcher.extraits_all());
    console.log("liste des extrait")
    console.log(this.videos)

    
  },

};

</script>

<template>
    <header>
        <nav class="header-nav">
            <ul class="menu">
            <li @click="extraits_current_question" :class="{ selected: selected === 'questions' }">Questions</li>
            <li @click="" :class="{selected: selected === 'auteurs'}">Auteurs</li>
            <li @click="" :class="{selected: selected === 'thèmes'}">Thèmes</li>
            <li @click="interview_current_extrait" :class="{selected: selected === 'extrait_in_playlists'}">Playlists contenant l'extrait</li>
            </ul>
            <img src="/imgs/close.png" alt="close" @click="this.$emit('toggle_aside')">
        </nav>

    </header>
    <main>
        <div>
            <h2>{{ titreSideBar }}</h2>
            <div class="search-bar">
                <input type="text" :placeholder=" placeholderRecherche "/>
                <img src="/imgs/Search.png" alt="loupe"/>
            </div>
            <div>
                <ul class="liste_video">
                    <li v-for="video in videos">
                        <div v-if="video.uuid != current_extrait.uuid">
                          <router-link @click="reset_videoStore" :to="`/lecteur_video/${video.uuid}`">
                            <img :src="video.url_miniature_yt" :alt="video.titre"/>
                          </router-link>
                          <div>
                              <h4>{{ video.titre }}</h4>
                              
                          </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </main>

</template>

<style scoped>
header, main{
    background-color: var(--gris-foncer);
    padding: 0 0.5rem;
}

header{
    border-bottom: 1px solid var(--blanc);
    height: 5%;
}

main {
  height: 95%; /* le reste de la page */
  overflow-y: auto; /* permet le scroll vertical */
}
.header-nav {
  display: flex;
  justify-content: space-between; /* menu à gauche, bouton X à droite */
  align-items: center;            /* centre verticalement */
  
}

.menu {
  display: flex;       /* aligne les <li> horizontalement */
  list-style: none;    /* supprime les puces */
  gap: 1rem;           /* espace entre les items */
  margin: 0;
  padding: 0;
}

.menu li {
  cursor: pointer;
}

.selected {
  color: var(--vert-neon);
}



.close-btn {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
}

.search-bar {
  width: 100%;
  display: flex;
}

.search-bar input {
  width: 85%;
  height: 2rem;
  border: none;
  border-radius: 20px;
  padding-left: 2%;
  margin-right: 2%;
}

.search-bar img {
  width: 9%;
  cursor: pointer;
}

.liste_video {
  margin: 0;
  padding: 0;
  cursor: pointer;
}

.liste_video li > div {
  list-style: none;
  display: flex;
  
}

.liste_video img, .liste_video a{
  display: block;
  width: 100%;
  height: 100%;

  border-radius: 20px;
  object-fit: cover;
  background-color: var(--gris-moyen);
}

.liste_video a{
    width: 55%;
    height: 55%;
    margin-right: 1em;
    margin-bottom: 2em;
}




</style>
