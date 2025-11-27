<script>
import { markRaw, toRaw } from 'vue';
import Extrait from '../../model/extrait';
import { videoStore } from "../../model/videoStore";
import miniature_video from "./miniature_video.vue";
import Artiste from '../../model/artiste';

export default {
  components: { miniature_video, },
  emits: ["toggle_aside", 'update'],
  inject : ["extrait_current", "interview_current"],
  props: {
    liste_extraits_current_interview: {
      type: Object,
      
    }
  },
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
      this.selected = "playlists"
      this.videos = markRaw(await this.extrait.interviews)
    },

    async extraits_current_question(){
      this.selected = "questions"
      /// console.log("current extrait:", this.extrait)
      /// console.log(await this.extrait.question.then(question => { return question.extraits}))
      this.videos = markRaw(await this.extrait.question.then(question => { return question.extraits}))
    },

    async extraits_interviews_current_artiste() {
      this.selected = "artiste";

      const artistes_current_video = [];

      if (this.interview) {
        for (const extrait of this.liste_extraits_current_interview) {
          const artiste = await extrait.artiste;
          if (artiste && !artistes_current_video.includes(artiste)) {
            artistes_current_video.push(artiste);
          }
        }
      } else {
        const artiste = await this.extrait.artiste;
        if (artiste) artistes_current_video.push(artiste);
      }

      const extraits_artiste = new Map();
      const interviews_artiste = new Map();

      for (const artiste of artistes_current_video) {
        const extraits_artiste_all = await artiste.extraits;

        for (const un_extrait of extraits_artiste_all) {
          extraits_artiste.set(un_extrait.uuid, un_extrait);

          const interviews_extrait_all = await un_extrait.interviews;
          for (const un_interview of interviews_extrait_all || []) {
            interviews_artiste.set(un_interview.uuid, un_interview);
          }
        }
      }

      const artiste_videos = [
        ...extraits_artiste.values(),
        ...interviews_artiste.values()
      ];

      this.videos = markRaw(artiste_videos);
    },
    



    async update_liste_video(video) {

      // maj du extrait_current ou interview_current selon le type de video

      if (video.extraits) {
        // c'est une interview
        /// console.log(video)
        this.interview_current.set(video);
        

        ///console.log((await video.extraits)[0])
        this.extrait_current.set((await video.extraits)[0]);
      } else {
        // c'est un extrait
        this.extrait_current.set(video);
        this.interview_current.set(null);
      }
      // recupération des nouveau extrait et interview
      this.extrait = await this.extrait_current.get();
      this.interview = await this.interview_current.get();
      
      // reset du videoStore
      videoStore.isPlaying = true;
      clearInterval(videoStore.intervalId);
      videoStore.intervalId = null;
      videoStore.currentTime = 0;

      this.$emit('update');
      this.videos = markRaw(await Extrait.list());

      this.$refs.miniature_videos.forEach(child => {
        child.update_miniature();
      });


      
    },


    



  },
  async mounted() {
    this.interview = toRaw(await this.interview_current.get());
    this.extrait = toRaw(await this.extrait_current.get());
    this.videos = markRaw(await Extrait.list());
    if (this.interview) this.img_close = false;


  },

};

</script>

<template>
    <header>
        <nav class="header-nav">
            <ul class="menu">
              <li @click="extraits_interviews_current_artiste" :class="{selected: selected === 'artiste'}">Artiste</li>
              <li @click="" :class="{selected: selected === 'thèmes'}">Thèmes</li>
              <li v-if="this.interview === null" @click="extraits_current_question" :class="{ selected: selected === 'questions' }">Questions</li>
              <!--si la video est un extrait-->
              <li v-if="this.interview === null" @click="interview_current_extrait" :class="{selected: selected === 'playlists'}">Playlists</li>
              
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
                    <li v-for="(video, index) in videos" :key="video.uuid">
                        <div>
                              <miniature_video 
                                ref="miniature_videos" 
                                @click="update_liste_video(video)"
                                :video="video" 
                              />
                          <div class="video_text">
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



.liste_video a{
    width: 55%;
    height: 55%;
    margin-right: 1em;
    margin-bottom: 2em;
}

.video_text{
  padding-right: 5%;
  flex-grow: 1;
}

p, h4{
  margin: 0;
}





</style>
