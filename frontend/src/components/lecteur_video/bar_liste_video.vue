<script>
import { markRaw, toRaw } from 'vue';
import Extrait from '../../model/extrait';
import { videoStore } from "../../model/videoStore";
import miniature_video from "./miniature_video.vue";
import ClientAPI from '../../model/clientAPI';


// Todo ajouter gif de chargement pendant le fetch des vidéos

export default {
  components: { miniature_video, },
  emits: ["toggle_aside", 'update'],
  inject : ["extrait_current", "interview_current"],
  props: {
    liste_extraits_current_interview: {
      type: Object,
      
    }
  },
  data() {
    return {
      videos: null,
      selected : "",
      img_close: true,
      extrait: null,
      interview: null,

    };
  },

  methods : {
    // pour Baptiste peut etre utile
    async get_statistiques_reco(video_regrardees){
      // initialiser les maps de comptage
      this.tags_count.clear();
      this.themes_count.clear();
      this.artistes_count.clear();
      this.questions_count.clear();

      for (const video of video_regardees) {
          // compter les tags
          const tags = await video.tags;
          for (const tag of tags) {
            this.tags_count.set(tag, (this.tags_count.get(tag) || 0) + 1);
          }
          // compter les thèmes
          const themes = await video.themes;
          for (const theme of themes) {
            this.themes_count.set(theme, (this.themes_count.get(theme) || 0) + 1);
          }
          // compter les artistes
          const artistes = await video.artiste;
          for (const artiste of artistes) {
            this.artistes_count.set(artiste, (this.artistes_count.get(artiste) || 0) + 1);
          }
          // compter les questions
          const questions = await video.question;
          for (const question of questions) {
            this.questions_count.set(question, (this.questions_count.get(question) || 0) + 1);
          }
        }
    },

    // pour Baptiste peut etre utile
    sort_stats(){
      // trier les maps de comptage par valeur décroissante
      // exemple pour les tags
      // avant trie
      // this.tags_count = new Map([
      //   ["rock", 12],
      //   ["pop", 5],
      //   ["jazz", 8],
      //   ["electro", 20]
      // ]);
      // après trie
      // this.tags_count = new Map([
      //   ["electro", 20],
      //   ["rock", 12],
      //   ["jazz", 8],
      //   ["pop", 5]
      // ]);


      this.tags_count = new Map([...this.tags_count.entries()].sort((a, b) => b[1] - a[1]));
      this.themes_count = new Map([...this.themes_count.entries()].sort((a, b) => b[1] - a[1]));
      this.artistes_count = new Map([...this.artistes_count.entries()].sort((a, b) => b[1] - a[1]));
      this.questions_count = new Map([...this.questions_count.entries()].sort((a, b) => b[1] - a[1]));
    },


    /**
     * Génère une map de poids selon le chemin d'entrée de l'utilisateur.
     * les poids sont plus lourd au debut du chemin.
     *
     * @param {Array} chemin - liste représentant le chemin d'entrée de l'utilisateur
     * @return {Map} liste des poids pour les recommandations
    */
    get_map_poids_reco(chemin){
      // chemin liste de mmNode
      // représentation d'un mmNode: {categorie: 'artiste', content: artiste1}
      // exemple de chemin : 
      // [{categorie: 'artiste', content: null},{categorie: 'artiste', content: artiste1}, {categorie: 'pays', content: null}, {categorie: 'pays', content: "france"}]

      const map_poids = new Map("artsite", 1, "thème", 1, "question", 1, "tags", 1);
      for (let i = 0; i < chemin.length; i++) {
        const node = chemin[i];
        const poids = chemin.length - i; // poids décroissant
        switch (node.categorie) {
          case 'artiste':
            map_poids.set("artiste", map_poids.get("artiste") + poids);
            break;
          case 'thème':
            map_poids.set("thème", map_poids.get("thème") + poids);
            break;
          case 'question':
            map_poids.set("question", map_poids.get("question") + poids);
            break;
          case 'tags':
            map_poids.set("tags", map_poids.get("tags") + poids);
            break;
          default:
            break;
        }
      }
    },

    get_delta_frequance_extraits(video_regardees){
        const nombre_extraits_regardes = video_regardees.filter(video => !video.extraits).length;
        const nombre_interviews_regardees = video_regardees.length - nombre_extraits_regardes;
        const delta_frequance_extraits = (video_regardees.length - nombre_extraits_regardes) / nombre_interviews_regardees   // rapport extrait/interview regardées

        // on interpole linéairement entre 0 et 1 -> 1 à 4 puis on arrondit pour reotourner un entier
        return Math.round(Math.min(Math.max(4 - 3 * delta_frequance_extraits, 1), 4));
    },

    /**
     * Génère une liste de vidéos selon un ratio interview/extrait
     * dérivé d'un delta compris entre 1 et deltaMax.
     *
     * @param {Map} map_poids - map des poids pour les recommandations
     * @param {Array} video_regardees - liste des vidéos regardées par l'utilisateur
     * @param {number} totalVideos - nombre total de vidéos à générer
     * @param {number} deltaMax - valeur maximale possible du delta (par ex. 4 aujourd’hui)
     */
    async generateVideos(map_poids, video_regardees, totalVideos, deltaMax = 4) {
      const delta_frequance_extraits = this.get_delta_frequance_extraits(video_regardees);

      // ratio linéaire suivant le delta, abstrait !
      const ratioInterview = Math.max(0, deltaMax - delta_frequance_extraits);
      const ratioExtrait   = delta_frequance_extraits;

      nbE = ratioExtrait * Math.floor(totalVideos / (ratioInterview + ratioExtrait));
      nbI = ratioInterview * Math.floor(totalVideos / (ratioInterview + ratioExtrait));

      // fetch des vidéos todo Baptiste
      const liste_extraits = fetchextrait(nbextrait = nbE, map_poids) // récupère x extraits recommander pout l'utilisateur
      const liste_interview =  fetchinterview(nbinterview = nbI, map_poids) // récupère y interviews recommander pour l'utilisateur

      // todo : fusionner les deux listes en respectant le patern interview/extrait

      // création du pattern basé sur le ratio
      const pattern = [
        ...Array(ratioInterview).fill("interview"),
        ...Array(ratioExtrait).fill("extrait")
      ];

      // boucle abstraite
      let indI = 0;
      let indE = 0;
      for (let i = 0; i < totalVideos; i++) {
        const type = pattern[i % pattern.length];
        if (type === "interview") {
          this.videos.push(liste_interview[indI]);
          indI++;
        } else {
          this.videos.push(liste_extraits[indE]);
          indE++;
        }
      }
    },


    async current_reco(){
      // get x derniers Interview/extrait regardés avec un taux de watch time supérieur à 70%
      // proposées proportion interview/extratait en fonction de ce que l'utilisateur regarde le plus
      // si user regarde plus extrait commencé par proposées x extraits, max 4 extrait 1 interview vise versa
      // donc  4 pour 1 max

      // pour choisir extrait/interview on fait classement de tags des x derniers regardés sup 70%
      // + classemnt des thèmes
      // + classement des artistes
      // + classement des questions
      
      // regarder le chemin d'entrée sur le lecteur video
      // si c'est par une playlist on propose plus d'interview
      // si c'est par une question on propose plus d'extrait
      // si c'est par artiste on ajoute un pods sue ce classement des artistes
      // si c'est par thème  on ajoute un pods sue ce classement des thèmes

      // si pas de user ou pas assez de data on propose les video les plus regardé avec un bon watch time

      // todo Baptiste attendre que Baptiste ait fait l'algorithme pour fetcher les vidéos recommander
      if (false){
        current_user = ClientAPI.current_user; // récupère l'utilisateur courant
        if (!current_user) {
          // TODO pas d'utilisateur connecté, on propose les vidéos les plus regardées
          this.videos = markRaw(await Extrait.list({size:10})); // récupère les 10 derniers extraits/interviews
        }
        else{
          // TODO caper le nombre de données récupérées + filtrer celles avec watch time > 70% + récupérer égalment les interviews
          const video_regardees = markRaw(await current_user.regarder_extraits); 

          const map_poids = this.get_poids_reco(videoStore.chemin);

          this.generateVideos(map_poids, video_regardees, 10);

        }
      }
      
        

      this.selected = "reco";
      this.videos = markRaw(await Extrait.list({size:10})); // récupère les 10 derniers extraits/interviews


    },




    async interview_current_extrait(){
      this.selected = "playlists"
      this.videos = markRaw(await this.extrait.interviews)
    },


    async extraits_current_question(){
      this.selected = "questions"
      /// console.log("current extrait:", this.extrait)
      /// console.log(await this.extrait.question.then(question => { return question.extraits}))
      this.videos = markRaw(await this.extrait.question.then(question => { return question.extraits}))
    },

    async extraits_interviews_current_artiste() {
      this.selected = "artiste";

      const artistes_current_video = [];

      if (this.interview) {
        for (const extrait of this.liste_extraits_current_interview) {
          const artiste = await extrait.artiste;
          if (artiste && !artistes_current_video.includes(artiste)) {
            artistes_current_video.push(artiste);
          }
        }
      } else {
        const artiste = await this.extrait.artiste;
        if (artiste) artistes_current_video.push(artiste);
      }

      const extraits_artiste = new Map();
      const interviews_artiste = new Map();

      for (const artiste of artistes_current_video) {
        const extraits_artiste_all = await artiste.extraits;

        for (const un_extrait of extraits_artiste_all) {
          extraits_artiste.set(un_extrait.uuid, un_extrait);

          const interviews_extrait_all = await un_extrait.interviews;
          for (const un_interview of interviews_extrait_all || []) {
            interviews_artiste.set(un_interview.uuid, un_interview);
          }
        }
      }

      const artiste_videos = [
        ...extraits_artiste.values(),
        ...interviews_artiste.values()
      ];

      this.videos = markRaw(artiste_videos);
    },
    



    async update_liste_video(video) {

      // maj du extrait_current ou interview_current selon le type de video

      if (video.extraits) {
        // c'est une interview
        /// console.log(video)
        this.interview_current.set(video);
        

        ///console.log((await video.extraits)[0])
        this.extrait_current.set((await video.extraits)[0]);
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
      
      this.$refs.miniature_videos.forEach(child => {
        child.update_miniature();
      });


      
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
              <li @click="current_reco" :class="{selected: selected === 'reco'}">Recomendation</li>
              <li @click="extraits_interviews_current_artiste" :class="{selected: selected === 'artiste'}">Artiste</li>
              <li @click="" :class="{selected: selected === 'thèmes'}">Thèmes</li>
              <!--si la video est un extrait-->
              <li v-if="this.interview === null" @click="extraits_current_question" :class="{ selected: selected === 'questions' }">Questions</li>
              <li v-if="this.interview === null" @click="interview_current_extrait" :class="{selected: selected === 'playlists'}">Playlists</li>
              
            </ul>
            
            <img v-if="img_close" src="/imgs/close.svg" alt="close" @click="this.$emit('toggle_aside')">
        </nav>

    </header>
    <main>
        <div>
            <div class="search-bar">
                <input type="text" placeholder="placeholderRecherche"/>
                <img src="/imgs/Search.png" alt="loupe"/>
            </div>
            <div>
                <ul class="liste_video">
                    <li v-for="(video) in videos" :key="video.uuid">
                        <div>
                              <miniature_video 
                                ref="miniature_videos" 
                                @click="update_liste_video(video)"
                                :video="video" 
                              />
                          <div class="video_text">
                              <h4>{{ video.titre }}</h4>
                              <p>{{ video.description }}</p>
                              
                          </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </main>

</template>

<style scoped>
header, main{
    background-color: var(--gris-foncer);
    padding: 0 0.5rem;
}

header{
    border-bottom: 1px solid var(--blanc);
    height: 5%;
    display: flex;
    align-items: center;     /* centre verticalement */
}

main {
  height: 64%; /* 100-5(header)-30(timecode)-1 */
  flex-grow: 1; /* permet à main de prendre tout l'espace restant */
  overflow-y: auto; /* permet le scroll vertical */
}
.header-nav {
  width: 100%;
  display: flex;
  justify-content: space-between; /* menu à gauche, bouton X à droite */
  align-items: center;            /* centre verticalement */
  
}

.header-nav > img {
  width: 6%;
  height: 6%;


  cursor: pointer;
  
}



.menu {
  display: flex;       /* aligne les <li> horizontalement */
  list-style: none;    /* supprime les puces */
  gap: 1rem;           /* espace entre les items */
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
  gap : 10px;
  flex-direction: column;
}

.liste_video li > div {
  list-style: none;
  display: flex;  
}



.liste_video a{
    width: 55%;
    height: 55%;
    margin-right: 1em;
    margin-bottom: 2em;
}

.video_text{
  padding-right: 5%;
  flex-grow: 1;
}

p, h4{
  margin: 0;
}





</style>
