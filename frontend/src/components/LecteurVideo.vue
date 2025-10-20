<script>
import IframeLectureVideo from './IframeLectureVideo.vue';
import BarListeVideo from "./BarListeVideo.vue";

export default {
  components: {
    IframeLectureVideo,
    BarListeVideo
  },
  methods: {
    parametresVideo() {
      // Logique pour les paramètres vidéo
      print("parametresVideo");
    },
    pictureInPicture() {
      // Logique pour le mode Picture-in-Picture
      print("pictureInPicture");
    }

  }

};

</script>

<template>
  <main>
    <IframeLectureVideo url="https://www.youtube.com/embed/10MZrDXjby8" />
    <div>
      <h2>Title</h2>
      <div>
        <p>Video description</p>
      </div>
    </div>
  </main>
  <aside>
    <BarListeVideo />
  </aside>
</template>
