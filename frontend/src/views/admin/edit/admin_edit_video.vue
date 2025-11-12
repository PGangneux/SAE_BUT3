<script>
import { markRaw } from 'vue';
import comp_baradmin from "../../../components/components_admin/nav_admin.vue";

import comp_popup from "../../../components/components_admin/popup_admin_edit.vue";
import Extrait from "../../../model/extrait";




export default {
  name: "page_admin_detail_video",
  components: {
    comp_baradmin,
    comp_popup,

  },data() {
        return {
            current_extrait : {type:Extrait},
            tags:[],
            thumbnail: '/imgs/width551.png',
            dico_extrait:{},
            taillelist:0,    

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
      console.log(this.popup)
    }


  },


 async mounted() {
    //reccuperation de l'id en parametre
    const ExtraitId = this.$route.params.id;
    //// console.log("ID de l'Extraits' :", ExtraitId);

    //reccuperation de l'Extrait via l'id
    this.current_extrait =  markRaw(await Extrait.detail(ExtraitId));


    console.log(this.current_extrait);

    // console.log("dico complet en cours");
    this.dico_extrait = {
      "artiste":    (markRaw(await this.current_extrait.artiste)).name,
      "question":   (markRaw(await this.current_extrait.titre)).name,
      "interviews": (markRaw(await this.current_extrait.interviews)),
      "tags": (markRaw(await this.current_extrait.tags))
    };


    this.taillelist = this.dico_extrait['tags'].length

   

  //  // console.log(this.dico_extrait['artiste']);
  //  // console.log(this.dico_extrait['question']);
  //  // console.log(this.dico_extrait['interviews']);
  //  // console.log(await this.current_extrait.interviews);



    
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
                <input type="text" id="question" name="question" class="textfield form-control col" placeholder="Question" v-model="this.dico_extrait['question']"  />
            </div>
          </div>

          <div class="input-group mb-3" >
            <span class="input-group-text colovert" >Artiste :</span>
            <input type="text" id="inputartist" name="inputartist" class="textfield form-control" v-model="this.dico_extrait['artiste']" />

            <select id="choix" name="choix" class="form-control colovert" style="border: solid; border-color: var(--vert-midel);" >
              <!-- utiliser js TODO -->
              <option value=""> > </option>
              <option value="option1"> Artiste 1</option> 
              <option value="option2"> Artiste 2</option>
              <option value="option3"> Artiste 3</option>
            </select>

            <div class="form-control colovert">
              <img   class="col" src="/imgs/date.svg" style="padding-right: 10px;" alt="">
              <label class="col whiteelement" style="padding-right: 10px;" for="name4"> Date </label>
              <input class="col" type="date" lang="fr" id="name4" name="name4" :value="this.current_extrait.uploaded_at"/>
              <!-- rendre jolie TODO -->
            </div>
          </div>

          <div class="row"  style="--bs-gutter-x: 0em;">
            <div class="input-group mb-3 ">
              <span class="input-group-text colovert" id="basic-addon1"  >youtube_url :</span>
              <input type="text" class="form-control textfield" placeholder="youtube_url" v-model="youtubeUrl">
            </div>
          </div>
            

          <div class="row"  style="--bs-gutter-x: 0em;">
              <div class="input-group mb-3 ">
                <span class="input-group-text colovert" id="basic-addon2">vimeo_url :</span>
                <input type="text" class="form-control textfield" placeholder="vimeo_url" v-model="vimeoUrl">
              </div>
          </div>
          

            <div class="row"  style="--bs-gutter-x: 0em;">
              <div class="form-group">
                <textarea type="aera" placeholder="Description" style="background-color: var(--gris-ultraclair); border:solid 0.3em;  border-color: var(--vert-pale);" class="form-control" v-model="description"></textarea>
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
        <RouterLink  to="/admin/extrait/creer/" class="btn button-blanc col"> Ajouter un Extrait <img src="/imgs/add_black.svg" alt="add" class="col "> </RouterLink>
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
    
   

    <div v-if="popup === true">  <comp_popup v-on:ecoutepopup="popupchange" /> </div>

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
