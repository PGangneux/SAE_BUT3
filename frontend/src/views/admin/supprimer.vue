<script>
import { markRaw } from 'vue';
import Extrait from "../../model/extrait";
import Interview from "../../model/interview";
import Utilisateur from "../../model/utilisateur.js";


export default {
    name: "components_supprimer",

    props: {
        Element_Supp: {
            type:Object,
        }
    },

    data() {
        return {
            ObjectType:null,
            liste_possible:["extrait","interview","utilisateur"]
        };
    },  
    
    computed: {
      nametype: {
        get() {
          return this.current_object ? this.current_object.name : 'Chargement...';
        },
      },
    },


    methods: {
        async deleteElement() {
            await this.Element_Supp.delete();
            this.$router.push("/admin/interview");
            
        }
    },


    async mounted() {
        console.log(this.Element_Supp)

        

    },


};



</script>

<template>
    <div class="overlay">

    
        <div class="popup">

            <h1> Voulez vous vraiment supprimer {{ nametype }}  </h1>
            <RouterLink class="col bt button-blanc"> Annuler </RouterLink>
            <button @click="deleteElement()" class="col bt button-blanc">Valider</button>
        </div>
    </div>

</template>

<style scoped>
.button-blanc{
    background-color: var(--blanc);
}

</style>
