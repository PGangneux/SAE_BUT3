<script>

export default {
    name: "comp_headerbaradmin",
};
</script>

<template>
        <nav class="headeradmin text-white py-3">
                <ul class="text-center">

                    <li class="nav-item text-white">
                        <RouterLink class="bt btn " to="/admin"> Accueil Admin </RouterLink>
                    </li>

                    <li class="nav-item text-white">
                        <RouterLink class="bt btn " to="/admin/extrait"> Extrait </RouterLink>
                    </li>

                    <li class="nav-item text-white ">
                        <RouterLink class="bt btn " to="/admin/user"> User </RouterLink>
                    </li>

                    <li class="nav-item text-white">
                        <RouterLink class="bt btn " to="/admin/interview">Playlist</RouterLink>
                    </li>
                </ul>
        </nav>
</template>

<style scoped>

.bt{
    color:white;
    background-color:var(--vert-pale);
    border-radius: 19%;
    
}

ul {
  display: flex;
  list-style-type: none;
  justify-content: space-between;

  
}

.headeradmin{
    background-color:var(--gris-moyen);
    margin: 10px 10px 10px 10px; 
}

</style>