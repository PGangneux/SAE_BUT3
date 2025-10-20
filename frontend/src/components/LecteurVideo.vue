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
        <div id="bottom-iframe">
          <h2>Title</h2>
          <div class="right-content">
            <a>Voir toute l’interview</a>
            <button>Paramètres</button>
            <button>PIP</button>
          </div>
        </div>

        <div id="description">
          <p>Video description</p>
        </div>
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

#bottom-iframe {
  display: flex;
  justify-content: space-between; /* <-- sépare gauche / droite */
  align-items: center;             /* <-- aligne verticalement */
  width: 100%;
  padding: 0 0.5rem;
  box-sizing: border-box;
  margin-top: 2%;
}

#bottom-iframe h2 {
  margin: 0;
}

#bottom-iframe .right-content {
  display: flex;
  align-items: center;
  gap: 0.5rem; /* espace entre les éléments à droite */
}

#bottom-iframe a {
  color: var(--vert-neon);
  text-decoration: underline;
  cursor: pointer;
}

#description {
  margin-top: 2%;
  background-color: var(--gris-foncer);
  border: var(--gris-foncer);
  border-radius: 20px;
  padding: 1rem;
  box-sizing: border-box;
}


aside {
  flex: 2.2;
  background-color: var(--gris-moyen);
  border-left: 3px solid var(--gris-taupe);
}


</style>
