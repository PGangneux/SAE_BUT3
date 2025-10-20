<script>
export default {
    name: "page_admin",
    components: {
    },
};


</script>

<template>
  <h1> Admin </h1>


  <nav>
    <ul>
      <li>
          <div class="card">
            <h1 class="text-center" > Extrait </h1>
            <div class="text-center">
              <img src="../assets/imgs/video.svg" alt="Video logo" height="87" width="100">
            </div>
          </div>
      </li>
      <li>
          <div class="card">
            <h1 class="text-center" > interview </h1>
            <div class="text-center">
              <img src="../assets/imgs/playlist.svg" alt="playlist logo" height="87" width="100">
            </div>
          </div>
      </li>

      <li>
          <div class="card">
            <h1 class="text-center" > User </h1>
            <div class="text-center">
              <img class="text-center" src="../assets/imgs/adminlogo.svg" alt="admin logo" height="87" width="100">
            </div>
          </div>
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
  filter: blur(0.25) drop-shadow(20px 13px 4px #000000) ;
 
}

ul {
  list-style-type: none;
}



</style>
