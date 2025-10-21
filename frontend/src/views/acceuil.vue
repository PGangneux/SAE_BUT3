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
    </div>
</template>

<style scoped>
.pip-video {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  width: 300px;
  height: 170px;
  border: 2px solid var(--vert-neon);
  border-radius: 10px;
  overflow: hidden;
  z-index: 9999;
  background-color: black;
}
</style>
