<script>
import { markRaw } from 'vue';
import comp_baradmin from "../../../components/components_admin/nav_admin.vue";

import popup_valider from "../../../components/components_admin/popup_validation_creation.vue";

import popup_interview from "../../../components/components_admin/popup_admin_edit.vue";


import Question from "../../../model/question";
import Artiste from "../../../model/artiste";
import Extrait from "../../../model/extrait";



export default {
  name: "page_admin_detail_video",
  components: {
    comp_baradmin,
    popup_valider,
    popup_interview,

  },data() {
        return {
            taillelist:Array,
            thumbnail: '/imgs/width551.png', //image defaults
            searchValueTag: "",
            
            //regroupement des valeurs des imputs
            dico_elementcreer:{  
                  titre: null,
                  description:  null,
                  youtube_url:  null,
                  vimeo_url:    null,
                  uploaded_at:  null,
                  artiste:      null,
                  question:     null,
                  tags:         null,
                  position:     null,
                  artiste_uuid: null,
                  question_uuid:null,
                  duree:        null,
            },
            
            selectedArtiste: "", //Artiste selectionner retourn null si rien
            selectedQuestion: "",//Questio selectionner retourn null si rien

            listeArtiste:[],    //liste des Artistes totals
            listeQuestion:[],   //liste des Questions totals
            tags:[],            //liste des tags totals


            popupSelectInterview: false, //Props pour popupSelectInterview
            popupEnregistrer:false,
        };
    },
    


  methods: {

    async enregistrer(){
      //fonction pour enregistrer un extraits dans L'api


      //Extrait vide
      const new_extrait = new Extrait("","","","","","","","","","","","",); 
      
      console.log(this.dico_elementcreer);

      new_extrait.titre = this.dico_elementcreer.titre;
      new_extrait.description = this.dico_elementcreer.description;
      new_extrait.youtube_url = this.dico_elementcreer.youtube_url;
      new_extrait.vimeo_url = this.dico_elementcreer.vimeo_url;
      new_extrait.uploaded_at = this.dico_elementcreer.uploaded_at
      new_extrait.tags = this.dico_elementcreer.tags
      new_extrait.artiste =this.dico_elementcreer.artiste_uuid;
      new_extrait.question = this.dico_elementcreer.question_uuid;
      
      console.log(new_extrait)

      const test = await new_extrait.create();
      
  
      console.log("creer");
      this.popupEnregistrer = false;
      //new_extrait.create
    },

    possiblecreation(){
    //fonction pour verifier si les elements peuve etre enregistrer

    },

    ajoutertag(){
      //permet d'ajouter un tag a l'extrait
    },

    removetag(idtags){
      //permet de retirer un tag a l'extrait

      if(this.dico_elementcreer.tags == []){
        //console.log("pas d'element a retiré")
      }else if (this.dico_elementcreer.tags.includes(idtags)) {
        this.dico_elementcreer.tags.remove(idtags);
        //console.log("tags retiré")
      }
    },

    popupchangeInterview(){
      //permet de changer l'etat de la popup Interview
      this.popupSelectInterview = !this.popupSelectInterview
      
    },

    popupchangeEnregistrer(){
      //permet de changer l'etat de la popup Enregistrer
      this.popupEnregistrer = !this.popupEnregistrer
      
    },



    SelectedArtisteId() {
      //reccupere l'artiste de la liste en reccuperant le nom de l'artiste selectionner
      //reccupere l'artiste de la liste
      const artiste = this.listeArtiste.find(a => a.name === this.selectedArtiste);

      

      //verifie si artiste existe et n'es pas null
      if (artiste) {
          this.dico_elementcreer.artiste = artiste;
          this.dico_elementcreer.artiste_uuid = artiste.uuid;
        } else {
          this.dico_elementcreer.artiste = null;
          this.dico_elementcreer.artiste_uuid = null;
      }

    },

    SelectedQuestion() {
      //reccupere la Question de la liste en reccuperant le text de la Question selectionner

      //reccupere l'artiste de la liste
      const question = this.listeQuestion.find(a => a.texte === this.selectedQuestion);

      //verifie si question existe et n'es pas null
      if (question) {
          this.dico_elementcreer.question = question;
          this.dico_elementcreer.question_uuid = question.uuid;
          this.dico_elementcreer.titre = question.texte;
        } else {
          this.dico_elementcreer.question = null;
          this.dico_elementcreer.question_uuid = null;
      }

    },

    async recupeArtiste(){
      //reccupere la liste des Artistes
      this.listeArtiste =  markRaw(await Artiste.list());
    },

    async recupeQuestion(){
      //reccupere la liste des Questions
      this.listeQuestion =  markRaw(await Question.list());
    }


  },



 async mounted() {
  this.taillelist = []

  await this.recupeArtiste();
  await this.recupeQuestion();

 }

};



</script>

<template>
    <comp_baradmin/>

    <form action="" class="row" style="--bs-gutter-x: 0em;">

      <div class="row"  style="--bs-gutter-x: 0em;">
        <RouterLink class="col-md-4" style="text-decoration: none; color: inherit;" :to="{path: '/admin/extrait/' }">
          <img :src="thumbnail" class="migniature" alt="migniature">
        </RouterLink>

        <div class="col-md-6">
          <div class="row"  style="--bs-gutter-x: 0em;">
            <div class=" input-group mb-3" >
                <span  class="input-group-text colovert" id="basic-addon3" > Question :</span>

                <input list="Questiondata" id="question" name="question" class="form-control colovert" style="border: solid; border-color: var(--vert-midel);"  v-model="selectedQuestion" @input="SelectedQuestion"/>
                
                <datalist id="Questiondata">
                <option v-for="question in listeQuestion" :key="question.id" :value="question.texte" :label="question.texte" > </option> 
                </datalist>


                <button class="bt" style="background-color: var(--gris-ultraclair);">  <img src="/imgs/add_black.svg" alt="add" class="col "> </button>
            </div>
          </div>

          <div class="row"  style="--bs-gutter-x: 0em;">
              <div class="input-group mb-3" >
                <span class="input-group-text colovert" >Artiste :</span>
                <input list="Artistedata" id="choix" name="choix" class="form-control colovert" style="border: solid; border-color: var(--vert-midel);"   v-model="selectedArtiste" @input="SelectedArtisteId">
                
                <datalist id="Artistedata">
                <option v-for="artiste in listeArtiste" :key="artiste.id" :value="artiste.name" :label="artiste.name" > </option> 
                </datalist>

                <button class="bt" style="background-color: var(--gris-ultraclair);"> <img src="/imgs/add_black.svg" alt="add" class="col  "> </button>
              </div>
          </div>

          <div class="row"  style="--bs-gutter-x: 0em;">
            <div class="input-group mb-3 ">
              <span class="input-group-text colovert" >  
                <img   class="col" src="/imgs/date.svg" style="padding-right: 10px; width: 1em; height: 1em;" alt="">
                Date : 
              </span>
              <input class="col form-control" type="date" lang="fr" id="date" name="name4" style="background-color: var(--gris-ultraclair);" v-model="dico_elementcreer.uploaded_at" />
            </div>
          </div>

          <div class="row"  style="--bs-gutter-x: 0em;">
            <div class="input-group mb-3 ">
              <span class="input-group-text colovert" id="basic-addon1"  >youtube_url :</span>
              <input type="text" class="form-control textfield" id="youtube" placeholder="youtube_url" v-model="dico_elementcreer.youtube_url" >
            </div>
          </div>
            

          <div class="row"  style="--bs-gutter-x: 0em;">
              <div class="input-group mb-3 ">
                <span class="input-group-text colovert" id="basic-addon2">vimeo_url :</span>
                <input type="text" class="form-control textfield" id="vimeo" placeholder="vimeo_url" v-model="dico_elementcreer.vimeo_url">
              </div>
          </div>
          

            <div class="row"  style="--bs-gutter-x: 0em;">
              <div class="input-group">
                <textarea type="aera" id="description" placeholder="Description" style="background-color: var(--gris-ultraclair); border:solid 0.3em;  border-color: var(--vert-pale);" class="form-control" v-model="dico_elementcreer.description"></textarea>
              </div>
            </div>

           
        </div>
      </div>


      <div class="row pad"  style="--bs-gutter-x: 0em;">
        <button  type="button" @click="enregistrer"  class="bt btn col" > <img src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>
        <button  type="reset"  class="bt btn col" > <img src="/imgs/cancel.svg" alt="Annuler"> Annuler </button>
      </div>

    </form>
    
    <div class="row grisee "  style="--bs-gutter-x: 0em;">
      <section class="row secondpart">
          <h1 class="pcentrer col"  style="--bs-gutter-x: 0em;"> Meta Donnée </h1>
          <button class="bt col"> <img src="/imgs/add_black.svg" alt="add" class="col "> </button>
          <div class="recherche col">
                <div class="search-bar">
                    <div class="input-group">
                        <input type="text" class="form-control" v-model="searchValueTag" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                        <RouterLink to="/" class="btn btn-outline-secondary buttonsearch" type="button" id="search-addon">
                                <img src="/imgs/search.svg" alt="button search">
                            </RouterLink>
                    </div>
                </div>
            </div>
      </section>



      <div class="row">

        <ul v-if="this.taillelist.length != 0" class="scroller2  row" style="--bs-gutter-x: 0em;" >
            <li v-for="tag in this.taillelist " class="col">
                <div class="row">
                  <img src="/imgs/labeltags.svg" class="col" alt="labelle tags" height="50" width="50">
                  <p class="col">ssssssssss</p>
                  <button> - </button>
                </div>
            </li>
        </ul>

        <ul v-else-if="this.taillelist == 0 " class="col">
            <li class="row"> 
              <img src="/imgs/labeltags.svg" class="col" alt="labelle tags" height="50" width="50">
              <p  class="col">vide</p>
              <button class="col bt" ><img src="/imgs/remove.svg" class="col" alt="labelle tags" height="20" width="20"> </button>
            </li>
        </ul>

        <ul v-else class="col">
            <li> 
                <p  class="col">erreur de Chargement</p>
            </li>
        </ul>        




      </div>
    </div>
    
   

    <!-- <div v-if="popupSelectInterview === true">  <popup_interview v-on:ecoutepopup="popupchangeInterview" v-on:Interview_ajouter="interview_ajouter" v-on:Interview_retirer="interview_retirer" /> </div> -->
    
    <div v-if="popupEnregistrer === true">  <popup_valider  v-on:popupenregistrer="popupchangeEnregistrer"/> </div>


    </template>

<style scoped>
.migniature{
  height: 90%;
  width: 90%;
}

.card {
  background-color: var(--gris-moyen);
  filter: drop-shadow(20px 13px 4px var(--noir));

  height:  553px;
  width: 470px;
}
li>.card {
  padding: 20px 50px 150px;
  margin: 10px 10px 10px 10px;  
}

span{
      min-width: 8em;
}

.scroller2 {
  height: 100vh;
  overflow-y: scroll;
  scrollbar-color: var(---blanc) #A6A6A6;
  scrollbar-width: thin;
}

.pad{
  padding-top: 1em;
  padding-bottom: 1em;
}

.pcentrer{
margin-top: 1em;
margin-bottom: 1em;
justify-content: center
}


.centrer{
justify-content: center
}

.tobodd{
    padding-top: 1em;
}

.tables{
  height: 1em;
  width: 100%;
}

.ultagger {
    list-style-type: none;

}

.scroller {
    width: 300px;
    height: 100vh;
    overflow-y: scroll;
    scrollbar-color: var(---blanc) #A6A6A6;
    scrollbar-width: thin;
}

ul {
  display: flex;
  list-style-type: none;
  justify-content: space-between;
}

.grisetround{
  border-radius:2em;
  
  background-color: var(--gris-moyen);
}

.grisee{
  background-color: var(--gris-moyen);
}


.textfield{
  background-color: var(--gris-ultraclair);
}

.bt{
    color: var(--blanc);
    background-color:var(--vert-pale);
    border-radius: 2em;
    
}

.colovert{
  border-color: var(--vert-pale);
  background-color:var(--vert-pale);
  color: var(--blanc);
}

.whiteelement{
 color: var(--blanc);
}

.migniature{
  border: solid 3px;
  border-color: var(--vert-neon);
  border-radius: 2em;
}

.secondpart{
  display: flex;
  justify-content: center;
  align-content: center;
  align-items: center;
  margin: 1em;
}

option{
  display : "none"
}

label{
  color: var(--vert-neon);
}


.button-blanc{
    background-color: var(--blanc);
}

</style>
