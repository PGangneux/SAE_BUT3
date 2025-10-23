// src/stores/videoStore.js
import { reactive } from "vue";

export const videoStore = reactive({
  uuid: "",
  url_yt: "",
  url_vimeo: "",
  url:"",
  lecteur: "",
  isPictureInPicture: false,
  currentTime: 0,   // <-- position actuelle en secondes
  isPlaying: false, // <-- statut lecture/pause
});
