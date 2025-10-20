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
      console.log("parametresVideo");
    },
    pictureInPicture() {
      console.log("pictureInPicture");
    },
  }
};
</script>

<template>
  <div class="layout">
    <main>
      <IframeLectureVideo url="https://www.youtube.com/embed/10MZrDXjby8" />
      <div>
        <h2>Title</h2>
        <a>Voir toute l’interview</a>
        <button @click="parametresVideo">Paramètres</button>
        <button @click="pictureInPicture">PIP</button>
      </div>
      <div>
        <p>Video description</p>
      </div>
    </main>

    <aside>
      <BarListeVideo />
    </aside>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  height: 100%;
  width: 100%;
}

main {
  flex: 5;
  background-color: var(--background-color);
  padding: 1rem;
  box-sizing: border-box;

  display: flex;
  flex-direction: column;
  margin: 0 auto; /* centre horizontalement */
  width: 83%;
  height: 93%;
  border-radius: 8px;
  padding-left: 2%;
  padding-right: 2%;
}


main > div {
  flex: 1;
}

aside {
  flex: 2.2;
  background-color: #4C4C4C;
}
</style>
