<script setup>
import { ref } from 'vue'

defineProps({
  msg: String,
})

const count = ref(0)
</script>

<template>
  <h1>{{ msg }}</h1>


  <nav>
    <ul>
      <li>
          <div class="card">
            <h1> Extrait </h1>
        
            <img src="../../assets/video.svg" alt="Video logo" height="87" width="100">
            
          </div>
      </li>
      <li>
          <div class="card">
            <h1> interview </h1>
            <img src="../../assets/playlist.svg" alt="playlist logo" height="87" width="100">
          </div>
      </li>

      <li>
          <div class="card">
            <h1> User </h1>
            <img src="../../assets/adminlogo.svg" alt="admin logo" height="87" width="100">
          </div>
      </li>
    </ul>
  </nav>


</template>

<style scoped>
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
