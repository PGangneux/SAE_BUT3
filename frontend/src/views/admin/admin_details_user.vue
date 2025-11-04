<script>

import { markRaw } from 'vue';
import comp_baradmin from "../../components/components_admin/nav_admin.vue";
import User from "../../model/utilisateur.js";


export default {
  name: "page_admin_details_client",
  components: {
    comp_baradmin,
  },data() {
        return {
            current_utilisateur : {type:User},
    };
  },    
  async mounted() {
        const utilisateurId = this.$route.params.id;
        this.current_utilisateur = markRaw(await User.detail(utilisateurId));
        console.log("utilisateur ",current_utilisateur.name)
        console.log(this.current_utilisateur)
    },
};



</script>

<template>
    <comp_baradmin/>

    <h1 class="text-center colorneon"> Details Utilisateur {{ pseudo }} </h1>
        <div class="row grisee" style=" margin-left: 0 !important; margin-right: 0 !important;">
            <div class="row " style=" margin-left: 0 !important; margin-right: 0 !important;">
                <div class=" col">
                    <p> Nom:{{ nom }}</p>
                </div>

                <div class="col">
                    <p> Prénom:{{ prenom }}</p>
                </div>
            </div>

            <div class="row" style=" margin-left: 0 !important; margin-right: 0 !important;">
                <div class="col " style="background-color: var(--gris-taupe); margin: 1%;">
                    <p class="row pcentrer">h1</p>


                </div>

                <div class="col " style="background-color:var(--gris-taupe); margin: 1%;">
                    <p class="row pcentrer">tags</p>

                </div>
            </div>


        </div>

        <form class="row" style=" margin-left: 0 !important; margin-right: 0 !important;" action="">
            <button  type="button"   class=" btn btred col" > <img src="/imgs/delete.svg" alt="Supprimer"> Supprimer Historique </button>
            <button  type="submit"   class="bt btn col" > <img src="/imgs/save.svg" alt="Enregistrer"> Modifier Utilisateur </button>
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

</style>
