<script>
import { markRaw } from 'vue';
import Extrait from '../../model/extrait';
import { videoStore } from "../../model/videoStore";
import miniature_video from "./miniature_video.vue";

export default {
  components: { miniature_video, },
  emits: ["toggle_aside", 'update'],
  inject : ["extrait_current", "interview_current"],
  data() {
    return {
      videos: null,
      selected : "",
      img_close: true,
      extrait: null,
      interview: null,

    };
  },
  methods : {
    async interview_current_extrait(){
      this.selected = "extrait_in_playlists"
      this.videos = markRaw(await this.extrait.interviews)
    },

    async extraits_current_question(){
      this.selected = "questions"
      /// console.log("current extrait:", this.extrait)
      /// console.log(await this.extrait.question.then(question => { return question.extraits}))
      this.videos = markRaw(await this.extrait.question.then(question => { return question.extraits}))
    },
    async reset_videoStore(extrait) {
      console.log("reset")
      this.extrait_current.set(extrait);
      this.interview_current.set(null);
      
      videoStore.currentTime = 0;
      videoStore.isPlaying = true;
      console.log("videostore dans reset_videoStore avant clearInterval", videoStore.currentTime, videoStore.intervalId)
      clearInterval(videoStore.intervalId);
      console.log("videostore dans reset_videoStore après clearInterval", videoStore.currentTime, videoStore.intervalId)
      videoStore.intervalId = null;
      videoStore.currentTime = 0;
      console.log("videostore dans reset_videoStore", videoStore.currentTime, videoStore.intervalId)

      this.$emit('update');
      console.log("videostore dans reset_videoStore après emit", videoStore.currentTime, videoStore.intervalId)
    },


  },
  async mounted() {
    this.interview = this.interview_current.get()
    this.extrait = this.extrait_current.get()
    this.videos = markRaw(await Extrait.list());
    if (this.interview.uuid) this.img_close = false;

  },

};

</script>

<template>
    <header>
        <nav class="header-nav">
            <ul class="menu">
              <li @click="" :class="{selected: selected === 'auteurs'}">Auteurs</li>
              <li @click="" :class="{selected: selected === 'thèmes'}">Thèmes</li>
              <!--si la video est un extrait-->
              <li v-if="this.interview != {}" @click="extraits_current_question" :class="{ selected: selected === 'questions' }">Questions</li>
              <li v-if="this.interview != {}" @click="interview_current_extrait" :class="{selected: selected === 'extrait_in_playlists'}">Playlists contenant l'extrait</li>
              
            </ul>
            
            <img v-if="img_close" src="/imgs/close.svg" alt="close" @click="this.$emit('toggle_aside')">
        </nav>

    </header>
    <main>
        <div>
            <div class="search-bar">
                <input type="text" placeholder="placeholderRecherche"/>
                <img src="/imgs/Search.png" alt="loupe"/>
            </div>
            <div>
                <ul class="liste_video">
                    <li v-for="video in videos">
                        <div v-if="video.uuid != current_extrait?.uuid">
                            
                            <miniature_video v-if="this.interview" @click="reset_videoStore(video)" :video="video" />
                            <miniature_video v-else @click="reset_videoStore(video)" :video="video" />
                          <div>
                              <h4>{{ video.titre }}</h4>
                              <p>{{ video.description }}</p>
                              
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
    display: flex;
    align-items: center;     /* centre verticalement */
}

main {
  height: 64%; /* 100-5(header)-30(timecode)-1 */
  flex-grow: 1; /* permet à main de prendre tout l'espace restant */
  overflow-y: auto; /* permet le scroll vertical */
}
.header-nav {
  width: 100%;
  display: flex;
  justify-content: space-between; /* menu à gauche, bouton X à droite */
  align-items: center;            /* centre verticalement */
  
}

.header-nav > img {
  width: 6%;
  height: 6%;


  cursor: pointer;
  
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



.liste_video {
  margin: 0;
  padding: 0;
  cursor: pointer;
  display: flex;
  gap : 10px;
  flex-direction: column;
}

.liste_video li > div {
  list-style: none;
  display: flex;  
}

.liste_video img, .liste_video a{
  display: block;
  width: 30%;
  height: 30%;

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
