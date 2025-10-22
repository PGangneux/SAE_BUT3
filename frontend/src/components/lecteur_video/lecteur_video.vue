<script>
import iframe_lecture_video from './iframe_lecture_video.vue';
import bar_liste_video from "./bar_liste_video.vue";
import parametres from './parametres.vue';
import { videoStore } from "../../stores/videoStore";

export default {
  name: "page_lecteur_video",
  components: { iframe_lecture_video, bar_liste_video, parametres },

  data() {
    return {
      param_visible: false,
      pos_x_iframe: 0,
      pos_y_iframe: 0,
      aside_visible: true,
      lecteur: 'Viméo',

      url: "https://player.vimeo.com/video/1128762950?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
    };
  },

  methods: {
    toggle_parametres() {
      this.param_visible = !this.param_visible;
    },

    picture_in_picture() {
      console.log("→ Activation du Picture in Picture");
      videoStore.url = this.url;
      videoStore.lecteur = this.lecteur;
      console.log("le lecteur: "+this.lecteur)
      videoStore.isPictureInPicture = true;

      // Rediriger vers la page d’accueil
      this.$router.push("/");
    },


    get_pos_x_iframe() {
      const rect = this.$refs.iframe.$el.getBoundingClientRect();
      return rect.right;
    },


    get_pos_y_iframe() {
      const rect = this.$refs.iframe.$el.getBoundingClientRect();
      return rect.bottom; // position y
    },

    set_lecteur(new_lecteur){
      this.lecteur = new_lecteur
      console.log("update url")
      this.set_url(this.lecteur)
    },

    set_url(lecteur){
      if (lecteur == "YouTube"){
        this.url = "https://www.youtube.com/embed/1NYQ65FTEC8?si=gwQlb9W4mPKm9Ri-"
      }
      else{
        this.url = "https://player.vimeo.com/video/1128762950?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
      }
    },

    async toggle_aside(){
      this.aside_visible = !this.aside_visible
      await this.updatePopupPosition()
    },

    async updatePopupPosition() {
      const before_visible = this.param_visible;
      
      if (this.param_visible) this.param_visible = false;
      await new Promise(resolve => setTimeout(resolve, 100));
      this.pos_x_iframe = this.get_pos_x_iframe();
      this.pos_y_iframe = this.get_pos_y_iframe();
      
      if (before_visible) this.param_visible = true; 

    }

  },

  mounted() {
    this.pos_x_iframe = this.get_pos_x_iframe();
    this.pos_y_iframe = this.get_pos_y_iframe();
    window.addEventListener('resize', this.updatePopupPosition);
  },

  beforeUnmount() {
    window.removeEventListener('resize', this.updatePopupPosition);
  }
};
</script>

<template>
  <div class="layout">
    <main>
      <iframe_lecture_video :url="url" ref="iframe"/>
      <div>
        <div id="bottom-iframe">
          <h2>Title</h2>
          <div class="right-content">
            <a>Voir toute l’interview</a>
            <img src="/imgs/Settings.png" alt="Paramètres" @click="toggle_parametres">
            <img src="/imgs/affichage_lecteur_réduit.png" alt="picture in picture" @click="picture_in_picture">
          </div>
        </div>

        <div id="description">
          <p>Video description</p>
        </div>
      </div>
    </main>

    <aside v-if="aside_visible">
      <bar_liste_video @toggle_aside="toggle_aside"/>
    </aside>
    <h2 v-else @click="toggle_aside"> < </h2>


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


main > div {
  flex: 1;
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


</style>
