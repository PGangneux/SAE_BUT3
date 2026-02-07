<script>

import { markRaw } from 'vue';
import ClientAPI from "@model/clientAPI.js";
import Utilisateur from "@model/utilisateur.js";
import edit_success from "./admin/gestion/edit_success.vue"
import edit_error from './admin/gestion/edit_error.vue';

export default {
    name: "page_account",
    components: {
        edit_success,
        edit_error
    },

    data() {
        return {

            current_utilisateur: { type: Utilisateur },
            popupEnregistrer: false,
            popupDelete: false,
            popupSuccess: false,
            popupError: false,
            create: true,
            showPassword: false,
            showNewPassword: false,

        };
    },
    methods: {
        togglePassword() {
            this.showPassword = !this.showPassword;
        },

        toggleNewPassword() {
            this.showNewPassword = !this.showNewPassword;
        }

    },

    
    async mounted() {
        this.current_utilisateur = markRaw(await ClientAPI.current_user);

        console.log("affiche",this.current_utilisateur)
    },
};
</script>

<template>

<h1 class="text-center colorneon"> Compte  </h1>

 <form action="" class="grisee" style="padding: 1em;">
        <div class="row client">
            <div class="row client">

                <div class="input-group mb-3 col">
                    <span class="row input-group-text  colovert client" for="Pseudo"> Pseudo </span>
                    <input type="text" class="form-control" id="Pseudo" name="Pseudo" placeholder="Pseudo"
                        v-model="this.current_utilisateur.pseudo">
                </div>

                <div class="input-group mb-3 col">
                    <span class="row input-group-text client colovert" for="Prénom">Prénom</span>
                    <input type="text" class="form-control row client" id="Prénom" name="Prénom" placeholder="Prénom"
                        v-model="this.current_utilisateur.prenom">
                </div>

            </div>

            <div class="row client">


                <div class="input-group mb-3 col">
                    <span class="row input-group-text  colovert client" for="Nom">Nom</span>
                    <input type="text" class="form-control row client" id="Nom" name="Nom" placeholder="Nom"
                        v-model="this.current_utilisateur.nom">
                </div>

                <div class="input-group mb-3 col">
                    <span class="row input-group-text client colovert" for="Adresse">Adresse</span>
                    <input type="text" class="form-control row client " id="Adresse" name="Adresse"
                        placeholder="Adresse e-mail" v-model="this.current_utilisateur.email">
                </div>
            </div>

            <div class="row client">
                <div class="input-group mb-3 col">
                    <span class="row input-group-text client colovert" for="MDP">MDP</span>

                    <input :type="showPassword ? 'text' : 'password'" class="form-control row client" id="MDP"
                        name="MDP" placeholder="MDP" v-model="this.current_utilisateur.password">
                    <button class="btn btn-outline-secondary colovert" type="button" @click="togglePassword">
                        <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    </button>

                </div>
            </div>

            <div class="row client">
                <div class="input-group mb-3 col">
                    <span class="row input-group-text client colovert" for="MDP">New MDP</span>

                    <input :type="showNewPassword ? 'text' : 'password'" class="form-control row client" id="MDP"
                        name="MDP" placeholder="New MDP" v-model="this.current_utilisateur.newPassword">
                    <button class="btn btn-outline-secondary colovert" type="button" @click="toggleNewPassword">
                        <i :class="showNewPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    </button>

                </div>
            </div>

        </div>
        <div class="row bottom_button client">

            <button @click="Enregistrer()" type="button" class="btn btn-outline-success"> <img src="/imgs/save.svg"
                    alt="Enregistrer"> Enregistrer </button>
            <RouterLink class="btn  btn-outline-danger" to="/account"> <img src="/imgs/delete.svg" alt="Supprimer"> Annuler
            </RouterLink>
        </div>
    </form>

</template>

<style scoped>

.client {
    margin-right: 0px;
    margin-left: 0px;
}


.colovert {
    border-color: var(--vert-pale);
    background-color: var(--vert-pale);
    color: var(--blanc);
}

span {
    min-width: 5em;
}


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

.input-group{
    align-items: center;
}

.heit{
  height: 100%;
  justify-content: center;
  display: flex;
  flex-wrap: wrap;
  align-content: center;
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

.imputexte{
    max-height: 2em;
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

.groupebutton{
    width: 100%;
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