<script>

import comp_baradmin from "../../components/components_admin/nav_admin.vue";
import comp_petit_extrait from '../../components/components_admin/Admin_presentation_petit_extrait.vue';


export default {
    name: "page_admin_edit_interview",
    components: {
      comp_baradmin,
      comp_petit_extrait,

    },data() {
        return {
            tags: ['Foo', 'Bar', 'Bsq', 'Bar2','GAB','GAB']
    };
  }

};


</script>

<template>

<comp_baradmin/>

<h1 class="text-center"> Admin </h1>

<div class="row" >
    <div class="col-md-5 aggrandir">
        <div class="container row ">
            <div class="search-bar grisee">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                    <button class="btn btn-outline-secondary" type="button" id="search-addon">
                            <img src="/imgs/search.svg" alt="button search">
                    </button>
                </div>
            </div>

            <ul class="scroller2  row">
                <li class="row carte" v-for="tag in tags">
                    <comp_petit_extrait/>
                </li>
            </ul>
        </div>


    </div>

    <div class="col-md-5">
        <h1> Titre - Playlist </h1>
    </div>
</div>



</template>

<style scoped>



.carte{
  padding: 5px;
  margin: 5px;
}



.card{
  background-color: var(--gris-moyen);
  filter: drop-shadow(20px 13px 4px var(--noir)) ;

 
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

  height: 80%;
  overflow-y: scroll;
  scrollbar-color: var(---blanc) #A6A6A6;
  scrollbar-width: thin;
}


.aggrandir{
  display: flex;
  flex-wrap: nowrap;
  list-style-type: none;
  flex-grow: 1;

}

.grisee{
  background-color: var(--gris-moyen);
}

</style>
