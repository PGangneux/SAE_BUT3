<script>
import { videoStore } from "../stores/videoStore.js";
import comp_mindmap from "../components/mindmap.vue";
import comp_recent from "../components/home_recent.vue";
import iframe_lecture_video from "../components/lecteur_video/iframe_lecture_video.vue";

export default {
  name: "page_accueil",
  components: {
    comp_mindmap,
    comp_recent,
    iframe_lecture_video
  },
  setup() {
    return { videoStore };
  },

  methods : {
    picture_in_picture() {
      console.log("→ Désactivation du Picture in Picture");
      videoStore.url = this.url;
      videoStore.lecteur = this.lecteur;
      console.log("le lecteur: "+this.lecteur)
      videoStore.isPictureInPicture = false;

      // Rediriger vers la page d’accueil
      this.$router.push("/lecteur_video");
    },
  }
};
</script>

<template>
    <h1>Accueil</h1>
    <comp_recent />
    <comp_mindmap />

    <!-- Si le mode PiP est actif -->
    <div 
        v-if="videoStore.isPictureInPicture" 
        class="pip-video"
    >
        <iframe_lecture_video :url="videoStore.url" />
        <img src="/imgs/affichage_lecteur_réduit_2.svg" alt="picture in picture" @click="picture_in_picture">
    </div>
</template>

<style scoped>
.pip-video {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  width: 30%;
  height: 30%;

  overflow: hidden;
  z-index: 9999;

}

/* L'image est positionnée par rapport au conteneur pip-video */
.pip-video img {
  position: absolute; /* position par rapport au parent */
  top: 0.5rem;        /* un petit offset depuis le haut */
  left: 0.5rem;       /* un petit offset depuis la gauche */
  width: 8%;        /* mieux qu'un pourcentage pour un bouton */
  z-index: 10000;     /* toujours au-dessus du contenu */
  cursor: pointer;

}

</style>
