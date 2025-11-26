<script>

import { markRaw } from 'vue';
import ClientAPI from "../model/clientAPI.js";
import Utilisateur from "../model/utilisateur.js";


export default {
    name: "page_account",
    data() {
        return {
            current_utilisateur : {type:Utilisateur},
            dico_user:{},
        };
    },
    
    async mounted() {
        this.current_utilisateur = markRaw(await ClientAPI.current_user);

        console.log("affiche",this.current_utilisateur)
    },
};
</script>

<template>

<h1 class="text-center colorneon"> Compte  </h1>

<form action="" class="heit" style="padding: 1em;">
    <div class="row client" style="height: 80%;">
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
                <label class="row client" for="mot de passe">Nouveau Mot De Passe</label>
                <input type="text" class="form-control row client" id="mot de passe" name="mot de passe" placeholder="mot de passe" >
            </div>


        </div>

        <div class="row client">
            <div class="input-group mb-3 col">
                <label class="row client" for="Adresse">Adresse</label>
                    <input type="text" class="form-control row client " id="Adresse" name="Adresse" placeholder="Adresse e-mail" v-model="this.current_utilisateur.email" >
            </div>

            <div class="input-group mb-3 col">
                <label class="row client" for="confirmer mdp">Confirmer Nouveau <br></br> Mot De Passe</label>
                    <input type="text" class="form-control row client " id="confirmer mdp" name="confirmer mdp" placeholder="confirmer mot de passe" >
            </div>
        </div>


    </div>
    <div class="row client" style="height: 10%;">
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

h2{
    margin-top: 1em;
}

.btred{
    color: var(--blanc);
    background-color:var(--rouge);
    border-radius: 2em;
    
}

.heit{
  height: 100%;
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
    min-width: 13em;
}

.colorneon{
  color: var(--vert-neon);
}


</style>