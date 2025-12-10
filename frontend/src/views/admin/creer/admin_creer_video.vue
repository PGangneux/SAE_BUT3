<script>
import { markRaw } from 'vue';
import comp_baradmin from "../../../components/components_admin/nav_admin.vue";

import popup_valider from "../../../components/components_admin/popup_validation_creation.vue";

import popup_interview from "../../../components/components_admin/popup_admin_edit.vue";
import Extrait from "../../../model/extrait";

import Interview from '../../../model/interview.js';
import Question from "../../../model/question";
import Artiste from "../../../model/artiste";



export default {
  name: "page_admin_detail_video",
  components: {
    comp_baradmin,
    popup_valider,
    popup_interview,

    //dataliste
  },data() {
        return {
            tags:[],
            dico_extrait:{},
            taillelist:Array,
            thumbnail: '/imgs/width551.png',
            searchValue: "",
            new_extrait:new Extrait("","","","","","","","","","","","",),
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
            selectedArtiste: "",
            selectedQuestion: "",
            selectedId: null,

            Element_Creer: {
              type:Object,
            },
            listeArtiste:[],
            listeQuestion:[],
            popup: false,
            popup2:false,
        };
    },
    


  methods: {

    async enregistrer(){

      
      console.log(this.dico_elementcreer);

      console.log(this.new_extrait)

      this.new_extrait.titre = this.dico_elementcreer.titre;
      this.new_extrait.description = this.dico_elementcreer.description;
      this.new_extrait.youtube_url = this.dico_elementcreer.youtube_url;
      this.new_extrait.vimeo_url = this.dico_elementcreer.vimeo_url;
      
      this.new_extrait.uploaded_at = this.dico_elementcreer.uploaded_at
      this.new_extrait.tags = this.dico_elementcreer.tags

      console.log(this.new_extrait)

      //https://www.youtube.com/watch?v=xvFZjo5PgG0
  

      console.log("creer");
      this.popup2 = true;
    },

    possiblecreation(){

    },

    ajoutertag(){

    },

    removetag(idtags){
      if(this.dico_elementcreer.tags == []){
        console.log("pas d'element a retiré")
      }else if (this.dico_elementcreer.tags.includes(idtags)) {
        this.dico_elementcreer.tags.remove(idtags);
        console.log("tags retiré")
      }
    },


    

    popupchange(){
      this.popup = !this.popup
      console.log(this.popup)
    },

    popupchange2(){
      this.popup2 = !this.popup2
      console.log(this.popup2)
    },



    updateSelectedArtisteId() {
     
     //console.log(this.selectedArtiste);
      const artiste = this.listeArtiste.find(a => a.name === this.selectedArtiste);

      if (artiste) {
          this.dico_elementcreer.artiste = artiste;
          this.dico_elementcreer.artiste_uuid = artiste.uuid;
          this.new_extrait.artiste =artiste.uuid;
        } else {
          this.dico_elementcreer.artiste = null;
          this.dico_elementcreer.artiste_uuid = null;
      }

      console.log( this.dico_elementcreer.artiste, this.dico_elementcreer.artiste_uuid);

    },

    updateSelectedQuestion() {
     
      //console.log(this.listeQuestion);
      const question = this.listeQuestion.find(a => a.texte === this.selectedQuestion);

      //console.log(question);

      if (question) {
          this.dico_elementcreer.question = question;
          this.dico_elementcreer.question_uuid = question.uuid;
          this.dico_elementcreer.titre = question.texte;
          this.new_extrait.question = question.uuid;
        } else {
          this.dico_elementcreer.question = null;
          this.dico_elementcreer.question_uuid = null;
      }


      console.log( this.dico_elementcreer.question);

    },










    async recupeArtiste(){
      this.listeArtiste =  markRaw(await Artiste.list());
      //console.log("artiste", this.listeArtiste)
      //console.log("artiste", this.listeArtiste[0].name)
    },




    async recupeQuestion(){
      this.listeQuestion =  markRaw(await Question.list());
      //console.log(this.listeQuestion)
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
        <RouterLink class="col-md-4" style="text-decoration: none; color: inherit;" :to="{path: '/admin/extrait/creer/' }">
          <img :src="thumbnail" class="migniature" alt="migniature">
        </RouterLink>

        <div class="col-md-6">
          <div class="row"  style="--bs-gutter-x: 0em;">
            <div class=" input-group mb-3" >
                <span  class="input-group-text colovert" id="basic-addon3" > Question :</span>

                <input list="Questiondata" id="question" name="question" class="form-control colovert" style="border: solid; border-color: var(--vert-midel);"  v-model="selectedQuestion" @input="updateSelectedQuestion"/>
                
                <datalist id="Questiondata">
                <option v-for="question in listeQuestion" :key="question.id" :value="question.texte" :label="question.texte" > </option> 
                </datalist>


                <button class="bt" style="background-color: var(--gris-ultraclair);">  <img src="/imgs/add_black.svg" alt="add" class="col "> </button>
            </div>
          </div>

          <div class="row"  style="--bs-gutter-x: 0em;">
              <div class="input-group mb-3" >
                <span class="input-group-text colovert" >Artiste :</span>
                <input list="Artistedata" id="choix" name="choix" class="form-control colovert" style="border: solid; border-color: var(--vert-midel);"   v-model="selectedArtiste" @input="updateSelectedArtisteId">
                
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
                        <input type="text" class="form-control" v-model="searchValue" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
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
    
   

    <div v-if="popup === true">  <popup_interview v-on:ecoutepopup="popupchange" v-on:Interview_ajouter="interview_ajouter" v-on:Interview_retirer="interview_retirer" /> </div>
    
    <div v-if="popup2 === true">  <popup_valider  v-on:popupenregistrer="popupchange2"/> </div>


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
