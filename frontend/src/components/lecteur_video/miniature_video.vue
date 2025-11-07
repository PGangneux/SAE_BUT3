<template>
  <div class="miniature-wrapper">
    <img v-if="url" :src="url" :alt="video.titre" />
    <p class="duree">{{ duree }}</p>
  </div>
</template>

<script>
export default {
  props: ["video"],
  data() {
    return { 
      url: null,
      duree: "00:00",
    };
  },
  async mounted() {
    await this.update_miniature()
  },
  methods: {
    async get_miniature(video) {
      try {
        // Cas 1 : c’est un extrait
        if (!video.extraits) {
          return (
            video.url_miniature_yt ||
            (await video.get_url_miniature_vimeo())
          );
        }

        // Cas 2 : c’est une interview
        const extraits = await video.extraits;
        if (!extraits || extraits.length === 0) {
          console.warn(`Aucun extrait trouvé pour l’interview ${video.uuid}`);
          return null;
        }

        const firstExtrait = extraits[0];
        return (
          firstExtrait.url_miniature_yt ||
          (await firstExtrait.get_url_miniature_vimeo())
        );
      } catch (err) {
        console.error("Erreur lors de la récupération de la miniature :", err);
        return null;
      }
    },

    async get_duree(video) {
      function format_duree(duree_seconds) {
        const hours = Math.floor(duree_seconds / 3600);
        const minutes = Math.floor((duree_seconds % 3600) / 60);
        const seconds = duree_seconds % 60;

        let formatted = "";
        if (hours > 0) formatted += String(hours).padStart(2, "0") + ":";
        formatted += String(minutes).padStart(2, "0") + ":";
        formatted += String(seconds).padStart(2, "0");

        return formatted;
      }

      let time = 0;
      try {
        if (video.extraits) {
          // Si c’est une interview
          const extraits = await video.extraits;
          for (let extrait of extraits) {
            time += extrait.duree;
          }
        } else {
          // Si c’est un extrait
          time = video.duree;
        }
      } catch (err) {
        console.error("Erreur dans get_duree :", err);
      }

      return format_duree(time);
    },

    async update_miniature(){
      this.url = await this.get_miniature(this.video);
      this.duree = await this.get_duree(this.video);
    }
  },

  watch: {
    video: {
      deep: true,
      immediate: true,
      handler() {
        this.update_miniature();
      }
    }
  }

};
</script>

<style scoped>
.miniature-wrapper {
  position: relative;
  display: inline-block;
  width: 50%;
}

.miniature-wrapper img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 11px;
  object-fit: cover;
  background-color: var(--gris-moyen);
}

/* Le temps en bas à gauche de l’image */
.duree {
  position: absolute;
  bottom: -5px;
  right: 8px;
  color: white;
  font-size: 0.8rem;
  background: rgba(0, 0, 0, 0.6);
  padding: 2px 6px;
  border-radius: 4px;
}
</style>

