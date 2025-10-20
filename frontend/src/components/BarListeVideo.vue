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
        <nav>
        <ul>
            <li>questions</li>
            <li>Auteurs</li>
            <li>Thèmes</li>
        </ul>
        </nav>
        <button>X</button>
    </header>
    <main>
        <div>
            <h2>{{ titreSideBar }}</h2>
            <div>
                <input type="text" :placeholder=" placeholderRecherche "/>
                <img src="../assets/loupe.png" alt="loupe"/>
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
    background-color: #4C4C4C;
}

</style>
