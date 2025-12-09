<script>
import { markRaw } from 'vue';
import comp_baradmin from "../../../components/components_admin/nav_admin.vue";
import comp_petit_extrait from '../../../components/components_admin/Admin_presentation_petit_extrait.vue';

import Interview from '../../../model/interview.js';
import Extrait from "../../../model/extrait.js";

export default {
    name: "page_admin_edit_interview",
    components: {
      comp_baradmin,
      comp_petit_extrait,

    },data() {
        return {
            Extraitlist : [],
            current_interview:{type:Interview},
            current_list_extraits:{type:Extrait},
            taillelist1:0,   
            taillelist2:0, 
    };
  },
  computed: {
      description: {
        get() {
          return this.current_interview?.description ? this.current_interview.description : 'Chargement...';
        },
      },
  },

 async mounted() {
    //reccuperation de l'id en parametre
    const InterviewId = this.$route.params.id;
    // console.log("ID de l'Interview' :", InterviewId);

    //reccuperation de l'Extrait via l'id
    this.current_interview =  markRaw(await Interview.detail(InterviewId));
    this.Extraitlist = markRaw(await Extrait.list());
    this.current_list_extraits = markRaw(await this.current_interview.extraits());

    console.log(this.current_list_extraits);
    console.log(this.Extraitlist);
    
    this.taillelist1 = this.Extraitlist.length
    this.taillelist2 =this.current_list_extraits.length


    this.question = 'Chargement...';

      

  },

};


</script>

<template>

<comp_baradmin/>

<h1 class="text-center"> Edit Interview-Playlist </h1>

<div class="row" style=" margin-left: 0 !important; margin-right: 0 !important;">
        <h1> {{ this.current_interview.titre }} - Playlist </h1>

        <div class="row"  style=" margin-left: 0 !important; margin-right: 0 !important;">
          <div class="form-group">
            <textarea type="aera" placeholder="Description" style="background-color: var(--gris-ultraclair); border:solid 0.3em;  border-color: var(--vert-pale);" v-model="description" class="form-control"></textarea>
          </div>
        </div>
</div>

<div class="row" style=" margin-left: 0 !important; margin-right: 0 !important;" >
    <div class="col-md-4 aggrandir" style="background-color:var(--vert-midel); margin: 1%;">
        <div class="container row  pcentrer " style=" margin-left: 0 !important; margin-right: 0 !important;">

            <div class="row" style=" margin-left: 0 !important; margin-right: 0 !important;">
              <h1> Question-Extrait existant</h1>
              <h1> Total Question-Extrait : {{this.taillelist1}}</h1>
            </div>

            <div class="search-bar grisee">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                    <button class="btn btn-outline-secondary" type="button" id="search-addon">
                            <img src="/imgs/search.svg" alt="button search">
                    </button>
                </div>
            </div>

            <ul class="scroller2  row" style=" margin-left: 0 !important; margin-right: 0 !important;">
                <li class="row carte pcentrer" v-for="extraitv1 in this.Extraitlist" style=" margin-left: 0 !important; margin-right: 0 !important;">
                    <comp_petit_extrait :current_extrait=extraitv1 />
                </li>
            </ul>
        </div>
    </div>

    <div  class="col" ></div>

    <div class="col-md-4 aggrandir" style="background-color:var(--vert-pale); margin: 1%;">
        <div class="container row pcentrer  " style=" margin-left: 0 !important; margin-right: 0 !important;">

            <div class="row" style=" margin-left: 0 !important; margin-right: 0 !important;">
              <h1> Question-Extrait dans Playlist</h1>
              <h1> Total Question-Extrait : {{ this.taillelist2 }}</h1>
            </div>

            <div class="search-bar grisee">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                    <button class="btn btn-outline-secondary" type="button" id="search-addon">
                            <img src="/imgs/search.svg" alt="button search">
                    </button>
                </div>
            </div>

            <ul class="scroller2  row  " style=" margin-left: 0 !important; margin-right: 0 !important;">
                <li class="row carte pcentrer" v-for="extraitv2 in this.current_list_extraits" style=" margin-left: 0 !important; margin-right: 0 !important;">
                    <comp_petit_extrait :current_extrait=extraitv2 />
                </li>
            </ul>
        </div>
    </div>
</div>

<div class="row pad"  style=" margin-left: 0 !important; margin-right: 0 !important;">
            <RouterLink  to="/admin/extrait/creer/" class="btn button-blanc col"> Ajouter un Extrait <img src="/imgs/add_black.svg" alt="add" class="col "> </RouterLink>
            <button  type="submit"   class="bt btn col" > <img src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>
            <button  type="button"  class="btred btn col" > <img src="/imgs/delete.svg" alt="Supprimer"> Supprimer </button>
</div>


</template>

<style scoped>

.pad{
  padding-top: 1em;
  padding-bottom: 1em;
}

.carte{
  padding: 5px;
  padding-bottom: 1em;
  /*!margin: 5px; */
}

.btred{
    color: var(--blanc);
    background-color:var(--rouge);
    border-radius: 2em;
    
}

.card{
  background-color: var(--gris-moyen);
  filter: drop-shadow(20px 13px 4px var(--noir)) ;

 
}

.pcentrer{
margin-top: 1em;
justify-content: center
}

.button-blanc{
    background-color: var(--blanc);
}


.bt{
    color:white;
    background-color:var(--vert-pale);
    border-radius: 2em;
    
}




li > .card{
    padding: 20px 50px 150px;
    margin: 10px 10px 10px 10px;
  
}



ul {
  display: flex;
  list-style-type: none;
  justify-content: space-between;

  
}

.scroller2 {

  height: 100vh;
  overflow-y: scroll;
  scrollbar-color: var(---blanc) #A6A6A6;
  scrollbar-width: thin;
}


.aggrandir{
  /*! display: flex; */
  /*! flex-wrap: nowrap; */
  list-style-type: none;
  flex-grow: 1;

}

.grisee{
  background-color: var(--gris-moyen);
}

</style>
