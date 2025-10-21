<script>

export default {
  data() {
    return {
        videos : {
            id: 1,
            title: "Titre de la vidéo",
            thumbnail: "lien_vers_la_miniature.jpg"
        },
        titreSideBar: "Question en cours",
        placeholderRecherche: "Rechercher une vidéo"
    }
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
            <img src="../../..//imgs/Close.png" alt="close">
        </nav>

    </header>
    <main>
        <div>
            <h2>{{ titreSideBar }}</h2>
            <div class="search-bar">
                <input type="text" :placeholder=" placeholderRecherche "/>
                <img src="../../..//imgs/Search.png" alt="loupe"/>
            </div>
            <div>
                <ul>
                    <li v-for="video in videos" :key="video.id">
                        <img :src="video.thumbnail" :alt="video.title"/>
                        <div>
                            <h3>{{ video.title }}</h3>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </main>

</template>

<style scoped>
header, main{
    background-color: var(--gris-moyen);
    padding: 0 1rem;
    
    
}

header{
    border-bottom: 1px solid var(--blanc);
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


</style>
