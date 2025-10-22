// src/stores/videoStore.js
import { reactive } from "vue";

export const videoStore = reactive({
  url: "",
  lecteur: "",
  isPictureInPicture: false,
  currentTime: 0,   // <-- position actuelle en secondes
  isPlaying: false, // <-- statut lecture/pause
});
