<script>

import comp_baradmin from "../../../components/components_admin/nav_admin.vue";

import comp_popup from "../../../components/components_admin/popup_admin_edit.vue";
import Extrait from "../../../model/extrait";

import { markRaw } from 'vue';

export default {
  name: "page_admin_detail_video",
  components: {
    comp_baradmin,
    comp_popup,

  },data() {
        return {
            current_extrait : {type:Extrait},
            tags:[],
            question : null,
            popup: false
        };
    }
    
    ,computed: {
      youtubeUrl: {
        get() {
          return this.current_extrait?.youtube_url ? 'https://www.youtube.com/watch?v=' + this.current_extrait.youtube_url : 'Chargement...';
        },
        set(value) {
          const id = value.split('v=')[1];
          if (id) this.current_extrait.youtube_url = id;
        }
      },

      vimeoUrl: {
        get() {
          
          return this.current_extrait?.vimeo_url ? 'https://vimeo.com/' + this.current_extrait.vimeo_url : 'Chargement...';
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


 async mounted() {
    //reccuperation de l'id en parametre
    const ExtraitId = this.$route.params.id;
    console.log("ID de l'Extraits' :", ExtraitId);

    //reccuperation de l'Extrait via l'id
    this.current_extrait =  markRaw(await Extrait.detail(ExtraitId));
    console.log(this.current_extrait);

    
    await this.current_extrait.artiste;
    await this.current_extrait.question;
    this.question = 'Chargement...';

      

  },


};



</script>

<template>
    <comp_baradmin/>

    <form action="" class="row" style="--bs-gutter-x: 0em;">

      <div class="row"  style="--bs-gutter-x: 0em;">
        <div class="col-md-4">
          <img src="/imgs/width551.png" class="migniature" alt="migniature">
        </div>

        <div class="col-md-6">
          <div class="row"  style="--bs-gutter-x: 0em;">
            <div class=" input-group mb-3" >
                <span  class="input-group-text colovert" id="basic-addon3" > Question :</span>
                <input type="text" id="question" name="question" class="textfield form-control col" placeholder="Question" v-model="question"  />
            </div>
          </div>

          <div class="input-group mb-3" >
            <span class="input-group-text colovert" >Artiste :</span>
            <input type="text" id="inputartist" name="inputartist" class="textfield form-control" v-model="test" />

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
              <input class="col" type="date" lang="fr" id="name4" name="name4" v-model="this.current_extrait.date"/>
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

            <div class="row">
              <h1 class="row pcentrer"> Tableau des Playlist</h1>
              <table class="ultagger table tables table-striped">
                  <thead>
                      <tr>
                          <th class="btgrisv2  col">Nom Playlist</th>
                          <th class="btgrisv2  col">paramètre</th>
                      </tr>
                  </thead>
                  <tbody class="tobodd scroller">
                      <tr class="col" v-for="tag in tags">
                          <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" to="/admin/interview/edit"> {{ tag }} </RouterLink> </td>
                          <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" to="/admin/interview/edit"> <button class="bt col"> update </button> <button class="bt col"> supprimer </button> </RouterLink> </td>
                      </tr>
                  </tbody>
              </table>
            </div>
        </div>
      </div>


      <div class="row pad"  style="--bs-gutter-x: 0em;">
        <div class="bt btn col"  @click="popup = !popup" > <img src="/imgs/add.svg" alt="Edit"> Edit</div>
        <button  type="submit"   class="bt btn col" > <img src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>
        <button  type="reset"  class="bt btn col" > <img src="/imgs/cancel.svg" alt="Annuler"> Annuler </button>

      </div>

    </form>
    
    <div class="row grisee "  style="--bs-gutter-x: 0em;">
      <h1 class="row pcentrer"  style="--bs-gutter-x: 0em;"> Meta Donnée </h1>
      <div class="row">
        <ul class="scroller2  row" style="--bs-gutter-x: 0em;">
          <li class="col" v-for="tag in tags">
            <div class="row">
              <img src="/imgs/labeltags.svg" class="col" alt="labelle tags" height="50" width="50">
              <p class="col">{{ tag }}</p>
            </div>
          </li>
        </ul>
      </div>
    </div>
    
   

    <div v-if="popup === true">  <comp_popup/> </div>

    </template>

<style scoped>
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


.scroller2 {
  height: 100%;
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
    width: 100%;
}

.ultagger {
    list-style-type: none;

}

.scroller {
    width: 300px;
    height: 100px;
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

</style>
