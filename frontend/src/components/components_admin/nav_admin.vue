n<script>

export default {
    name: "comp_headerbaradmin",
};
</script>

<template>
        <nav class="headeradmin text-white navadmin">
                <ul class="text-center" style="padding:1em;">

                    <li class="nav-item text-white">
                        <RouterLink class="bt btn " to="/admin"> Accueil Admin </RouterLink>
                    </li>

                    <li class="nav-item text-white">
                        <RouterLink class="bt btn " to="/admin/extrait"> Extrait </RouterLink>
                    </li>

                    <li class="nav-item text-white">
                        <RouterLink class="bt btn " to="/admin/interview">Interview</RouterLink>
                    </li>
                    
                    <li class="nav-item text-white ">
                        <RouterLink class="bt btn " to="/admin/user"> User </RouterLink>
                    </li>
                </ul>
        </nav>
</template>

<style scoped>

.bt{
    color:white;
    background-color:var(--vert-pale);
    border-radius: 2em;
    
}

ul {
  display: flex;
  list-style-type: none;
  justify-content: space-around;
  flex-wrap: wrap;
}

li{
      padding-bottom: 1em;
}

.headeradmin{
    background-color:var(--gris-moyen);
    margin: 10px 10px 10px 10px; 
}

.navadmin{
    padding-top: 0.07em;
    padding-top:  0.07em;
    border-radius: 1em;
}

</style>