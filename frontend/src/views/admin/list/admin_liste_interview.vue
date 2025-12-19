<script>
/**
 * Page d'administration des playlists (interviews)
 * - Affiche la liste des interviews
 * - Permet une recherche par titre
 * - Calcule dynamiquement le nombre d'extraits et la durée
 */
import { markRaw, nextTick } from 'vue';
import Interview from '../../../model/interview.js';
import Model from "../../../model/model.js";

import comp_baradmin from "../../../components/components_admin/nav_admin.vue";
import {parseAndImport} from "../../../model/parse_csv.js"

export default {
    name: "page_admin_interview",
    components: {
        comp_baradmin,

    }, data() {
        return {
            allInterviews: [],  // Liste complète des interviews 
            /**
             * Dictionnaire indexé par uuid d'interview
             * Contient :
             *  - length : nombre d'extraits
             *  - tags   : tags associés
             *  - duree  : durée formatée
             */
            dico_interviews: {},
            search: ""  // Texte de recherche (filtrage par titre) 
        };
    },



    /**
    * Hook appelé après le montage du composant
    * - Récupère la liste des interviews
    * - Calcule les métadonnées associées
    */
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
        /**
         * Retourne la liste des interviews filtrées
         * selon le texte de recherche (insensible à la casse)
         *
         * @returns {Array}
         */
        interviewsFiltrees() {
            if (!this.search) return this.allInterviews;

            return this.allInterviews.filter(inter =>
                inter.titre.toLowerCase().includes(this.search.toLowerCase())
            );
        }
    },

    methods: {
        /**
         * Convertit un tableau de tags en chaîne de caractères
         *
         * @param {Array} tags_array - Liste des tags
         * @returns {String} Chaîne de tags séparés par des espaces
         */
        tags_to_string(tags_array) {
            let string_tags = "";
            for (let tag of tags_array) {
                string_tags += tag.name + " ";
            }
            return string_tags.trim();
        },


        importCSV() {
            this.$refs.csvInput.click();
        },

        async handleFile(event) {
            const file = event.target.files[0];
            if (!file) return;

            // Lire le contenu du fichier
            const text = await file.text();

            let test = await parseAndImport(text)
            console.log(test)

            // const reader = new FileReader();
            // reader.onload = (e) => {
            //     const csv = e.target.result;
            //     console.log(csv); // contenu du CSV
            // };
            // reader.readAsText(file);
        }


    },
};
</script>

<template>

    <comp_baradmin />

    <div class="main">


        <h1 class="text-center">Playlists</h1>


        <div class="header">
            <div class="search-wrapper">
                <div class="input-group input-group-sm">
                    <input v-model="search" type="text" class="form-control" placeholder="Titre d'une playlist..."
                        aria-label="Search" list="interviewData">
                    <datalist id="interviewData">
                        <option v-for="inter in allInterviews" :key="inter.uuid" :value="inter.titre" />
                    </datalist>
                </div>
            </div>


            <button @click="importCSV">Importer un CSV</button>
            <input
                type="file"
                ref="csvInput"
                accept=".csv"
                style="display: none"
                @change="handleFile"
            />

            <RouterLink to="/admin/interview/creer/" class="btn btn-outline-light btn-add">
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
                                <RouterLink class="container container_extrait"
                                    :to="`/admin/interview/${interview.uuid}`">
                                    {{ interview.titre }}
                                </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container container_extrait"
                                    :to="`/admin/interview/${interview.uuid}`">
                                    {{ dico_interviews[interview.uuid]?.length }}
                                </RouterLink>
                            </td>
                            <td>
                                <RouterLink class="container container_extrait"
                                    :to="`/admin/interview/${interview.uuid}`">
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
.main {
    margin: 2%;
}

.btgrisv2 {
    color: white;
    background-color: var(--gris-moyen);
    padding: 1em;
}



.aggrandir {
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

tr {
    height: 50px;
}

td {
    height: 50px;
}

.table-scroll {
    display: block;
    max-height: 40vh;
    /* hauteur de la zone scrollable */
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

tr a {
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
    max-width: 300px;
    /* taille réduite */
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
