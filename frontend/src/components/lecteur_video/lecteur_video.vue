<script>
import iframe_lecture_video from './iframe_lecture_video.vue';
import bar_liste_video from "./bar_liste_video.vue";

export default {
  components: {
    iframe_lecture_video,
    bar_liste_video
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
      <iframe_lecture_video url="https://www.youtube.com/embed/10MZrDXjby8" />
      <div>
        <div id="bottom-iframe">
          <h2>Title</h2>
          <div class="right-content">
            <a>Voir toute l’interview</a>
            <img src="../../..//imgs/Settings.png" alt="Paramètres">
            <img src="../../..//imgs/affichage_lecteur_réduit.png" alt="Paramètres">
          </div>
        </div>

        <div id="description">
          <p>Video description</p>
        </div>
      </div>
    </main>

    <aside>
      <bar_liste_video/>
    </aside>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  width: 100vw;
  height: 100vh;
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
