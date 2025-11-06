<script>
import { markRaw } from 'vue';
import iframe_lecture_video from './iframe_lecture_video.vue';
import bar_liste_video from "./bar_liste_video.vue";
import timecode from "./timecode.vue";
import parametres from './parametres.vue';
import { videoStore } from "../../model/videoStore";


export default {
  name: "page_lecteur_video",
  inject : ["extrait_current", "interview_current"],
  components: { iframe_lecture_video, bar_liste_video, parametres, timecode },

  data() {
    return {
      param_visible: false,
      pos_x_iframe: null,
      pos_y_iframe: null,
      aside_visible: true,
      interview: null,
      extrait: null,
      liste_extraits: null,
      base_url_yt: "https://www.youtube.com/embed/",
      base_url_vimeo: "https://player.vimeo.com/video/",
      url_yt: "",
      url_vimeo: "",
      url:null,
    };
  },

  async mounted() {
    /// ///console.log("Mounted lecteur_video.vue");
    await this.update()
    
    if (this.$refs.iframe) {
      // stocke l'instance complète dans videoStore
      videoStore.iframeComponent = this.$refs.iframe;
      console.log("iframeComponent stocké :", videoStore.iframeComponent);
      //await this.$refs.iframe.update_player();
    }
    console.log("videoStore iframe lecteru", videoStore.lecteur)
    
  },

  beforeUnmount() {
    window.removeEventListener('resize', this.updatePopupPosition);
  },


  methods: {
    async update(){
      
      const interviewData = await this.interview_current.get();
      const extraitData = await this.extrait_current.get();
      

      if (interviewData) {
        this.interview = markRaw(interviewData);
      } else {
        this.interview = null;
      }

      if (extraitData) {
        this.extrait = markRaw(extraitData);
      } else {
        this.extrait = null;
      }


      if (this.interview != null){ 

        this.liste_extraits = markRaw( await this.interview.extraits);
        if (!this.extrait){
          this.extrait = markRaw(this.liste_extraits[0]);
          this.extrait_current.set(this.liste_extraits[0]);
        }
      }
      else {
        this.liste_extraits = null;
      }

      this.url_yt = this.base_url_yt + this.extrait.youtube_url;
      this.url_vimeo = this.base_url_vimeo + this.extrait.vimeo_url;


      
      this.redirect_extrait(this.extrait)
    },

    iframe_build(){
      // Mettre à jour la position du player
      this.pos_x_iframe = this.get_pos_x_iframe();
      this.pos_y_iframe = this.get_pos_y_iframe();
      window.addEventListener('resize', this.updatePopupPosition);
    },

    picture_in_picture() {
      //videoStore.uuid = this.extrait.uuid;
      //videoStore.url_yt = this.url_yt;
      //videoStore.url_vimeo = this.url_vimeo;
      console.log("lecteur", videoStore.lecteur)
      console.log("url", videoStore.url)
      videoStore.isPictureInPicture = true;
      videoStore.iframeComponent.set_url(videoStore.lecteur) 
      this.$router.push("/");
    },

    async toggle_aside() {
      this.aside_visible = !this.aside_visible;
      await this.updatePopupPosition();
    },


    async redirect_extrait(extrait){
        // Mettre à jour l'extrait local
        this.extrait_current.set(markRaw(extrait)) ;
        this.extrait = markRaw(extrait);

        // Mettre à jour les URLs
        this.url_yt = this.base_url_yt + this.extrait.youtube_url;
        this.url_vimeo = this.base_url_vimeo + this.extrait.vimeo_url;
        
        // Réinitialiser le store
        videoStore.isPlaying = true;
        


        // update videoStore
        videoStore.uuid = this.extrait.uuid
        videoStore.url_yt = this.url_yt
        videoStore.url_vimeo = this.url_vimeo
        videoStore.url =  (videoStore.lecteur === 'YouTube') ? videoStore.url_yt : videoStore.url_vimeo;
        this.url = videoStore.url
        

        //update le player si il est présent
        if (!this.$refs.iframe) {
          console.log("iframe non trouvé, impossible de mettre à jour le player");
          return;
        }
        else{
          await this.$refs.iframe.update_player();
        }
        
        
    },

    async lancement_prochaine_video() {
      
      if (!this.interview) {
        return;
      }
      
      let index = this.liste_extraits.find(extrait => extrait.uuid === this.extrait.uuid).position; // recupère la position de l'extrait courant dans this.liste_extraits
      
      if (index < this.liste_extraits.length-1) {
        let next_extrait = this.liste_extraits[index + 1];
        // réinitialiser le temps de la vidéo
        //videoStore.currentTime = 0;
        // lancer la prochaine vidéo
        await this.redirect_extrait(next_extrait);

      } else {
        ///console.log("Fin de la liste des extraits de l'interview");
      }
    }

  },

  

};
</script>


<template>
  <div class="layout">
    <main>
      
      <iframe_lecture_video
        v-if="url"
        :url='this.url'
        ref="iframe"
        @iframe_build ="iframe_build"
        @lancement_prochaine_video="lancement_prochaine_video"
   
      />

      <div v-else class="player"></div>

      
      <div>
        <div id="bottom-iframe">
          <h2>{{ extrait?.titre || 'titre' }}</h2>
          <div class="right-content">
            <img src="/imgs/reduire.svg" alt="picture in picture" @click="picture_in_picture">
          </div>
        </div>

        <div id="description">
          <p>{{extrait?.description || 'description vidéo'}}</p>
        </div>
      </div>
    </main>

    <aside v-show="aside_visible">
    <timecode
      v-if="this.liste_extraits && this.interview"
      :interview="interview"
      :liste_extraits="liste_extraits"
      @redirect_extrait="redirect_extrait"
      @toggle_aside="toggle_aside"
    />


      
      <bar_liste_video 
        @toggle_aside="toggle_aside" 
        @update="update"
        :liste_extraits_current_interview="this.liste_extraits"
      />
    </aside>
    <h2 v-show="!aside_visible" @click="toggle_aside"> < </h2>


  </div>
</template>

<style scoped>
.layout {
  display: flex;
  width: 100vw;
  height: 100vh;
}

main {
  flex: 5;
  background-color: var(--noir);
  padding: 1rem;
  box-sizing: border-box;

  display: flex;
  flex-direction: column;
  margin: 0 auto; /* centre horizontalement */
  width: 83%;
  height: 100%;
  padding-left: 2%;
  padding-right: 2%;
}







#bottom-iframe {
  display: flex;
  justify-content: space-between; /* <-- sépare gauche / droite */
  align-items: center;             /* <-- aligne verticalement */
  width: 100%;
  padding: 0 0.5rem;
  box-sizing: border-box;
  margin-top: 2%;
}

#bottom-iframe h2 {
  margin: 0;
}

#bottom-iframe .right-content {
  display: flex;
  align-items: center;
  gap: 0.5rem; /* espace entre les éléments à droite */
}

#bottom-iframe img {
  width: 2em;
  height: 2em;
  cursor: pointer;
}

#bottom-iframe a {
  color: var(--vert-neon);
  text-decoration: underline;
  cursor: pointer;
}

#description {
  margin-top: 2%;
  background-color: var(--gris-foncer);
  border: var(--gris-foncer);
  border-radius: 20px;
  padding: 1rem;
  box-sizing: border-box;
}


.layout aside{
  flex: 2.2;
  background-color: var(--gris-moyen);
  border-left: 3px solid var(--gris-taupe);
  display: flex;
  flex-direction: column;
}

.layout h2{
  margin-right: 10px;
  color: var(--vert-neon);
}


iframe{
  width: 100%;
  height: 100%;
}




</style>
