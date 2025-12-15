<script>
import { markRaw } from 'vue';
import comp_baradmin from "../../../components/components_admin/nav_admin.vue";

import popup_interview from "../../../components/components_admin/popup_admin_edit.vue";
import Extrait from "../../../model/extrait";
import Interview from '../../../model/interview.js';
import Question from "../../../model/question";
import Artiste from "../../../model/artiste";



export default {
  name: "page_admin_detail_video",



  components: {
    comp_baradmin,
    popup_interview,

  },data() {
        return {
            current_extrait : {type:Extrait},
            tags:[],
            thumbnail: '/imgs/width551.png',
            dico_extrait:{},
            taillelist:0,

            //a modifer
            dico_elementmodif:{  
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

            popup: false
        };
    }
    
    ,computed: {
      youtubeUrl: {
        get() {
          if(this.current_extrait?.youtube_url != null){
            return 'https://www.youtube.com/watch?v=' + this.current_extrait.youtube_url;
          }else if (this.current_extrait?.youtube_url == null){
            return '';
          }else{
            return 'erreur...';
          }
         
        },
        set(value) {
          const id = value.split('v=')[1];
          if (id) this.current_extrait.youtube_url = id;
        }
      },

      vimeoUrl: {
        get() {

          if(this.current_extrait?.vimeo_url != null){
            return 'https://vimeo.com/' + this.current_extrait.vimeo_url;
          }else if (this.current_extrait?.vimeo_url == null){
            return '';
          }else{
            return 'erreur...';
          }

          
        },
        set(value) {
          const id = value.split('/').pop();
          if (id) this.current_extrait.vimeo_url = id;
        }
      },
      description : {
         get() {
          return this.current_extrait?.description ? this.current_extrait.description : 'Chargement...';
        },
      },

      question : {
         get() {
          return this.current_extrait?.question ? this.current_extrait.question : 'Chargement...';
        },
      }
  },


  methods: {


    popupchange(){
      this.popup = !this.popup
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
    //reccuperation de l'id en parametre
    const ExtraitId = this.$route.params.id;

    //reccuperation de l'Extrait via l'id
    this.current_extrait =  markRaw(await Extrait.detail(ExtraitId));
    await this.recupeArtiste();
    await this.recupeQuestion();


    this.dico_extrait = {
      "artiste":    (markRaw(await this.current_extrait.artiste)),
      "uploaded_at": (markRaw(await this.current_extrait.uploaded_at)),
      "question":   (markRaw(await this.current_extrait.titre)),
      "interviews": (markRaw(await this.current_extrait.interviews)),
      "tags": (markRaw(await this.current_extrait.tags))
    };


    this.taillelist = this.dico_extrait['tags'].length







    
    if (this.current_extrait.url_miniature_yt != null && this.current_extrait.url_miniature_yt.includes(this.current_extrait.youtube_url) ) {
        
      this.thumbnail = await this.current_extrait.url_miniature_yt
        
    }else{
        this.thumbnail = await this.current_extrait.url_miniature_vi()
        
    }


  },


};



</script>

<template>
    <comp_baradmin/>

    <form action="" class="row" style="--bs-gutter-x: 0em;">

      <div class="row"  style="--bs-gutter-x: 0em;">
        <RouterLink class="col-md-4" style="text-decoration: none; color: inherit; padding: 1em;" :to="{path: '/lecteur_video/' + current_extrait.uuid }">
          <img :src="thumbnail" class="migniature" alt="migniature">
        </RouterLink>

        <div class="col-md-6 scroller" style="width: 65%; height: 33vh;">
          
          

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
              <input class="col form-control" type="date" lang="fr" id="date" name="name4" style="background-color: var(--gris-ultraclair);" v-model="this.current_extrait.uploaded_at" />
            </div>
          </div>

          <div class="row"  style="--bs-gutter-x: 0em;">
            <div class="input-group mb-3 ">
              <span class="input-group-text colovert" id="basic-addon1"  >youtube_url :</span>
              <input type="text" class="form-control textfield" id="youtube" placeholder="youtube_url" v-model="this.current_extrait.youtube_url" >
            </div>
          </div>
            

          <div class="row"  style="--bs-gutter-x: 0em;">
              <div class="input-group mb-3 ">
                <span class="input-group-text colovert" id="basic-addon2">vimeo_url :</span>
                <input type="text" class="form-control textfield" id="vimeo" placeholder="vimeo_url" v-model="this.current_extrait.vimeo_url">
              </div>
          </div>
          

          <div class="row"  style="--bs-gutter-x: 0em;">
            <div class="input-group">
              <textarea type="aera" id="description" placeholder="Description" style="background-color: var(--gris-ultraclair); border:solid 0.3em;  border-color: var(--vert-pale);" class="form-control" v-model="this.current_extrait.description"></textarea>
            </div>
          </div>

            <div class="row" style="margin-right: 0em; margin-left: 0em;">
              <h1 class="row pcentrer"> Tableau des Playlist
                 <div class="bt btn row"  @click="popup = !popup" style="width: 8%; border-radius: 100%; margin-right:0px; margin-left: 0px;"> <img src="/imgs/search.svg" alt="Edit" style="width: 100%;"> </div>
              </h1>
             
              <table class="ultagger table tables table-striped">
                  <thead>
                      <tr>
                          <th class="btgrisv2  col">Nom Playlist</th>
                          <th class="btgrisv2  col">paramètre</th>
                      </tr>
                  </thead>
                  <tbody class="tobodd">
                      <tr class="col" v-for="interview in this.dico_extrait['interviews']">
                          <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/' + interview.uuid"> {{ interview.titre }} </RouterLink> </td>
                          <td> <RouterLink class="container container_extrait col "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/' + interview.uuid"> <button class="bt col"> modifier </button></RouterLink>  <RouterLink class="container container_extrait col "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/' + interview.uuid"> <button class="bt col"> supprimer </button> </RouterLink> </td>
                      </tr>
                  </tbody>
              </table>

              <RouterLink  to="/admin/interview/creer/" type="button" class="btn button-blanc col"> Ajouter un Playlist <img src="/imgs/add_black.svg" alt="add" class="col "> </RouterLink>
             
            </div>
        </div>
      </div>


      <div class="row pad"  style="--bs-gutter-x: 0em;">
        <RouterLink  to="/admin/extrait/" class="btn button-blanc col"> Ajouter un Extrait <img src="/imgs/add_black.svg" alt="add" class="col "> </RouterLink>
        <button  type="submit"   class="bt btn col" > <img src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>
        <button  type="reset"  class="bt btn col" > <img src="/imgs/cancel.svg" alt="Annuler"> Annuler </button>

      </div>

    </form>
    
    <div class="row grisee "  style="--bs-gutter-x: 0em;">
      <h1 class="row pcentrer"  style="--bs-gutter-x: 0em;"> Meta Donnée </h1>
      <div class="row">

        <ul v-if="this.taillelist != 0" class="scroller2  row" style="--bs-gutter-x: 0em; height: 17vh;" >
            <li v-for="tag in dico_extrait.tags " class="col">
                <div class="row" style="--bs-gutter-x: 0rem;">
                  <img src="/imgs/labeltags.svg" class="col" alt="labelle tags" height="50" width="50" style="max-width: 5em;">
                  <p class="col" style="text-align: center; max-width:max-content; align-content: center; ">{{ tag.name }}</p>
                </div>
            </li>
        </ul>

        <ul v-else-if="this.taillelist == 0 " class="col">
            <li class="row"> 
                <p  class="col">vide</p>
            </li>
        </ul>

        <ul v-else class="col">
            <li> 
                <p  class="col">erreur de Chargement</p>
            </li>
        </ul>        




      </div>
    </div>
    
   

    <div v-if="popup === true">  <popup_interview v-on:ecoutepopup="popupchange" /> </div>

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

  height: 100%;
  width: 100%;
}

option{
  display : "none"
}

label{
  color: var(--vert-neon);
}


li>.card {
  padding: 20px 50px 150px;
  margin: 10px 10px 10px 10px;  
}

span{
      min-width: 8em;
}
ul {
  display: flex;
  list-style-type: none;
  justify-content: space-between;
}


.scroller {
    width: 100%;
    height: 100vh;
    overflow-y: scroll;
    scrollbar-color: var(---blanc) #A6A6A6;
    scrollbar-width: thin;
}





.scroller2 {
  height: 100vh;
  overflow-y: scroll;
  scrollbar-color: var(---blanc) #A6A6A6;
  scrollbar-width: thin;
}




.button-blanc{
    background-color: var(--blanc);
}







</style>
