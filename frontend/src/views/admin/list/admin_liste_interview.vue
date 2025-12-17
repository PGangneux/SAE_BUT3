<script>
import { markRaw, nextTick} from 'vue';
import Interview from '../../../model/interview.js';
import Model from "../../../model/model.js";

import comp_baradmin from "../../../components/components_admin/nav_admin.vue";


export default {
  name: "page_admin_interview",
  components: {
    comp_baradmin,

  },data() {
        return {
            allInterviews: [],   // liste complète
            dico_interviews:{},
            search: ""           // texte de recherche
        };
    },


  async mounted() {
    this.allInterviews = markRaw(await Interview.list());

    try {
        for (let interview of this.allInterviews) {
            const extraits = await interview.extraits()
            this.dico_interviews[interview.uuid] = {
                "length": extraits.length, 
                "tags": markRaw(await interview.tags()), 
                "duree": Model.format_duree(interview.get_duree(extraits))
            };
        }

    } catch (error) {
      console.error('Erreur lors de la récupération des interviews ou des extraits:', error);
    }
  },
  computed: {
    interviewsFiltrees() {
        if (!this.search) return this.allInterviews;

        return this.allInterviews.filter(inter =>
            inter.titre.toLowerCase().includes(this.search.toLowerCase())
        );
    }
  },
  
  methods: {
    tags_to_string(tags_array) {
        let string_tags = "";
        for (let tag of tags_array){
            string_tags += tag.name + " ";
        }
        return string_tags.trim();
    },


   },
};




</script>

<template>

<comp_baradmin/>

<div class="main">


    <h1 class="text-center">Playlist</h1>


    <div class="header">
        <div class="search-wrapper">
            <div class="input-group input-group-sm">
                <input
                    v-model="search"
                    type="text"
                    class="form-control"
                    placeholder="Titre d'une playlist..."
                    aria-label="Search"
                    list="interviewData"
                >
                <datalist id="interviewData">
                    <option 
                        v-for="inter in allInterviews" 
                        :key="inter.uuid" 
                        :value="inter.titre"
                    />
                </datalist>
            </div>
        </div>

        <RouterLink
            to="/admin/interview/creer/"
            class="btn btn-outline-light btn-add"
        >
            Ajouter une Playlist
            <img src="/imgs/add.svg" alt="add">
        </RouterLink>
    </div>


    <div class="row">
        <div class="col-md-6 aggrandir">
                <table class=" ultagger table  table-bordered">
                    <thead>
                        <tr>
                            <th class="btgrisv2" scope="col">Nom interview</th>
                            <th class="btgrisv2" scope="col">Nombres d'extraits</th>
                            <th class="btgrisv2" scope="col">Durée de l'interview (en minutes)</th>

                        </tr>
                    </thead>
                    <tbody class="table-scroll">
                        <tr v-for="interview in interviewsFiltrees" :key="interview.uuid">
                            <td>
                                <RouterLink class="container container_extrait" :to="`/admin/interview/${interview.uuid}`">
                                    {{ interview.titre }}
                                </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container container_extrait" :to="`/admin/interview/${interview.uuid}`">
                                    {{ dico_interviews[interview.uuid]?.length }}
                                </RouterLink>
                            </td>
                            <td>
                                 <RouterLink class="container container_extrait":to="`/admin/interview/${interview.uuid}`">
                                     {{ dico_interviews[interview.uuid]?.duree }}
                                 </RouterLink>
                            </td>
                        </tr>
                    </tbody>
                </table>
            
        </div>
    </div>

</div>

</template>


<style scoped>
.main{
    margin: 2%;
}

.btgrisv2{
    color:white;
    background-color:var(--gris-moyen);
    padding: 1em;
}



.aggrandir{
  display: flex;
  flex-wrap: nowrap;
  list-style-type: none;
  flex-grow: 1;
  padding-top: 1em;
  padding-bottom: 1em;

}

/* ==== TABLE ==== */

th {
  height: 50px;
}

tr{
    height: 50px;
}

td {
  height: 50px;
}

.table-scroll {
    display: block;
    max-height: 40vh;      /* hauteur de la zone scrollable */
    overflow-y: auto;
    /* Firefox */
    scrollbar-width: none;

    /* IE / Edge */
    -ms-overflow-style: none;
}

/* Chrome / Safari */
.table-scroll::-webkit-scrollbar {
    display: none;
}


.table-scroll tr {
    display: table;
    width: 100%;
    table-layout: fixed;
}

thead tr {
    display: table;
    width: 100%;
    table-layout: fixed;
}

tr a{
    text-decoration: none; 
    color: inherit;
}




/* ===== HEADER ===== */
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.5em;
}

/* ===== SEARCH ===== */
.search-wrapper {
    max-width: 300px; /* taille réduite */
    flex-grow: 1;
}

.input-group-sm input {
    font-size: 0.9rem;
}

.buttonsearch {
    background-color: var(--vert-pale);
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ===== BOUTON AJOUT ===== */
.btn-add {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    white-space: nowrap;
}


</style>

