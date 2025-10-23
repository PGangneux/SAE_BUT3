<script>
import { markRaw } from 'vue';
import { prefetcher } from "../../model/prefetcher";

export default {
  data() {
    return {
      extraits: null
    };
  },




  async mounted() {
    this.extraits = markRaw(await prefetcher.extrait_all());
    console.log("liste des extrait")
    console.log(this.extraits)

    
  },

};

</script>

<template>
    <header>
        <nav class="header-nav">
            <ul class="menu">
            <li>questions</li>
            <li>Auteurs</li>
            <li>Thèmes</li>
            </ul>
            <img src="/imgs/close.png" alt="close" @click="this.$emit('toggle_aside')">
        </nav>

    </header>
    <main>
        <div>
            <h2>{{ titreSideBar }}</h2>
            <div class="search-bar">
                <input type="text" :placeholder=" placeholderRecherche "/>
                <img src="/imgs/Search.png" alt="loupe"/>
            </div>
            <div>
                <ul class="liste_video">
                    <li v-for="extrait in extraits">
                        <router-link :to="`/lecteur_video/${extrait.uuid}`">
                          <img :src="extrait.url_miniature_yt" :alt="extrait.titre"/>
                        </router-link>
                        <div>
                            <h4>{{ extrait.titre }}</h4>
                            
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
}

main {
  height: 95%; /* le reste de la page */
  overflow-y: auto; /* permet le scroll vertical */
}
.header-nav {
  display: flex;
  justify-content: space-between; /* menu à gauche, bouton X à droite */
  align-items: center;            /* centre verticalement */
  
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

.search-bar img {
  width: 9%;
  cursor: pointer;
}

.liste_video {
  margin: 0;
  padding: 0;
  cursor: pointer;
}

.liste_video li {
  list-style: none;
  display: flex;
  
}

.liste_video img, .liste_video a{
  display: block;
  width: 100%;
  height: 100%;

  border-radius: 20px;
  object-fit: cover;
  background-color: var(--gris-moyen);
}

.liste_video a{
    width: 55%;
    height: 55%;
    margin-right: 1em;
    margin-bottom: 2em;
}




</style>
