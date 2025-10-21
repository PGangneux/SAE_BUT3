<script>
import comp_baradmin from '../../components/components_admin/HeaderbarAdmin.vue';

export default {
    name: "page_admin_listuser",
    components: {
        comp_baradmin,
    },
};


</script>

<template>

    <comp_baradmin/>
    <h1 class="text-center"> Admin </h1>


    <nav>
        <ul>
        <li>

            <RouterLink class="card" to="/admin/extrait">
                
                <h1 class="text-center" > Extrait </h1>
                <div class="text-center align-middle">
                <img src="../../assets/imgs/video.svg" alt="Video logo" height="87" width="100">
                </div>
            </RouterLink>

        </li>

        <li>
            <RouterLink class="card" to="/admin/interview">
                <h1 class="text-center" > interview </h1>
                <div class="text-center">
                <img src="../../assets/imgs/playlist.svg" alt="playlist logo" height="87" width="100">
                </div>
            </RouterLink>

        </li>

        <li>
            <RouterLink class="card" to="/admin/user">

            <h1 class="text-center" > Extrait </h1>
            <div class="text-center align-middle">
              <img src="/imgs/video.svg" alt="Video logo" height="87" width="100">
            </div>
          
            </RouterLink>

        </li>
        </ul>
    </nav>



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
