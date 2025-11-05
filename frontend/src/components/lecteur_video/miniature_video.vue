<template>
  <img v-if="url" :src="url" :alt="video.titre" />
</template>

<script>
export default {
  props: ["video"],
  data() {
    return { url: null };
  },
  async mounted() {
    /// //console.log("Mounted miniature_video for video:", this.video.uuid);
    this.url = await this.get_miniature(this.video);
    /// //console.log("Miniature URL:", this.url);
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
        }

  }
};
</script>
