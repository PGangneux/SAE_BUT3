<script>
import { markRaw } from 'vue';
import comp_baradmin from "../../../components/components_admin/nav_admin.vue";

import User from "../../../model/utilisateur.js";

export default {
  name: "page_admin_edit_client",
  components: {
    comp_baradmin,

  }, data() {
        return {
            utilisateur:{type:User},
        };
    },
  
    async mounted() {
        const utilisateurId = this.$route.params.id;
        this.utilisateur = markRaw(await User.detail(utilisateurId));
    },
};



</script>

<template>
    <comp_baradmin/>

    <h1 class="text-center colorneon"> Éditer un Compte  
    <RouterLink  class="bt" style="text-decoration: none; color: inherit; color: var(--blanc); font-size: 0.5em; padding: 0.5em 0.1em;" :to="{path:'/admin/user/'+ utilisateur.uuid}"> retour </RouterLink>

    </h1>
    
    <form action="">
        <div class="row client">
            <div class="row client">

                <div class="input-group mb-3 col">
                    <label class="row client" for="Pseudo"> Pseudo </label>
                    <input type="text" class="form-control" id="Pseudo" name="Pseudo" placeholder="Pseudo" v-model="this.utilisateur.pseudo" >
                </div>

                <div class="input-group mb-3 col">
                    <label class="row client" for="Prénom">Prénom</label>
                    <input type="text" class="form-control row client" id="Prénom" name="Prénom" placeholder="Prénom" v-model="this.utilisateur.prenom" >
                </div>

            </div>

            <div class="row client">


                <div class="input-group mb-3 col">
                    <label class="row client" for="Nom">Nom</label>
                    <input type="text" class="form-control row client" id="Nom" name="Nom" placeholder="Nom" v-model="this.utilisateur.nom">
                </div>

                <div class="input-group mb-3 col">
                    <label class="row client" for="Adresse">Adresse</label>
                        <input type="text" class="form-control row client " id="Adresse" name="Adresse" placeholder="Adresse e-mail" v-model="this.utilisateur.email" >
                </div>

            </div>
        </div>
        <div class="row client">

            <button  type="button"   class=" btn btred col" > <img src="/imgs/delete.svg" alt="Supprimer"> Supprimer </button>
            <button  type="submit"   class="bt btn col" > <img src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>
            <button  type="reset"  class="bt btn col" > <img src="/imgs/cancel.svg" alt="Annuler"> Annuler </button>
        </div>
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

.client{
    margin-right:0px;
    margin-left:0px;
}

label{
    color: var(--blanc);
    text-align: center;
    justify-content: center;
    align-content: center;
    padding-right: 1em;
}

.colorneon{
  color: var(--vert-neon);
}

</style>
