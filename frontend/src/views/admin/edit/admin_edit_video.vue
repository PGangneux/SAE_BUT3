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
          <img src="/imgs/width550.png" class="migniature" alt="migniature">
        </div>

        <div class="col-md-6 ">
            <div class="row" >
              <div class="col grisetround" >
                <label for="urlyoutube">youtube_url :</label>
                <input type="text" id="urlyoutube" name="urlyoutube" class="textfield" placeholder="youtube_url" />
              </div>
            </div>
          


            <div class="row" >
                <div class="col grisetround" >
                  <label for="urlvimeo">vimeo_url :</label>
                  <input type="text" id="urlvimeo" name="urlvimeo" class="textfield" placeholder="vimeo_url" />
                </div>
            </div>
          

            <div class="row" >
                <label for="question"  class="col" > Question :</label>
                <input type="text" id="question" name="question" class="textfield col" placeholder="Question" />
            </div>

            <div class="row" >
                <label for="name3"  class="col" >Artiste :</label>
                <input type="text" id="name3" name="name3" class="textfield col" placeholder="Artiste" />

                <select id="choix" name="choix" class="col" >
                  <!-- utiliser js TODO -->
                  <option value="option1"> Artiste 1</option> 
                  <option value="option2"> Artiste 2</option>
                  <option value="option3"> Artiste 3</option>
                </select>

                <div class="col">
                  <img   class="col" src="/imgs/date.svg" alt="">
                  <label class="col" for="name4"> Date </label>
                  <input class="col" type="date" lang="fr" id="name4" name="name4" />
                  <!-- rendre jolie TODO -->
                </div>

            </div>
            <div class="row" >
              <input type="aera" placeholder="Description" />
            </div>
        </div>
      </div>

      <div class="row" >
        <div class="col grisetround" >
          <label for="name">Interview Actuelle :</label>
          <input type="text" id="name" name="name" class="textfield" placeholder="question de l'interview" />
        </div>

        

        <div class="bt btn col"  @click="popup = !popup" >
          <img src="/imgs/add.svg" alt="Edit"> <p class=" col" >Edit</p>
        </div>

        <button  type="submit"   class="bt btn col" > <img src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>
        <button  type="reset"  class="bt btn col" > <img src="/imgs/cancel.svg" alt="Annuler"> Annuler </button>


      </div>

    </form>
    
    <div class="row grisee" >
      <p class="row" > Meta Donnée </p>
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
