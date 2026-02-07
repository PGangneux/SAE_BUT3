<script>
import { markRaw } from 'vue';
import Utilisateur from "@model/utilisateur.js";
import edit_success from "./admin/gestion/edit_success.vue"
import edit_error from './admin/gestion/edit_error.vue';

export default {
    name: "page_inscription",
    components: {
        edit_success,
        edit_error
    },
    
    data() {
        return {
            
            current_utilisateur : {type:Utilisateur},
            popupEnregistrer:false,
            popupDelete: false,
            popupSuccess: false,
            popupError: false,
            create:true,

    };
  }, 
  
  
  methods: {
    async validationUSER(){
      let erreur ="";
      if(this.current_utilisateur.pseudo == null || this. current_utilisateur.pseudo ==""){
        erreur += "il manque un pseudo  \n";
      }if(this. current_utilisateur.nom == null || this. current_utilisateur.nom ==""){
        erreur += "il manque une nom  \n";
      }if(this. current_utilisateur.email == null || this. current_utilisateur.email ==""){
        erreur += "il manque une email  \n";
      }if(this. current_utilisateur.password == null || this. current_utilisateur.password ==""){
        erreur += "il manque un mot de passe  \n";
      }
      return erreur;
    },


    



    async Enregistrer(){

        
      try{
        console.log("hello");

        this.message_error = await this.validationUSER();

        if(this.message_error  == ""){
          await this.current_utilisateur.create();
          sessionStorage.setItem('popupSuccess', 'true');
          sessionStorage.setItem('create', this.create ? 'true' : 'false');

          alert("creer");
        }else{
          this.popupError = true;
                setTimeout(()=>{
                    this.popupError = false;
          },5000)
        }


      }catch (error) {
                console.error('Erreur lors de la sauvegarde:', error.toString());
                this.message_error = error.toString();
                this.popupError = true;
                setTimeout(()=>{
                    this.popupError = false;
                },5000)
      }
      
    },



  },

  async mounted() {

        // Popup succès après reload brutal
        if (sessionStorage.getItem('popupSuccess') === 'true') {
            this.popupSuccess = true;

                // Déterminer si c'était en mode création ou modification
            this.createMode = sessionStorage.getItem('create') === 'true';
            console.log("createmode",this.createMode)

            sessionStorage.removeItem('popupSuccess');
            sessionStorage.removeItem('create');

            // ⏱ cacher après 5 secondes
            setTimeout(() => {
                this.popupSuccess = false;
            }, 5000);
        }

        this.current_utilisateur = markRaw( await new Utilisateur({}));


        

    },
};



</script>

<template>
    <h1 class="vert-neon">Inscription</h1>
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

            <div class="row client">
                <div class="input-group mb-3 col">
                    <label class="row client" for="MDP">MDP</label>
                    <input type="password"  class="form-control row client" id="MDP" name="MDP" placeholder="MDP" v-model="this.current_utilisateur.password">
                </div>
            </div>

        </div>
        <div class="row bottom_button client">

          <button @click="Enregistrer()" type="button" class="btn btn-outline-success"> <img src="/imgs/save.svg"
                  alt="Enregistrer"> Enregistrer </button>
          <button @click="this.popupDelete = true" type="button" class="btn  btn-outline-danger"> <img
                  src="/imgs/delete.svg" alt="Supprimer"> Supprimer </button>
        </div>
    </form>
</template>