<script>

import { videoStore } from "../../model/videoStore";
import { nextTick } from 'vue';

export default {
  name: 'iframe_lecture_video',
  
  emits: ['lancement_prochaine_video'],

  data() {
    return {
      player: null
    };
  },

  methods: {
    loadYouTubeAPI() {
      if (window.YT && window.YT.Player) return Promise.resolve(window.YT);

      if (!window._ytApiPromise) {
        window._ytApiPromise = new Promise((resolve) => {
          const tag = document.createElement("script");
          tag.src = "https://www.youtube.com/iframe_api";
          window.onYouTubeIframeAPIReady = () => resolve(window.YT);
          document.head.appendChild(tag);
        });
      }

      return window._ytApiPromise;
    },

    get_YT_videoId(url) {
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
    },

    startTracking() {
      videoStore.intervalId = setInterval(() => {
        if (this.player && typeof this.player.getCurrentTime === "function") {
          videoStore.currentTime = this.player.getCurrentTime();
        }
      }, 1000);
    },

    stopTracking() {
      if (videoStore.intervalId) {
        clearInterval(videoStore.intervalId);
        videoStore.intervalId = null;
      }
    },

    reset_old_lecteur() {
      if (this.player) {
        if (typeof this.player.destroy === 'function') {
          this.player.destroy();
        }
        this.player = null;
      }
    },

    async initYouTube(videoId) {
      this.reset_old_lecteur();
      const YT = await this.loadYouTubeAPI();
      await nextTick();
      
      this.player = new YT.Player("player", {
        videoId,
        events: {
          onReady: (event) => {
            if (videoStore.currentTime) {
              event.target.seekTo(videoStore.currentTime);
            }
            if (videoStore.isPlaying) event.target.playVideo();
            else event.target.pauseVideo();
          },
          onStateChange: (event) => {
            if (event.data === YT.PlayerState.PLAYING) {
              videoStore.isPlaying = true;
              this.startTracking();
            }
            if (event.data === YT.PlayerState.PAUSED) {
              videoStore.isPlaying = false;
              this.stopTracking();
            }
            if (event.data === YT.PlayerState.ENDED) {
              this.$emit('lancement_prochaine_video');
            }
          },
        },
      });
    },

    async initVimeo() {
      this.stopTracking();
      this.reset_old_lecteur();
      
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
      iframe.src = videoStore.url;
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
      vimeoPlayer.on("timeupdate", ({ seconds }) => {
        videoStore.currentTime = seconds;
      });
      vimeoPlayer.on("play", () => (videoStore.isPlaying = true));
      vimeoPlayer.on("pause", () => (videoStore.isPlaying = false));
      vimeoPlayer.on("ended", () => {
        videoStore.currentTime = 0;
        this.$emit('lancement_prochaine_video');
      });

      this.player = vimeoPlayer;
    },

    async update_player() {
      console.log("update")
      await nextTick();
      if (videoStore.url.includes("youtube") || videoStore.url.includes("youtu.be")) {
        const id = this.get_YT_videoId(videoStore.url);
        await this.initYouTube(id);
      } else {
        await this.initVimeo();
      }
    },

    set_url(lecteur) {
      videoStore.url = (lecteur === 'YouTube') ? videoStore.url_yt : videoStore.url_vimeo;
      this.update_player();
    }
  },

  async mounted() {
    await nextTick();
    if (videoStore.url.includes("youtube")) {
      const id = this.get_YT_videoId(videoStore.url);
      await this.initYouTube(id);
    } else {
      await this.initVimeo();
    }
  },

  beforeUnmount() {
    if (this.player && this.player.destroy) this.player.destroy();
    this.stopTracking();
  }
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
