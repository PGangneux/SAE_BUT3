<script>
import { markRaw } from 'vue';
import iframe_lecture_video from './iframe_lecture_video.vue';
import bar_liste_video from "./bar_liste_video.vue";
import timecode from "./timecode.vue";
import parametres from './parametres.vue';
import { videoStore } from "../../model/videoStore";
import Extrait from '../../model/extrait';
import Interview from '../../model/interview';

export default {
  name: "page_lecteur_video",
  components: { iframe_lecture_video, bar_liste_video, parametres, timecode },

  props: {
    Iuuid: {
      type: String,
    },
    Euuid: {
      type: String,
    },
  },

  data() {
    return {
      param_visible: false,
      pos_x_iframe: null,
      pos_y_iframe: null,
      aside_visible: true,
      extrait: null,
      interview: null,
      liste_extraits: null,
      base_url_yt: "https://www.youtube.com/embed/",
      base_url_vimeo: "https://player.vimeo.com/video/",
      url_yt: "",
      url_vimeo: "",
      url:null,
    };
  },

  async mounted() {
    this.extrait = markRaw(await Extrait.detail(this.Euuid));
    this.interview = markRaw(await Interview.detail(this.Iuuid));
    if (this.interview.uuid) {
      this.liste_extraits = markRaw( await this.interview.extraits);
    }

    this.url_yt = this.base_url_yt + this.extrait.youtube_url;
    this.url_vimeo = this.base_url_vimeo + this.extrait.vimeo_url;
    
    this.set_url(videoStore.lecteur)

  },

  beforeUnmount() {
    window.removeEventListener('resize', this.updatePopupPosition);
  },


  methods: {
    iframe_build(){
      // Mettre à jour la position du player
      this.pos_x_iframe = this.get_pos_x_iframe();
      this.pos_y_iframe = this.get_pos_y_iframe();
      window.addEventListener('resize', this.updatePopupPosition);
    },

    toggle_parametres() {
      this.param_visible = !this.param_visible;
    },

    picture_in_picture() {
      if (this.interview.uuid) {
        videoStore.uuid = this.Iuuid+"/"+this.Euuid;
      }
      else{
        videoStore.uuid = this.Euuid;
      }
      videoStore.url_yt = this.url_yt;
      videoStore.url_vimeo = this.url_vimeo;
      videoStore.url = this.url;
      videoStore.isPictureInPicture = true;
      this.$router.push("/");
    },

    get_pos_x_iframe() {
      if (videoStore.lecteur == "YouTube"){
        const rect = this.$refs.iframe?.$el?.getBoundingClientRect?.();
        return rect ? rect.right : null;
      }
      const rect = this.$refs.iframe?.$el?.getBoundingClientRect?.();
      return rect ? rect.right : null;
    },

    get_pos_y_iframe() {
      const rect = this.$refs.iframe?.$el?.getBoundingClientRect?.();
      return rect ? rect.bottom : null;
    },

    async toggle_aside() {
      this.aside_visible = !this.aside_visible;
      await this.updatePopupPosition();
    },

    async updatePopupPosition() {
      const before_visible = this.param_visible;
      if (this.param_visible) this.param_visible = false;
      await new Promise(resolve => setTimeout(resolve, 100));
      this.pos_x_iframe = this.get_pos_x_iframe();
      this.pos_y_iframe = this.get_pos_y_iframe();
      if (before_visible) this.param_visible = true;
    },

    set_url(lecteur) {
      this.url = (lecteur === 'YouTube') ? this.url_yt : this.url_vimeo;
    },

    async set_lecteur(new_lecteur){
      console.log("videoStore av set_lecteur: ")
      console.log(JSON.parse(JSON.stringify(videoStore)))
      videoStore.lecteur = new_lecteur
      this.set_url(videoStore.lecteur)
      
      await this.$refs.iframe.update_player()
    },

    async lunch_next_video() {
      
      if (!this.interview?.uuid) {
        return;
      }
      
      let index = this.liste_extraits.find(extrait => extrait.uuid === this.extrait.uuid).position; // recupère la position de l'extrait courant dans this.liste_extraits
      console.log("Index actuel:", index);  
      console.log("Longueur liste extraits:", this.liste_extraits.length);
      
      if (index < this.liste_extraits.length-1) {
        
        // Mettre à jour l'extrait local
        this.extrait = markRaw(this.liste_extraits[index+1]);
        console.log("Extrait suivant UUID:", this.extrait.uuid);
        console.log(this.extrait);
        
        // Mettre à jour les URLs
        this.url_yt = this.base_url_yt + this.extrait.youtube_url;
        this.url_vimeo = this.base_url_vimeo + this.extrait.vimeo_url;
        
        // Réinitialiser le store
        videoStore.currentTime = 0;
        videoStore.isPlaying = true;
        

        // Mettre à jour l'URL sans recharger (optionnel)
        this.$router.replace({
          path: `/lecteur_video/${this.Iuuid}/${this.extrait.uuid}`
        });

        console.log("Lecture de l'extrait suivant lancée.");
        console.log(this.Euuid);

      } else {
        console.log("Fin de la liste des extraits de l'interview");
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
        @lunch_next_video="lunch_next_video"
   
      />

      <div v-else class="player"></div>

      
      <div>
        <div id="bottom-iframe">
          <h2>{{ extrait?.titre || 'titre' }}</h2>
          <div class="right-content">
            <a>Voir toute les playlists</a>
            <img src="/imgs/Settings.png" alt="Paramètres" @click="toggle_parametres">
            <img src="/imgs/affichage_lecteur_réduit.png" alt="picture in picture" @click="picture_in_picture">
          </div>
        </div>

        <div id="description">
          <p>{{extrait?.description || 'description vidéo'}}</p>
        </div>
      </div>
    </main>

    <aside v-show="aside_visible">
      <timecode
        v-if="this.liste_extraits"
        :interview="this.interview"
        :liste_extrait="this.liste_extraits"
      />

      
      <bar_liste_video 
        @toggle_aside="toggle_aside" 
        :current_extrait="extrait"
      />
    </aside>
    <h2 v-show="!aside_visible" @click="toggle_aside"> < </h2>


    <parametres
        v-if="param_visible"
        :pos_x_iframe="pos_x_iframe"
        :pos_y_iframe="pos_y_iframe"
        :lecteur="lecteur"
        @set_lecteur="set_lecteur"
      />
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
