<script>
import { markRaw } from 'vue';
import comp_baradmin from "../../../components/components_admin/nav_admin.vue";

import popup_interview from "../../../components/components_admin/popup_admin_edit.vue";
import Extrait from "../../../model/extrait";
import Interview from '../../../model/interview.js';
import Question from "../../../model/question";
import Artiste from "../../../model/artiste";
import supprimer from "../supprimer.vue";
import tags from "../tags.vue"
import Tag from "../../../model/tag.js";

import { handleTagsConnected, handleTagsDisconnected, handleTagsCreated } from '../fn_save_tags.js';

export default {
  name: "page_admin_detail_video",



  components: {
    comp_baradmin,
    popup_interview,
    supprimer,
    tags,

  },data() {
        return {
            current_extrait : null,
            thumbnail: '/imgs/width551.png',          
            laselectedArtiste: "", //Artiste selectionner retourn null si rien
            laselectedQuestion: "",//Questio selectionner retourn null si rien 

            interviews:[],
            listeArtiste:[],    //liste des Artistes totals
            listeQuestion:[],   //liste des Questions totals
            popupDelete: false,
            searchValueTag:"",
            create:false,
            popup: false,
            popupSelectInterview: false, //Props pour popupSelectInterview
            popupEnregistrer:false,
            
            urlVimeoReconstruit:"",
            urlyoutubeReconstruit:"",

            tagsConnected: [],
            tagsToDisconnect: [],
            tagsToCreate: [],  
        };
    },
    
    


  methods: {

    handleTagsCreated(tags) {
      console.log("htct1");
        handleTagsCreated(this, tags)
        console.log("htct2", this.tagsToCreate);
    },

    handleTagsDisconnected(tags) {
      console.log("htd1");
        handleTagsDisconnected(this, tags)
        console.log("htd2",this.tagsToDisconnect);
    },

    handleTagsConnected(tag) {

      
            
           
      console.log("htc1");
        handleTagsConnected(this, tag)
        console.log("htc2",this.tagsConnected);
    },

    async save_tags() {
        console.log("save tags",this.current_extrait);
        try {
            // Connecter les tags existants
            for (const tag of this.tagsConnected) {
                console.log(tag)
                await this.current_extrait.connect_tag(tag);
            }
            
            // Créer et connecter les nouveaux tags
            for (const tagData of this.tagsToCreate) {
                const newTag = await new Tag({ name: tagData.name }).create();
                await this.current_extrait.connect_tag(newTag);
            }
            
            // Déconnecter les tags
            for (const tag of this.tagsToDisconnect) {
                await this.current_extrait.disconnect_tag(tag);
            }
            
            // Réinitialiser les listes après sauvegarde
            this.tagsConnected = [];
            this.tagsToCreate = [];
            this.tagsToDisconnect = [];
        } catch (error) {
            console.error('Erreur lors de la sauvegarde des tags:', error);
            throw error;
        }
    },

    creerNouveauArtiste(){
      const newArtiste = new Artiste({});

      if (!this.listeArtiste.find(a => a.name === this.laselectedArtiste)){
        newArtiste.name = this.laselectedArtiste;
        newArtiste.create()
        this.listeArtiste.add(newArtiste);

      }else{
        console.log('artiste existe deja');
      }
      
    },

    creerNouvelleQuestion(){
      const newQuestion = new Question({});

      if (!this.listeQuestion.find(a => a.name === this.laselectedQuestion)){
        newQuestion.name = this.laselectedQuestion;
        newQuestion.create()
        this.listeQuestion.add(newQuestion);

      }else{
        console.log('question existe deja');
      }
      
    },


    async enregistrer(){
      //fonction pour enregistrer un extraits dans L'api

      console.log(this.current_extrait);
      this.current_extrait.duree = 0;

      this.popupEnregistrer = true;
      console.log('deb')
      await this.current_extrait.create();
      console.log('ga')
      
      //this.new_extrait = new markRaw(new Extrait({}));

      await this.save_tags();
      console.log('fa')
  
      console.log("creer");
      
      //new_extrait.create
    },

    popupchange(){
      this.popup = !this.popup
    },

   async modificationDonnees(){
      if (this.create) {
          await this.enregistrer();
      } else {
        await this.Update();
      }
    },


    async Update(){
      console.log(this.current_extrait);
      this.current_extrait.update();
      await this.save_tags();
    },



    SelectedArtisteId() {
      //reccupere l'artiste de la liste en reccuperant le nom de l'artiste selectionner
      //reccupere l'artiste de la liste
      const artiste = this.listeArtiste.find(a => a.name === this.laselectedArtiste);

      

      //verifie si artiste existe et n'es pas null
      if (artiste) {
          this.current_extrait.artiste = artiste.uuid;
          this.current_extrait.artiste_uuid = artiste.uuid;
        } else {
          this.current_extrait.artiste = null;
          this.current_extrait.artiste_uuid = null;
      }

    },

    FoncSelectedQuestion() {
      //reccupere la Question de la liste en reccuperant le text de la Question selectionner

      //reccupere l'artiste de la liste
      const question = this.listeQuestion.find(a => a.texte === this.laselectedQuestion);

      //verifie si question existe et n'es pas null
      if (question) {
          this.current_extrait.question = question.uuid;
          this.current_extrait.question_uuid = question.uuid;
        } else {
          this.current_extrait.question = null;
          this.current_extrait.question_uuid = null;
      }

    },

    async recupeArtiste(){
      //reccupere la liste des Artistes
      this.listeArtiste =  markRaw(await Artiste.list());
    },

    async recupeQuestion(){
      //reccupere la liste des Questions
      this.listeQuestion =  markRaw(await Question.list());
    },


    popupchangeEnregistrer(){
      //permet de changer l'etat de la popup Enregistrer
      this.popupEnregistrer = !this.popupEnregistrer
      
    },

    popupchangeInterview(){
      //permet de changer l'etat de la popup Interview
      this.popupSelectInterview = !this.popupSelectInterview
      
    },

    async validateYouTubeVideo(url) {
      // Extraire l'ID YouTube
      if ((this.get_YT_videoId(url)==null || this.get_YT_videoId(url)=="") || !this.get_YT_videoId(url) ) {
        console.log("URL YouTube invalide");
        return '/imgs/width551.png';
      }
      const videoId = this.get_YT_videoId(url);
      if (!videoId) {
        console.log("URL YouTube invalide");
        return '/imgs/width551.png';
      }
      try {
        const response = await fetch(
          `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`
        );

        if (!response.ok) {
          if (response.status === 404) {
            console.log("Vidéo introuvable");
          } else {
            console.log("Vidéo inaccessible");
          }
          return '/imgs/width551.png';
        }
        const data = await response.json();
        return data.thumbnail_url;

      } catch (error) {
        return '/imgs/width551.png';
      }
    },


    async validateVimeoVideo(url) {
      // Extraire l'ID Vimeo
      if (this.get_Vimeo_videoId(url)==null || this.get_Vimeo_videoId(url)=="" ||!this.get_Vimeo_videoId(url)) {
        return '/imgs/width551.png';
      }
      const videoId = this.get_Vimeo_videoId(url);
      if (!videoId) {
        console.log("URL Vimeo invalide");
        return '/imgs/width551.png';
      }
      
      try {
        const response = await fetch(
          `https://vimeo.com/api/oembed.json?url=https://vimeo.com/${videoId}`
        );
        
        if (!response.ok) {
          if(response.status === 404 ){
            console.log("Vidéo introuvable")
          }else{
          console.log("Vidéo inaccessible")
        }
        return '/imgs/width551.png'
        }
        
        const data = await response.json();
        return data.thumbnail_url;
      }
        catch (error) {
        return '/imgs/width551.png';
      }
    },

  async migniature_video(){

        if (this.urlVimeoReconstruit !=null && !this.urlVimeoReconstruit.includes('https') && this.urlVimeoReconstruit!='' ) {
          this.urlVimeoReconstruit = 'https://vimeo.com/' +this.urlVimeoReconstruit ;
        }

        if (this.urlyoutubeReconstruit !=null && !this.urlyoutubeReconstruit.includes('https') && this.urlyoutubeReconstruit!='') {
          this.urlyoutubeReconstruit = 'https://www.youtube.com/watch?v='  + this.urlyoutubeReconstruit;
        }

        try{
          this.current_extrait.youtube_url = this.get_YT_videoId(this.urlyoutubeReconstruit);
        }catch{
          this.current_extrait.youtube_url="";
          console.log('erreur');
        }

        try{
          this.current_extrait.vimeo_url = await this.get_Vimeo_videoId(this.urlVimeoReconstruit);
          console.log(this.current_extrait.vimeo_url);
        }catch{
          this.current_extrait.vimeo_url="";
          console.log('erreur');
        }

    
        if ( this.current_extrait.url_miniature_yt != null && this.current_extrait.url_miniature_yt.includes(this.current_extrait.youtube_url) && !this.current_extrait.youtube_url=="" ) {
          
          console.log(this.validateYouTubeVideo(this.urlyoutubeReconstruit));
          this.thumbnail = await this.validateYouTubeVideo(this.urlyoutubeReconstruit);
            
        }else{
          console.log(this.validateVimeoVideo(this.urlVimeoReconstruit));
          this.thumbnail = await this.validateVimeoVideo(this.urlVimeoReconstruit);
        }
  },

    get_YT_videoId(url) {
      try {
        const u = new URL(url);
        if (u.hostname === "youtu.be") return u.pathname.slice(1);
        if (u.hostname.includes("youtube.com")) {
          if (u.pathname.startsWith("/embed/")) return u.pathname.split("/")[2];
          if (u.searchParams.has("v")) return u.searchParams.get("v");
        }
      } catch {
        console.warn("URL YouTube invalide :", url);
      }
      return null;
    },


    get_Vimeo_videoId(url) {
      try {
        const u = new URL(url);
        if (u.hostname.includes("vimeo.com")) {
          if (u.pathname.match(/^\/\d+$/)) {
            return u.pathname.slice(1);
          }
          const match = u.pathname.match(/\/(\d+)$/);
          if (match) return match[1];
          if (u.pathname.startsWith("/video/")) {
            return u.pathname.split("/")[2];
          }
        }
      } catch {
        console.warn("URL Vimeo invalide :", url);
      }
      return null;
    }

  },

 async mounted() {
    await this.recupeArtiste();
    await this.recupeQuestion();
  
    //reccuperation de l'id en parametre
    const ExtraitId = this.$route.params.id;
    console.log(ExtraitId);

    if (ExtraitId != null) {
        //reccuperation de l'Extrait via l'id
      this.current_extrait =  markRaw(await Extrait.detail(ExtraitId));
      console.log(this.current_extrait);
      this.interviews = markRaw(await this.current_extrait.interviews());
      console.log(this.interviews);
      this.tags = markRaw(await this.current_extrait.tags());


      if(await this.current_extrait.question != null){
        const question =  markRaw(await this.current_extrait.question);
        this.laselectedQuestion = question.texte;
        this.current_extrait.question.uuid = question.uuid;
        this.current_extrait.question = question.uuid;
      }

      if(await this.current_extrait.artiste != null){
        const artiste = markRaw(await this.current_extrait.artiste);
        this.laselectedArtiste  = artiste.name;
        this.current_extrait.artiste = artiste.uuid;
        this.current_extrait.artiste.uuid = artiste.uuid;
      }

      
      

    }else{
      this.current_extrait = markRaw( await new Extrait({}));
      this.create = true;
    }
    this.urlVimeoReconstruit = this.current_extrait.vimeo_url;
    this.urlyoutubeReconstruit =this.current_extrait.youtube_url;
    this.migniature_video()

    

  }
};






</script>

<template>
    <comp_baradmin/>

    <form v-if="current_extrait" action="" class="row" style="--bs-gutter-x: 0em;">




      <div class="row"  style="--bs-gutter-x: 0em;">
        
        <RouterLink  class="col-md-4" style="text-decoration: none; color: inherit; padding: 1em;" :to="{path: '/lecteur_video/' + current_extrait.uuid }">
          <img :src="thumbnail" class="migniature" alt="migniature">
        </RouterLink>

        <div class="col-md-6 scroller" style="width: 65%; height: 33vh;">
          
        <div class="row"  style="--bs-gutter-x: 0em;">
            <div class=" input-group mb-3" >
                <span  class="input-group-text colovert" id="basic-addon3" > Titre :</span>
                <input list="Questiondata" id="question" name="question" class="form-control"   v-model="this.current_extrait.titre"/>
            </div>
        </div>

          <div class="row"  style="--bs-gutter-x: 0em;">
            <div class=" input-group mb-3" >
                <span  class="input-group-text colovert" id="basic-addon3" > Question :</span>

                <input list="Questiondata" id="question" name="question" class="form-control colovert" style="border: solid; border-color: var(--vert-midel);"  v-model="laselectedQuestion" @input="FoncSelectedQuestion"/>
                
                <datalist id="Questiondata">
                <option v-for="question in listeQuestion" :key="question.id" :value="question.texte" :label="question.texte" > </option> 
                </datalist>


                <button class="bt" style="background-color: var(--gris-ultraclair);">  <img src="/imgs/add_black.svg" alt="add" class="col "> </button>
            </div>
          </div>


          <div class="row"  style="--bs-gutter-x: 0em;">
              <div class="input-group mb-3" >
                <span class="input-group-text colovert" >Artiste :</span>
                <input list="Artistedata" id="choixArtiste" name="choixArtiste" class="form-control colovert" style="border: solid; border-color: var(--vert-midel);"   v-model="laselectedArtiste" @input="SelectedArtisteId">
                
                <datalist id="Artistedata">
                <option v-for="artiste in listeArtiste" :key="artiste.id" :value="artiste.name" :label="artiste.name" > </option> 
                </datalist>

                <button class="bt" type="button" @click="creerNouveauArtiste" style="background-color: var(--gris-ultraclair);"> <img src="/imgs/add_black.svg" alt="add" class="col  "> </button>
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
              <input type="text" class="form-control textfield" id="youtube" placeholder="youtube_url" @change="migniature_video" v-model="this.urlyoutubeReconstruit" >
            </div>
          </div>
            

          <div class="row"  style="--bs-gutter-x: 0em;">
              <div class="input-group mb-3 ">
                <span class="input-group-text colovert" id="basic-addon2">vimeo_url :</span>
                <input type="text" class="form-control textfield" id="vimeo" placeholder="vimeo_url" @change="migniature_video" v-model="this.urlVimeoReconstruit">
              </div>
          </div>
          

          <div class="row"  style="--bs-gutter-x: 0em;">
            <div class="input-group">
              <textarea type="aera" id="description" placeholder="Description" style="background-color: var(--gris-ultraclair); border:solid 0.3em;  border-color: var(--vert-pale);" class="form-control" v-model="this.current_extrait.description"></textarea>
            </div>
          </div>

            <div v-if="!create" class="row" style="margin-right: 0em; margin-left: 0em;">
              <h1 class="row pcentrer"> Tableau des Playlist
                 <div class="bt btn row"  @click="popup = !popup" style="width: 8%; border-radius: 100%; margin-right:0px; margin-left: 0px;"> <img src="/imgs/search.svg" alt="Edit" style="width: 100%;"> </div>
              </h1>
             
              <table  class="ultagger table tables table-striped">
                  <thead>
                      <tr>
                          <th class="btgrisv2  col">Nom Playlist</th>
                          <th class="btgrisv2  col">paramètre</th>
                      </tr>
                  </thead>
                  <tbody class="tobodd">
                      <tr class="col" v-for="interview in this.interviews">
                          <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/' + interview.uuid"> {{ interview.titre }} </RouterLink> </td>
                          <td> <RouterLink class="container container_extrait col "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/' + interview.uuid"> <button class="bt col"> modifier </button></RouterLink>  <RouterLink class="container container_extrait col "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/' + interview.uuid"> <button class="bt col"> supprimer </button> </RouterLink> </td>
                      </tr>
                  </tbody>
              </table>

              <RouterLink  to="/admin/interview/creer/" type="button" class="btn button-blanc col"> Ajouter un Playlist <img src="/imgs/add_black.svg" alt="add" class="col "> </RouterLink>
             
            </div>
        </div>
      </div>

      <div class="bottom_button">
          <RouterLink v-if="!create" to="/admin/extrait/" class="btn btn-outline-light"> <img src="/imgs/add.svg" alt="add">
              Ajouter un Extrait</RouterLink>
          <button @click="modificationDonnees()" type="button" class="btn btn-outline-success"> <img src="/imgs/save.svg"
                  alt="Enregistrer"> Enregistrer </button>
          <button @click="this.popupDelete = true" type="button" class="btn  btn-outline-danger"> <img
                  src="/imgs/delete.svg" alt="Supprimer"> Supprimer </button>
      </div>

      <supprimer v-if="popupDelete" :Element_Supp="current_extrait" @closePopup="popupDelete = false" />

    </form>
  

    <!-- Only render tags when current_interview is loaded -->
    <tags 
        v-if="current_extrait"
        :video="current_extrait"
        @update:tagsCreated="handleTagsCreated"
        @update:tagsDisconnected="handleTagsDisconnected"
        @update:tagsConnected="handleTagsConnected"
    />
    
   

    <div v-if="popup === true">  <popup_interview v-on:ecoutepopup="popupchange" /> </div>

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

.secondpart{
  display: flex;
  justify-content: center;
  align-content: center;
  align-items: center;
  margin: 1em;
}





</style>
