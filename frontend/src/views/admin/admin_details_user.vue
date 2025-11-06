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

    <h1 class="text-center colorneon"> Éditer un Compte  </h1>

    <form action="" class="grisee" style="padding: 1em;">
        <div class="row client">
            <div class="row client">

                <div class="input-group mb-3 col">
                    <label class="row client" for="Pseudo"> Pseudo </label>
                    <input type="text" class="form-control" id="Pseudo" name="Pseudo" placeholder="Pseudo" v-model="this.current_utilisateur.pseudo" >
                </div>

                <div class="input-group mb-3 col">
                    <label class="row client" for="Prénom">Prénom</label>
                    <input type="text" class="form-control row client" id="Prénom" name="Prénom" placeholder="Prénom" v-model="this.current_utilisateur.prenom" >
                </div>

            </div>

            <div class="row client">


                <div class="input-group mb-3 col">
                    <label class="row client" for="Nom">Nom</label>
                    <input type="text" class="form-control row client" id="Nom" name="Nom" placeholder="Nom" v-model="this.current_utilisateur.nom">
                </div>

                <div class="input-group mb-3 col">
                    <label class="row client" for="Adresse">Adresse</label>
                        <input type="text" class="form-control row client " id="Adresse" name="Adresse" placeholder="Adresse e-mail" v-model="this.current_utilisateur.email" >
                </div>

            </div>
        </div>
        <div class="row client">

            <button  type="button"   class=" btn btred col" > <img src="/imgs/delete.svg" alt="Supprimer"> Supprimer </button>
            <button  type="submit"   class="bt btn col" > <img src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>
            <button  type="reset"  class="bt btn col" > <img src="/imgs/cancel.svg" alt="Annuler"> Annuler </button>
        </div>
    </form>

    <h2 class="text-center colorneon"> Details Utilisateur {{ pseudo }} </h2>


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

        <form class="row" style=" margin-left: 0 !important; margin-right: 0 !important; padding: 1em;" action="">
            <button  type="button"   class=" btn btred col" > <img src="/imgs/delete.svg" alt="Supprimer"> Supprimer Historique </button>
        </form>


        </div>


    </template>

<style scoped>

.bt{
    color: var(--blanc);
    background-color:var(--vert-pale);
    border-radius: 2em;
    
}

h2{
    margin-top: 1em;
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
    min-width: 5em;
}

.colorneon{
  color: var(--vert-neon);
}


</style>
