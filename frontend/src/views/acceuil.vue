<script>
import { videoStore } from "../model/videoStore.js";
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

  data() {
    return {
      isDragging: false,
      offsetX: 0,
      offsetY: 0,
    };
  },

  methods : {

    picture_in_picture() {
      // console.log("→ Désactivation du Picture in Picture");
      // console.log("videoStore: ")
      // console.log(JSON.parse(JSON.stringify(videoStore)))
      
      //videoStore.lecteur = this.lecteur;
      // console.log("le lecteur: ")
      videoStore.isPictureInPicture = false;

      // Rediriger vers la page d’accueil
      // console.log(videoStore.uuid)
      this.$router.push("/lecteur_video/");
    },
  

    startDrag(event) {
      const pip = document.querySelector(".pip-video");

      this.isDragging = true;
      const rect = pip.getBoundingClientRect();
      this.offsetX = event.clientX - rect.left;
      this.offsetY = event.clientY - rect.top;

      // Désactiver la sélection pendant le drag
      document.body.style.userSelect = "none";
      document.body.style.pointerEvents = "auto"; // on garde pointer-events pour iframe

      document.addEventListener("mousemove", this.onDrag);
      document.addEventListener("mouseup", this.stopDrag);
    },

    onDrag(event) {
        if (!this.isDragging) return;
        const pip = document.querySelector(".pip-video");
        if (!pip) return;

        // Empêcher le PiP de sortir de l'écran
        const minX = 0;
        const minY = 0;
        const maxX = window.innerWidth - pip.offsetWidth;
        const maxY = window.innerHeight - pip.offsetHeight;

        let left = event.clientX - this.offsetX;
        let top = event.clientY - this.offsetY;

        if (left < minX) left = minX;
        if (top < minY) top = minY;
        if (left > maxX) left = maxX;
        if (top > maxY) top = maxY;

        pip.style.left = left + "px";
        pip.style.top = top + "px";
    },

    stopDrag() {
        this.isDragging = false;
        document.removeEventListener("mousemove", this.onDrag);
        document.removeEventListener("mouseup", this.stopDrag);
    },
  },
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
      @mousedown="startDrag"
      ref="pip"
    >
      <!-- iframe picture in picture-->
       
      <component
        v-if="videoStore.iframeComponent"
        :is="videoStore.iframeComponent.$options"
        v-bind="videoStore.iframeComponent.$props"
      />
      <img src="/imgs/agrandir.svg" 
          alt="picture in picture" 
          @click.stop="picture_in_picture">
    </div>
    


</template>

<style scoped>
.pip-video {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  width: 20%;
  height: 25%;

  overflow: hidden;
  z-index: 9999;
  
  
  border-radius: 20px;

  cursor: pointer;

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
