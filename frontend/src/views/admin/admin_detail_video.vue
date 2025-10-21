<script>

import comp_baradmin from "../../components/components_admin/nav_admin.vue";


export default {
  name: "page_admin_detail_video",
  components: {
    comp_baradmin,
  },
};


</script>

<template>
    <comp_baradmin/>


    <h1 class="text-center"> Details </h1>
 
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
</style>
