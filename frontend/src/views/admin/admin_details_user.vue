<script>

import { markRaw } from 'vue';
import comp_baradmin from "../../components/components_admin/nav_admin.vue";
import User from "../../model/utilisateur.js";
import Tags from '../../model/tag.js';

export default {
  name: "page_admin_details_client",
  components: {
    comp_baradmin,
  },data() {
        return {
            current_utilisateur : {type:User},
            tags:{type:Tags},
    };
  },    
  async mounted() {
        const utilisateurId = this.$route.params.id;
        this.current_utilisateur = markRaw(await User.detail(utilisateurId));
        this.tags = markRaw(await Tags.list())

    },
};



</script>

<template>
    <comp_baradmin/>

    <h1 class="text-center colorneon"> Details Utilisateur {{ pseudo }} </h1>


        <div class="row grisee" style=" margin-left: 0 !important; margin-right: 0 !important;">
            <div class="row " style=" margin-left: 0 !important; margin-right: 0 !important;">
                <div class=" col test">
                    <p> Nom: {{ this.current_utilisateur.nom }}</p>
                </div>

                <div class="col test">
                    <p> Prénom: {{ this.current_utilisateur.prenom }}</p>
                </div>
            </div>

            <div class="row" style=" margin-left: 0 !important; margin-right: 0 !important;">
                <div class="col " style="background-color: var(--gris-taupe); margin: 1%;">
                    <p class="row pcentrer">details non definie</p>


                </div>

                <div class="col " style="background-color:var(--gris-taupe); margin: 1%;">
                    <p class="row pcentrer">Tag User</p>
                    <ul class="scroller ultagger row tagsfully">
                        <li class="col" v-for="tag in this.tags">
                            <button class="btn btn-primary"> {{ tag.name }} </button>
                        </li>
                    </ul>

                </div>
            </div>


        </div>

        <form class="row" style=" margin-left: 0 !important; margin-right: 0 !important;" action="">
            <button  type="button"   class=" btn btred col" > <img src="/imgs/delete.svg" alt="Supprimer"> Supprimer Historique </button>
            <RouterLink class="bt btn col" :to="'/admin/user/edit/' +this.current_utilisateur.uuid ">
                <button  type="button"   class=" btn col" >
                    <img src="/imgs/save.svg" class="col" alt="Modifier">   
                    Modifier Utilisateur
                </button>  

            </RouterLink>
        </form>


    
    </template>

<style scoped>

.bt{
    color: var(--blanc);
    background-color:var(--vert-pale);
    border-radius: 2em;
    
}

.btred{
    color: var(--blanc);
    background-color:var(--rouge);
    border-radius: 2em;
    
}

.grisee{
  background-color: var(--gris-moyen);
}

label{
    color: var(--blanc);
}

.colorneon{
  color: var(--vert-neon);
}


.pcentrer{
    margin-top: 1em;
    margin-bottom: 1em;
    justify-content: center
}


.ultagger {
    list-style-type: none;

}

.tagsfully{
    width: 100%;
    height:100%;
}


.test{
    margin: 1%;
  text-align: center;
}

</style>
