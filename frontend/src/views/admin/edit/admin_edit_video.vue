<script>

import comp_baradmin from "../../../components/components_admin/nav_admin.vue";

import comp_popup from "../../../components/components_admin/popup_admin_edit.vue";

export default {
  name: "page_admin_detail_video",
  components: {
    comp_baradmin,
    comp_popup,

  },data() {
        return {
            tags: ['Foo', 'Bar', 'Bsq', 'Bar2','GAB','GAB'],
            popup: false
        };
    }
};



</script>

<template>
    <comp_baradmin/>


    <form action="" class="row">

      <div class="row" >
        <div class="col-md-4">
          <img src="/imgs/width551.png" class="migniature" alt="migniature">
        </div>

        <div class="col-md-6 scroller2">
            <div class="row" >
              <div class="input-group mb-3 ">
                <span class="input-group-text" id="basic-addon1">youtube_url :</span>
                <input type="text" class="form-control textfield" placeholder="youtube_url" aria-label="youtube_url" aria-describedby="basic-addon1">
              </div>
            </div>




            <div class="row" >
                <div class="input-group mb-3 ">
                  <span class="input-group-text" id="basic-addon2">vimeo_url :</span>
                  <input type="text" class="form-control textfield" placeholder="vimeo_url" aria-label="vimeo_url" aria-describedby="basic-addon2">
                </div>
            </div>
          
            <div class="row" >
              <div class=" input-group mb-3" >
                  <span  class="input-group-text" id="basic-addon3" > Question :</span>
                  <input type="text" id="question" name="question" class="textfield form-control col" placeholder="Question" aria-label="Question" aria-describedby="basic-addon3" />
              </div>
            </div>


            <div class="input-group mb-3" >
                <span class="input-group-text" >Artiste :</span>
                <input type="text" id="inputartist" name="inputartist" class="textfield form-control" placeholder="Artiste" aria-label="Artiste" />

                <select id="choix" name="choix" class="form-control" >
                  <!-- utiliser js TODO -->
                   <option value=""> > </option>
                  <option value="option1"> Artiste 1</option> 
                  <option value="option2"> Artiste 2</option>
                  <option value="option3"> Artiste 3</option>
                </select>

                <div class="form-control">
                  <img   class="col" src="/imgs/date.svg" alt="">
                  <label class="col" for="name4"> Date </label>
                  <input class="col" type="date" lang="fr" id="name4" name="name4" />
                  <!-- rendre jolie TODO -->
                </div>

            </div>



            <div class="row" >
              <div class="form-group">
                <textarea type="aera" placeholder="Description" class="form-control"></textarea>
              </div>
            </div>
        </div>
      </div>

      <div class="row pad" >
        <div class="input-group col" >
          <span class="input-group-text" id="basic-addon8" >Interview Actuelle :</span>
          <input type="text" id="name" name="name" class="textfield form-control"  placeholder="Interview Actuelle" aria-label="Interview Actuelle :" aria-describedby="basic-addon8"  />
        </div>

        <div class="bt btn col"  @click="popup = !popup" > <img src="/imgs/add.svg" alt="Edit"> Edit</div>
        <button  type="submit"   class="bt btn col" > <img src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>
        <button  type="reset"  class="bt btn col" > <img src="/imgs/cancel.svg" alt="Annuler"> Annuler </button>

      </div>

    </form>
    
    <div class="row grisee " >
      <h1 class="row pcentrer" > Meta Donnée </h1>
      <div class="row">
        <ul class="scroller2  row">
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
  color: var(--blanc);
  background-color: var(--gris-taupe);
}

.bt{
    color: var(--blanc);
    background-color:var(--vert-pale);
    border-radius: 2em;
    
}

.migniature{
  border-radius: 2em;
}

option{
  display : "none"
}

label{
  color: var(--vert-neon);
}

</style>
