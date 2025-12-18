<script>
import { markRaw, toRaw } from 'vue';
import Extrait from '../../model/extrait';
import { videoStore } from "../../model/videoStore";
import miniature_video from "./miniature_video.vue";
import ClientAPI from '../../model/clientAPI';
import Interview from '../../model/interview';


// Todo ajouter gif de chargement pendant le fetch des vidéos

export default {
  components: { miniature_video, },
  emits: ["toggle_aside", 'update'],
  inject: ["extrait_current", "interview_current"],
  props: {
    liste_extraits_current_interview: {
      type: Object,

    }
  },
  data() {
    return {
      videos: null,
      selected: "",
      img_close: true,
      extrait: null,
      interview: null,
      page: 0,

    };
  },

  methods: {
    /**
     * Génère un dictionnaire de poids selon le chemin d'entrée de l'utilisateur.
     * les poids sont plus lourd au debut du chemin.
     *
     * @param {Array} chemin - liste représentant le chemin d'entrée de l'utilisateur
     * @return {Dict} Dictionnaire des poids pour les recommandations
    */
    get_reco_weights(chemin) {
      const weights = {};
      console.log("bar_list_video get_reco_weights", chemin);

      chemin.forEach((value, index, array) => {
        console.log("bar_list_video get_reco_weights", value);
        weights[value.constructor.mmch_dbjsclass.name] = array.length - index;
      });
      return weights;
    },


    // À déplacer
    async current_reco() {
      if (this.selected != "reco") {
        this.page = 0
        this.selected = "reco";
        this.videos = []
      }
      // Feature-flag de l'algorithme de recommandation
      if (true) {
        const video = this.extrait ? this.extrait.uuid : this.interview ? this.interview.uuid : null;
        // TODO Nécessite d'enregistrer et modifier les poids à chaque fois
        let weights;
        if (false) {
          weights = localStorage.getItem('weights');
          weights = weights ? JSON.parse(weights) : this.get_reco_weights(videoStore.chemin);
          localStorage.setItem('weights', JSON.stringify(weights));
        }
        else {
          weights = this.get_reco_weights(videoStore.chemin);
        }
        this.videos = this.videos.concat(
          markRaw(
            await ClientAPI.post(
              `${ClientAPI.BASE_URL}api/recommandations`,
              JSON.stringify({ 'weights': weights }),
              ClientAPI.current_user ? true : false,
              video ? { 'video': video, 'size': 10, 'page':this.page } : null
            )
              .then(
                json => {
                  return json.map(
                    (v) => {
                      if (v.type == 'Extrait') { return markRaw(new Extrait(v.value)); }
                      else { return markRaw(new Interview(v.value)); }
                    }
                  );
                }
              )
          )
        );
      }
      else {
        this.videos = markRaw(await Extrait.list({ size: 10 })); // récupère les 10 derniers extraits/interviews
      }
      console.log('vidéo', this.videos);
    },




    async interview_current_extrait() {
      this.selected = "playlists"
      this.videos = markRaw(await this.extrait.interviews())
    },


    async extraits_current_question() {
      if (this.selected != "questions") {
        this.page = 0
        this.selected = "questions"
        this.videos = []
      }
      const video = this.extrait ? this.extrait.uuid : this.interview ? this.interview.uuid : null;
      // TODO Nécessite d'enregistrer et modifier les poids à chaque fois
      let weights;
      if (false) {
        weights = localStorage.getItem('weights');
        weights = weights ? JSON.parse(weights) : this.get_reco_weights(videoStore.chemin);
        localStorage.setItem('weights', JSON.stringify(weights));
      }
      else {
        weights = this.get_reco_weights(videoStore.chemin);
      }
      const question = markRaw(await this.extrait.question);
      this.videos = this.videos.concat(
        markRaw(
          await ClientAPI.post(
            `${ClientAPI.BASE_URL}api/recommandations`,
            JSON.stringify({ 'weights': weights, 'filters': { 'Question': question.uuid } }),
            ClientAPI.current_user ? true : false,
            video ? { 'video': video, 'size': 10, 'page':this.page } : null
          )
            .then(
              json => {
                return json.map(
                  (v) => {
                    if (v.type == 'Extrait') { return markRaw(new Extrait(v.value)); }
                    else { return markRaw(new Interview(v.value)); }
                  }
                );
              }
            )
          )
        );
    },

    async extraits_interviews_current_artiste() {
      if (this.selected != "artiste") {
        this.page = 0
        this.selected = "artiste";
        this.videos = []
      }
      const video = this.extrait ? this.extrait.uuid : this.interview ? this.interview.uuid : null;
      // TODO Nécessite d'enregistrer et modifier les poids à chaque fois
      let weights;
      if (false) {
        weights = localStorage.getItem('weights');
        weights = weights ? JSON.parse(weights) : this.get_reco_weights(videoStore.chemin);
        localStorage.setItem('weights', JSON.stringify(weights));
      }
      else {
        weights = this.get_reco_weights(videoStore.chemin);
      }
      const artiste = markRaw(await this.extrait.artiste);
      this.videos = this.videos.concat(
        markRaw(
          await ClientAPI.post(
            `${ClientAPI.BASE_URL}api/recommandations`,
            JSON.stringify({ 'weights': weights, 'filters': { 'Artiste': artiste.uuid } }),
            ClientAPI.current_user ? true : false,
            video ? { 'video': video, 'size': 10, 'page':this.page } : null
          )
            .then(
              json => {
                return json.map(
                  (v) => {
                    if (v.type == 'Extrait') { return markRaw(new Extrait(v.value)); }
                    else { return markRaw(new Interview(v.value)); }
                  }
                );
              }
            )
            )
        );

    },

    async extrait_current_theme() {
      if (this.selected != "thèmes") {
        this.page = 0
        this.selected = "thèmes"
        this.videos = []
      }
      const video = this.extrait ? this.extrait.uuid : this.interview ? this.interview.uuid : null;
      // TODO Nécessite d'enregistrer et modifier les poids à chaque fois
      let weights;
      if (false) {
        weights = localStorage.getItem('weights');
        weights = weights ? JSON.parse(weights) : this.get_reco_weights(videoStore.chemin);
        localStorage.setItem('weights', JSON.stringify(weights));
      }
      else {
        weights = this.get_reco_weights(videoStore.chemin);
      }
      const question = markRaw(await this.extrait.question);
      const theme = markRaw(await question.theme);
      this.videos = this.videos.concat(
        markRaw(
          await ClientAPI.post(
            `${ClientAPI.BASE_URL}api/recommandations`,
            JSON.stringify({ 'weights': weights, 'filters': { 'Thème': theme.uuid } }),
            ClientAPI.current_user ? true : false,
            video ? { 'video': video, 'size': 10, 'page':this.page } : null
          )
            .then(
              json => {
                return json.map(
                  (v) => {
                    if (v.type == 'Extrait') { return markRaw(new Extrait(v.value)); }
                    else { return markRaw(new Interview(v.value)); }
                  }
                );
              }
            )
          )
        );
    },




    async update_liste_video(video) {
      console.log("update liste videp");
      // maj du extrait_current ou interview_current selon le type de video

      if (video.extraits) {
        // c'est une interview
        /// console.log(video)
        this.interview_current.set(video);


        ///console.log((await video.extraits)[0])
        this.extrait_current.set((await video.extraits())[0]);
      } else {
        // c'est un extrait
        this.extrait_current.set(video);
        this.interview_current.set(null);
      }
      // recupération des nouveau extrait et interview
      this.extrait = await this.extrait_current.get();
      this.interview = await this.interview_current.get();



      // reset du videoStore
      videoStore.isPlaying = true;
      clearInterval(videoStore.intervalId);
      videoStore.intervalId = null;
      videoStore.currentTime = 0;

      this.$emit('update');

      //update bar liste video
      this.selected = '';
      console.log("this.current_reco test") 
      await this.current_reco()
      console.log("after update video reco", this.videos)

      this.$refs.miniature_videos.forEach(child => {
        child.update_miniature();
      });

      
    },

    async plus_video() {
      this.page++;
      switch (this.selected) {
        case 'reco': await this.current_reco(); break;
        case 'questions': await this.extraits_current_question(); break;
        case 'artiste': await this.extraits_interviews_current_artiste(); break;
        case 'thèmes': await this.extrait_current_theme(); break;
      }

    },

  },
  async mounted() {
    this.interview = toRaw(await this.interview_current.get());
    this.extrait = toRaw(await this.extrait_current.get());
    this.current_reco();
    if (this.interview) this.img_close = false;


  },

};

</script>

<template>
  <header>
    <nav class="header-nav">
      <ul class="menu">
        <li @click="current_reco" :class="{ selected: selected === 'reco' }">Recomendation</li>
        <!--si la video est un extrait-->
        <li v-if="this.interview === null" @click="extraits_interviews_current_artiste"
          :class="{ selected: selected === 'artiste' }">Artiste</li>
        <li v-if="this.interview === null" @click="extraits_current_question"
          :class="{ selected: selected === 'questions' }">Questions</li>
        <li v-if="this.interview === null" @click="extrait_current_theme" :class="{ selected: selected === 'thèmes' }">
          Thèmes</li>
        <li v-if="this.interview === null" @click="interview_current_extrait"
          :class="{ selected: selected === 'playlists' }">Playlists</li>

      </ul>

      <img v-if="img_close" src="/imgs/close.svg" alt="close" @click="this.$emit('toggle_aside')">
    </nav>

  </header>
  <main>
    <div>
      <div>
        <ul class="liste_video">
          <li v-for="(video) in videos" :key="video.uuid">
            <div>
              <miniature_video ref="miniature_videos" @click="update_liste_video(video)" :video="video" />
              <div class="video_text">
                <h4>{{ video.titre }}</h4>
                <p>{{ video.description }}</p>

              </div>
            </div>
          </li>
        </ul>
        <button @click="plus_video()">plus de video ...</button>
      </div>
    </div>
  </main>

</template>

<style scoped>
header,
main {
  background-color: var(--gris-foncer);
  padding: 0 0.5rem;
}

header {
  border-bottom: 1px solid var(--blanc);
  height: 5%;
  display: flex;
  align-items: center;
  /* centre verticalement */
}

main {
  height: 64%;
  /* 100-5(header)-30(timecode)-1 */
  flex-grow: 1;
  /* permet à main de prendre tout l'espace restant */
  overflow-y: auto;
  /* permet le scroll vertical */
}

.header-nav {
  width: 100%;
  display: flex;
  justify-content: space-between;
  /* menu à gauche, bouton X à droite */
  align-items: center;
  /* centre verticalement */

}

.header-nav>img {
  width: 6%;
  height: 6%;


  cursor: pointer;

}



.menu {
  display: flex;
  /* aligne les <li> horizontalement */
  list-style: none;
  /* supprime les puces */
  gap: 1rem;
  /* espace entre les items */
  margin: 0;
  padding: 0;
}

.menu li {
  cursor: pointer;
}

.selected {
  color: var(--vert-neon);
}



.close-btn {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
}

.search-bar {
  width: 100%;
  display: flex;
}

.search-bar input {
  width: 85%;
  height: 2rem;
  border: none;
  border-radius: 20px;
  padding-left: 2%;
  margin-right: 2%;
}



.liste_video {
  margin: 0;
  padding: 0;
  cursor: pointer;
  display: flex;
  gap: 10px;
  flex-direction: column;
}

.liste_video li>div {
  list-style: none;
  display: flex;
}



.liste_video a {
  width: 55%;
  height: 55%;
  margin-right: 1em;
  margin-bottom: 2em;
}

.video_text {
  padding-right: 5%;
  flex-grow: 1;
}

p,
h4 {
  margin: 0;
}
</style>
