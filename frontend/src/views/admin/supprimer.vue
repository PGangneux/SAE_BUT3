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


    async mounted() {
        

        if (this.Element_Supp == null){
            const ObjectId = this.$route.params.id;
            this.ObjectType = this.$route.params.type;

            if ( this.liste_possible.includes(this.ObjectType) ) {
                    switch (this.ObjectType) {
                        case "extrait":
                            this.current_object =  markRaw(await Extrait.detail(ObjectId));
                            console.log("Extrait")
                        break;

                        case "interview":
                                this.current_object =  markRaw(await Interview.detail(ObjectId));
                                console.log("Interview")
                            break;

                        case "utilisateur":
                                this.current_object =  markRaw(await Utilisateur.detail(ObjectId));
                                console.log("Utilisateur")
                            break;
                    
                        default:
                            console.log("whats")
                            break;
                    }
                
            }else{
                console.log("why")
            }
            

        }

        

    },


};



</script>

<template>

    <h1> Voulez vous vraiment supprimer {{ nametype }}  </h1>

    <form action="" class="row" style="--bs-gutter-x: 0em;">
        <div class="row"  style="--bs-gutter-x: 0em;">
            <RouterLink class="col bt button-blanc" style="text-decoration: none; color: inherit; padding: 1em;" :to="{path: '/admin/'+ ObjectType }"> Annuler </RouterLink>
            <button class="col bt button-blanc">Valider</button>
        </div>
    </form>

    </template>

<style scoped>
.button-blanc{
    background-color: var(--blanc);
}

</style>
