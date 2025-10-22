<script>

import comp_baradmin from "../../components/components_admin/nav_admin.vue";

import comp_extrait from '../../components/components_admin/Admin_presentation_extrait.vue';

import comp_admin_trie_extrait from '../../components/components_admin/Admin_trie.vue';

export default {
    name: "page_admin_listextrait",
    components: {
      comp_baradmin,
      comp_extrait,
      comp_admin_trie_extrait,
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
    <comp_admin_trie_extrait/>

    <div class="col-md-9 aggrandir">
      <ul class="scroller2  row">
        <li class="row carte" v-for="tag in tags">
            <comp_extrait/>
        </li>
      </ul>
      
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


</style>
