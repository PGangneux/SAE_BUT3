<script>
export default {
  name: "page_admin_acceuil",
  
};


</script>

<template>
  <h1 class="text-center"> Admin </h1>
  <nav>
    <ul class="blocchoix" style="padding-right:1em ; padding-left: 1em;">
      <li>
        <RouterLink class="card col" to="/admin/extrait">
          <h1 class="text-center">Question-Extrait</h1>
          <div class="text-center align-middle">
            <img src="/imgs/video.svg" alt="Video logo" height="311" width="311">
          </div>
        </RouterLink>
      </li>
      <li>
        <RouterLink class="card col" to="/admin/interview">
          <h1 class="text-center">Interview-Playlist</h1>
          <div class="text-center">
            <img src="/imgs/playlist.svg" alt="playlist logo" height="311" width="311">
          </div>
        </RouterLink>
      </li>
      <li>
        <RouterLink class="card col" to="/admin/user">
          <h1 class="text-center">User</h1>
          <div class="text-center">
            <img class="text-center" src="/imgs/adminlogo.svg" alt="admin logo" height="311" width="311">
          </div>
        </RouterLink>
      </li>
    </ul>
  </nav>
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

.blocchoix{
  display: flex;
  text-align: center;
  align-content: center;
  align-items: center;
  justify-content: space-around;
}

ul {
  display: flex;
  list-style-type: none;
  justify-content: space-between;
}
</style>
