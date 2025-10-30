// src/stores/videoStore.js
import { reactive } from "vue";

export const videoStore = reactive({
  uuid: "",
  url_yt: "",
  url_vimeo: "",
  url:"",
  lecteur: "Viméo",
  isPictureInPicture: false,
  currentTime: 0,   // <-- position actuelle en secondes
  isPlaying: true, // <-- statut lecture/pause
});
