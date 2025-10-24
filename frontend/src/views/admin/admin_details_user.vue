<script>

import comp_baradmin from "../../components/components_admin/nav_admin.vue";


export default {
  name: "page_admin_details_client",
  components: {
    comp_baradmin,
  },data() {
        return {
            pseudo:"kilemonnar",
            nom:"crap",
            prenom:"timeo",
    };
  },
};



</script>

<template>
    <comp_baradmin/>

    <h1 class="text-center colorneon"> Details Utilisateur {{ pseudo }} </h1>
        <div class="row">
            <div class="row">
                <div class="input-group mb-3 col">
                    <p> Nom:{{ nom }}</p>
                </div>

                <div class="input-group mb-3 col">
                    <p> Prénom:{{ prenom }}</p>
                </div>
            </div>
        </div>

        <form class="row" action="">
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



label{
    color: var(--blanc);
}

.colorneon{
  color: var(--vert-neon);
}

</style>
