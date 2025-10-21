<script>

import comp_baradmin from "../../components/components_admin/headerbar_admin.vue";

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

    <div class="col aggrandir">
      <ul class="scroller2  row">
        <li class="row" v-for="tag in tags">
            <comp_extrait/>
        </li>
      </ul>
      
    </div>
  </div>



</template>

<style scoped>

body{
    background-color: #0F0F0F;
}


h1 {
  color: #ffffff;
}

.card{
  background-color: #2C2D32;
  filter: drop-shadow(20px 13px 4px #000000) ;

 
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
  scrollbar-color: #FFFFFF #A6A6A6;
  scrollbar-width: thin;
}


.aggrandir{
  display: flex;
  flex-wrap: nowrap;
  list-style-type: none;
  flex-grow: 1;

}


</style>
