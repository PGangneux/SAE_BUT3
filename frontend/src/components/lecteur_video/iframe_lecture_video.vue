<script>
import { onMounted, onBeforeUnmount, ref, nextTick } from "vue";
import { videoStore } from "../../stores/videoStore";

const YT_API_URL = "https://www.youtube.com/iframe_api";
const VIMEO_API_URL = "https://player.vimeo.com/api/player.js";

// ✅ 1. Charger l’API YouTube une seule fois globalement
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

  setup(props) {
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
      if (!window.Vimeo) {
        const script = document.createElement("script");
        script.src = VIMEO_API_URL;
        document.body.appendChild(script);
        await new Promise((r) => (script.onload = r));
      }

      player.value = new window.Vimeo.Player("player");
      if (videoStore.currentTime) player.value.setCurrentTime(videoStore.currentTime);
      if (videoStore.isPlaying) player.value.play();

      player.value.on("timeupdate", ({ seconds }) => (videoStore.currentTime = seconds));
      player.value.on("play", () => (videoStore.isPlaying = true));
      player.value.on("pause", () => (videoStore.isPlaying = false));
    }

    onMounted(async () => {
      await nextTick();
      if (props.url.includes("youtube")) {
        const id = get_YT_videoId(props.url);
        await initYouTube(id);
      } else {
        await initVimeo();
      }
    });

    onBeforeUnmount(() => {
      if (player.value && player.value.destroy) player.value.destroy();
    });

    return {};
  },
};
</script>

<template>
  <div id="player" style="width:100%; height:100%; border-radius:20px"></div>
</template>

<style scoped>
#player {
  width: 100%;
  height: 100%;
  border: 3px solid var(--blanc);
  border-radius: 20px;
  background-color: #000;
  box-sizing: border-box;
}
</style>
