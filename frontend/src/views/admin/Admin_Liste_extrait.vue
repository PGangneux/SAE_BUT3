<script>

import comp_baradmin from '../../components/components_admin/HeaderbarAdmin.vue';

import comp_extrait from '../../components/components_admin/Admin_presentation_extrait.vue';

export default {
    name: "page_admin_listextrait",
    components: {
      comp_baradmin,
      comp_extrait,
    },
};


</script>

<template>

  <comp_baradmin/>

  <h1 class="text-center"> Admin </h1>


  <comp_extrait/>


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



</style>
