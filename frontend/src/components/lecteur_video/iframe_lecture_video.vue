<script>
import { onMounted, onBeforeUnmount, ref, nextTick, } from "vue";
import { videoStore } from "../../model/videoStore";
import { markRaw } from 'vue';

const YT_API_URL = "https://www.youtube.com/iframe_api";

export default {
  props: { url: String },

  setup(props, { expose, emit }) {
    const player = ref(null);
    
    // Charger l’API YouTube une seule fois globalement
    function loadYouTubeAPI() {
      if (window.YT && window.YT.Player) return Promise.resolve(window.YT);

      if (!window._ytApiPromise) {
        window._ytApiPromise = new Promise((resolve) => {
          const tag = document.createElement("script");
          tag.src = YT_API_URL;
          window.onYouTubeIframeAPIReady = () => resolve(window.YT);
          document.head.appendChild(tag);
        });
      }

      return window._ytApiPromise;
    }

    function get_YT_videoId(url) {
      try {
        const u = new URL(url);
        if (u.hostname === "youtu.be") return u.pathname.slice(1);
        if (u.hostname.includes("youtube.com")) {
          if (u.pathname.startsWith("/embed/")) return u.pathname.split("/")[2];
          if (u.searchParams.has("v")) return u.searchParams.get("v");
        }
      } catch {
        console.warn("URL YouTube invalide :", url);
      }
      return null;
    }    

    function startTracking() {
      videoStore.intervalId = setInterval(() => {
        if (player.value && typeof player.value.getCurrentTime === "function") {
          /// console.log("YouTube current time :", player.value.getCurrentTime());
          videoStore.currentTime = player.value.getCurrentTime();
          /////console.log("aPRÈS Mise à jour videoStore.currentTime depuis YouTube :", videoStore.currentTime);
        }
      }, 1000);
    }

    function stopTracking() {
      if (videoStore.intervalId) {
        clearInterval(videoStore.intervalId);
        videoStore.intervalId = null;
        ///console.log("dans if Arrêt du suivi du temps de la vidéo", videoStore.currentTime);
      }
      else{
        ///console.log("Arrêt du suivi du temps de la vidéo", videoStore.currentTime);

      }
    }

    function reset_old_lecteur() {
      //  Nettoyer l'ancien player
      if (player.value) {
        if (typeof player.value.destroy === 'function') {
          player.value.destroy();
        }
        player.value = null;
      }
    }

    async function initYouTube(videoId) {
      reset_old_lecteur()
      const current_time = videoStore.currentTime
      const YT = await loadYouTubeAPI();
      await nextTick();
      player.value = new YT.Player("player", {
        videoId,
        playerVars: {
          start: 0  // Force le démarrage à 0
        },
        events: {
          onReady: (event) => {
            if (videoStore.currentTime) {
              event.target.seekTo(current_time);
              ///console.log("YouTube seekTo :", current_time);
              videoStore.currentTime = current_time;
              ///console.log("Après YouTube seekTo :", current_time);
              // Synchronisation du temps de lecture
            }
            if (videoStore.isPlaying) event.target.playVideo();
            else event.target.pauseVideo();
          },
          onStateChange: (event) => {
            if (event.data === YT.PlayerState.PLAYING) {
              videoStore.isPlaying = true;
              startTracking();
            }
            if (event.data === YT.PlayerState.PAUSED) {
              videoStore.isPlaying = false;
              stopTracking();
            }
            if (event.data === YT.PlayerState.ENDED) emit('lancement_prochaine_video');
          },
        },
      });


    }

    async function initVimeo() {
      stopTracking()
      reset_old_lecteur()
      const current_time = videoStore.currentTime
      // Charger Vimeo API si pas encore là
      if (!window.Vimeo || !window.Vimeo.Player) {
        await new Promise((resolve) => {
          const script = document.createElement("script");
          script.src = "https://player.vimeo.com/api/player.js";
          script.onload = resolve;
          document.body.appendChild(script);
        });
      }

      // Créer l'iframe
      const container = document.getElementById("player");
      container.innerHTML = "";

      const iframe = document.createElement("iframe");

      iframe.src = props.url;
      iframe.allow = "autoplay; fullscreen; picture-in-picture";
      iframe.allowFullscreen = true;
      iframe.style.width = "100%";
      iframe.style.height = "100%";
      container.appendChild(iframe);


      // Créer le player
      const vimeoPlayer = new window.Vimeo.Player(iframe);

      // Attendre qu'il soit prêt
      try {
        await vimeoPlayer.ready();
      } catch (e) {
        console.error("Vimeo jamais prêt :", e);
        return;
      }
      // Synchroniser l'état
      if (videoStore.currentTime) {
        try {
          await vimeoPlayer.setCurrentTime(current_time);
          ///console.log("Vimeo setCurrentTime :", current_time);
          videoStore.currentTime = current_time
          ///console.log("Après Vimeo setCurrentTime :", current_time);
        } catch (err) {
          console.warn("Impossible de définir le temps :", err);
        }
      }

      if (videoStore.isPlaying) await vimeoPlayer.play();
      else await vimeoPlayer.pause();

      // Écoute des événements
      vimeoPlayer.on("timeupdate", ({ seconds }) => {
<<<<<<< HEAD
         /// ///console.log("Vimeo timeupdate :", seconds);
        ///console.log("Mise à jour videoStore.currentTime depuis Vimeo :", videoStore.currentTime);
=======
         /// console.log("Vimeo timeupdate :", seconds);
>>>>>>> bcee838 (changement correct des consol point log)
        videoStore.currentTime = seconds; 
        ///console.log("Après Mise à jour videoStore.currentTime depuis Vimeo :", videoStore.currentTime);
      });
      vimeoPlayer.on("play", () => (videoStore.isPlaying = true));
      vimeoPlayer.on("pause", () => (videoStore.isPlaying = false));
      vimeoPlayer.on("ended", () => (emit('lancement_prochaine_video')));

      player.value = vimeoPlayer;
    }

    async function update_player() {
      await nextTick();
<<<<<<< HEAD
      ///console.log("videostore", videoStore.isPlaying)
=======
      // console.log("videostore", videoStore.isPlaying)
>>>>>>> bcee838 (changement correct des consol point log)
      if (props.url.includes("youtube")) {

        const id = get_YT_videoId(props.url);
        await initYouTube(id);
      } else {
        await initVimeo();
      }
    }

    onMounted(async () => {
<<<<<<< HEAD
      /// ///console.log("Initialisation du lecteur iframe vidéo");
      /// ///console.log("URL vidéo :", props.url);
      /// ///console.log("Temps courant :", videoStore);
      ///console.log("videostore au montage iframe", videoStore.currentTime)
=======
      /// console.log("Initialisation du lecteur iframe vidéo");
      /// console.log("URL vidéo :", props.url);
      /// console.log("Temps courant :", videoStore);
>>>>>>> bcee838 (changement correct des consol point log)
      await nextTick();
      ///console.log("après next tick montage iframe", videoStore.currentTime)
      if (props.url.includes("youtube")) {
        const id = get_YT_videoId(props.url);
        await initYouTube(id);
      } else {

        await initVimeo();
      }

      emit('iframe_build')


    });



    onBeforeUnmount(() => {
      if (player.value && player.value.destroy) player.value.destroy();
      stopTracking();
    });

    expose({
      update_player,
    });

    return {};
  },
};
</script>

<template>
  <div ref="rootElement" class="rootElement">
    <div class="player" id="player"></div>
  </div>
</template>

<style scoped>
.rootElement {
  width: 100%;
  height: 100%;

  background-color: #000;
}
</style>
