<script>
export default {
    name: "page_admin_listuser",
    components: {
    },
};


</script>

<template>
  <h1 class="text-center"> Admin </h1>


  <nav>
    <ul>
      <li>

          <RouterLink class="card" to="/admin/extrait">
            
            <h1 class="text-center" > Extrait </h1>
            <div class="text-center align-middle">
              <img src="/imgs/video.svg" alt="Video logo" height="87" width="100">
            </div>
          </RouterLink>

      </li>

      <li>
          <RouterLink class="card" to="/admin/interview">
            <h1 class="text-center" > interview </h1>
            <div class="text-center">
              <img src="/imgs/playlist.svg" alt="playlist logo" height="87" width="100">
            </div>
          </RouterLink>

      </li>

      <li>
        
          <RouterLink class="card" to="/admin/user">

            <h1 class="text-center" > User </h1>
            <div class="text-center">
              <img class="text-center" src="/imgs/adminlogo.svg" alt="admin logo" height="87" width="100">
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
