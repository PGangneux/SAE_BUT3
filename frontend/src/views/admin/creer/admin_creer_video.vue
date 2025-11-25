<script>
import { markRaw } from 'vue';
import comp_baradmin from "../../../components/components_admin/nav_admin.vue";

import popup_valider from "../../../components/components_admin/popup_validation_creation.vue";

import comp_popup from "../../../components/components_admin/popup_admin_edit.vue";
import Extrait from "../../../model/extrait";




export default {
  name: "page_admin_detail_video",
  components: {
    comp_baradmin,
    popup_valider,
    comp_popup,

  },data() {
        return {
            current_extrait : {type:Extrait},
            tags:[],
            dico_extrait:{},
            taillelist:Array,
            thumbnail: '/imgs/width551.png',

            Element_Creer: {
              type:Object,
            },
            popup: false,
            popup2:true,
        };
    },
    


  methods: {

    async enregistrer(){
      let dicocreation = {
        "titre"         : document.getElementById("question").value, 
        "description"   : document.getElementById("description").value, 
        "youtube_url"   : document.getElementById("youtube").value, 
        "vimeo_url"     : document.getElementById("vimeo").value, 
        "uploaded_at"   : document.getElementById("date").value, 
        "artiste"       : document.getElementById("inputartist").value, 
        "question"      : document.getElementById("question").value,
        
        "interviews"    : document.getElementById("in").value, 
        "tags"          : document.getElementById("in").value,
        "position"      : document.getElementById("in").value,
        "artiste_uuid"  : document.getElementById("in").value,
        "question_uuid" : document.getElementById("in").value,
        "duree"         : document.getElementById("in").value, 
      };


      document.getElementById("in").value;


      this.Element_Creer = await new Extrait().create()
      this.popup2 =true;
    },

    popupchange(){
      this.popup = !this.popup
      console.log(this.popup)
    },

    popupchange2(){
      this.popup2 = !this.popup2
      console.log(this.popup2)
    }


  },


 async mounted() {
  this.taillelist = []
 }

};



</script>

<template>
    <comp_baradmin/>

    <form action="" class="row" style="--bs-gutter-x: 0em;">

      <div class="row"  style="--bs-gutter-x: 0em;">
        <RouterLink class="col-md-4" style="text-decoration: none; color: inherit;" :to="{path: '/lecteur_video/' + current_extrait.uuid }">
          <img :src="thumbnail" class="migniature" alt="migniature">
        </RouterLink>

        <div class="col-md-6">
          <div class="row"  style="--bs-gutter-x: 0em;">
            <div class=" input-group mb-3" >
                <span  class="input-group-text colovert" id="basic-addon3" > Question :</span>

                <select id="question" name="question" class="form-control colovert" style="border: solid; border-color: var(--vert-midel);" >
                  <!-- utiliser js TODO -->
                  <option value=""> > </option>
                  <option value="option1"> Question 1</option> 
                  <option value="option2"> Question 2</option>
                  <option value="option3"> Question 3</option>
                </select>
                <button class="bt" style="background-color: var(--gris-ultraclair);">  <img src="/imgs/add_black.svg" alt="add" class="col "> </button>
            </div>
          </div>

          <div class="row"  style="--bs-gutter-x: 0em;">
              <div class="input-group mb-3" >
                <span class="input-group-text colovert" >Artiste :</span>
                <select id="choix" name="choix" class="form-control colovert" style="border: solid; border-color: var(--vert-midel);" >
                  <!-- utiliser js TODO -->
                  <option value=""> > </option>
                  <option value="option1"> Artiste 1</option> 
                  <option value="option2"> Artiste 2</option>
                  <option value="option3"> Artiste 3</option>
                </select>
                <button class="bt" style="background-color: var(--gris-ultraclair);"> <img src="/imgs/add_black.svg" alt="add" class="col  "> </button>
              </div>
          </div>

          <div class="row"  style="--bs-gutter-x: 0em;">
            <div class="input-group mb-3 ">
              <span class="input-group-text colovert" >  
                <img   class="col" src="/imgs/date.svg" style="padding-right: 10px; width: 1em; height: 1em;" alt="">
                Date : 
              </span>
              <input class="col form-control" type="date" lang="fr" id="date" name="name4" style="background-color: var(--gris-ultraclair);" />
            </div>
          </div>

          <div class="row"  style="--bs-gutter-x: 0em;">
            <div class="input-group mb-3 ">
              <span class="input-group-text colovert" id="basic-addon1"  >youtube_url :</span>
              <input type="text" class="form-control textfield" id="youtube" placeholder="youtube_url">
            </div>
          </div>
            

          <div class="row"  style="--bs-gutter-x: 0em;">
              <div class="input-group mb-3 ">
                <span class="input-group-text colovert" id="basic-addon2">vimeo_url :</span>
                <input type="text" class="form-control textfield" id="vimeo" placeholder="vimeo_url" >
              </div>
          </div>
          

            <div class="row"  style="--bs-gutter-x: 0em;">
              <div class="input-group">
                <textarea type="aera" id="description" placeholder="Description" style="background-color: var(--gris-ultraclair); border:solid 0.3em;  border-color: var(--vert-pale);" class="form-control"></textarea>
              </div>
            </div>

            <div class="row">
              <h1 class="row pcentrer"> Tableau des Playlist
                 <div class="bt btn row"  @click="popup = !popup" style="width: 8%; height: 2.5em; border-radius: 100%; margin-right:0px; margin-left: 0px;"> <img src="/imgs/search.svg" alt="Edit" style="width: 100%;"> </div>
              </h1>
             
              <table class="ultagger table tables table-striped">
                  <thead>
                      <tr>
                          <th class="btgrisv2  col">Nom Playlist</th>
                          <th class="btgrisv2  col">paramètre</th>
                      </tr>
                  </thead>
                  <tbody class="tobodd scroller">
                      <tr class="col" v-for="interview in this.dico_extrait['interviews']">
                          <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> ha </RouterLink> </td>
                          <td> <RouterLink class="container container_extrait col "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> <button class="bt col"> modifier </button></RouterLink>  <RouterLink class="container container_extrait col "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> <button class="bt col"> supprimer </button> </RouterLink> </td>
                      </tr>
                  </tbody>
              </table>
             
              <RouterLink  to="/admin/interview/creer/" type="button" class="btn button-blanc col"> Ajouter un Playlist <img src="/imgs/add_black.svg" alt="add" class="col "> </RouterLink>

            </div>
        </div>
      </div>


      <div class="row pad"  style="--bs-gutter-x: 0em;">
        <button  type="button" @click="enregistrer"  class="bt btn col" > <img src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>
        <button  type="reset"  class="bt btn col" > <img src="/imgs/cancel.svg" alt="Annuler"> Annuler </button>
      </div>

    </form>
    
    <div class="row grisee "  style="--bs-gutter-x: 0em;">
      <h1 class="row pcentrer"  style="--bs-gutter-x: 0em;"> Meta Donnée </h1>
      <button> <img src="/imgs/add_black.svg" alt="add" class="col "> </button>
       <div class="recherche">
            <div class="search-bar">
                <div class="input-group">
                    <input type="text" class="form-control" v-model="searchValue" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                    <RouterLink to="/" class="btn btn-outline-secondary buttonsearch" type="button" id="search-addon">
                            <img src="/imgs/search.svg" alt="button search">
                        </RouterLink>
                </div>
            </div>
      </div>



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
    
   

    <div v-if="popup === true">  <comp_popup v-on:ecoutepopup="popupchange" /> </div>
    
    <div v-if="popup2 === true">  <popup_valider  v-on:ecoutepopup2="popupchange2" /> </div>


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
