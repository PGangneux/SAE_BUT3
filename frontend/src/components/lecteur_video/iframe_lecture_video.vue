<script>
import { onMounted, onBeforeUnmount, ref, nextTick } from "vue";
import { videoStore } from "../../stores/videoStore";

const YT_API_URL = "https://www.youtube.com/iframe_api";

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

export default {
  props: { url: String },

  setup(props, { expose }) {
    const player = ref(null);

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


    async function initYouTube(videoId) {
      const YT = await loadYouTubeAPI();
      await nextTick();

      console.log("✅ Création du player YouTube...");
      player.value = new YT.Player("player", {
        videoId,
        events: {
          onReady: (event) => {
            console.log("YouTube Player prêt !");
            if (videoStore.currentTime) event.target.seekTo(videoStore.currentTime);
            console.log("en cours ?" +videoStore.isPlaying )
            if (videoStore.isPlaying) event.target.playVideo();
            else event.target.pauseVideo();
          },
          onStateChange: (event) => {
            if (event.data === YT.PlayerState.PLAYING) videoStore.isPlaying = true;
            if (event.data === YT.PlayerState.PAUSED) videoStore.isPlaying = false;
          },
        },
      });

      // Synchronisation du temps de lecture
      setInterval(() => {
        if (player.value && typeof player.value.getCurrentTime === "function") {
          videoStore.currentTime = player.value.getCurrentTime();
        }
      }, 1000);
    }



    async function initVimeo() {
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
          await vimeoPlayer.setCurrentTime(videoStore.currentTime);
        } catch (err) {
          console.warn("Impossible de définir le temps :", err);
        }
      }

      if (videoStore.isPlaying) await vimeoPlayer.play();
      else await vimeoPlayer.pause();

      // Écoute des événements
      vimeoPlayer.on("timeupdate", ({ seconds }) => (videoStore.currentTime = seconds));
      vimeoPlayer.on("play", () => (videoStore.isPlaying = true));
      vimeoPlayer.on("pause", () => (videoStore.isPlaying = false));

      player.value = vimeoPlayer;
    }

    async function update_player() {
      if (player.value && player.value.destroy) {
        console.log("🔁 Destruction ancien player");
        player.value.destroy();
      }

      await nextTick();

      if (props.url.includes("youtube")) {
        const id = get_YT_videoId(props.url);
        await initYouTube(id);
      } else {
        await initVimeo();
      }
    }




    onMounted(async () => {
      await nextTick();
      console.log("création")
      if (props.url.includes("youtube")) {
        const id = get_YT_videoId(props.url);
        await initYouTube(id);
      } else {
        console.log("test init vimeo")
        await initVimeo();
        console.log("test fin init vimeo")
      }


    });



    onBeforeUnmount(() => {
      if (player.value && player.value.destroy) player.value.destroy();
    });

    expose({
      update_player,
    });

    return {};
  },
};
</script>

<template>
  <div class="player" id="player"></div>
</template>

