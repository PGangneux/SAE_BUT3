<script>
import comp_baradmin from '../../../components/components_admin/nav_admin.vue';

export default {
    name: "page_admin_listuser",
    components: {
        comp_baradmin,
    },data() {
        return {
            tags: ['Foo', 'Bar', 'Bsq', 'Bar2','GAB','GAB'],
        };
    }
};


</script>

<template>

    <comp_baradmin/>
    
    <div class="row"> 
        <button class="col btgris btn"> Ajouter un utilisateur  <img src="/imgs/add.svg" alt="ajouter"></button>


        <div class="container col">
            <div class="search-bar">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                    <button class="btn btn-outline-secondary" type="button" id="search-addon">
                            <img src="/imgs/search.svg" alt="button search">
                        </button>
                </div>
            </div>
        </div>


    </div>

    <div class="raw">    

        <div class="raw">
            <button scope="col" class="btgris btn" > Pseudo</button>
            <button scope="col" class="btgris btn" > Nom</button>
            <button scope="col" class="btgris btn" > Prénom</button>
            <button scope="col" class="btgris btn" > État du compte</button>
        </div>

        <table class="scroller ultagger table tables table-bordered">
            <thead>
            </thead>
            <tbody>
                <tr class="col" v-for="tag in tags">
                    <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" to="/admin/user/edit"> {{ tag }} </RouterLink> </td>
                    <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" to="/admin/user/edit"> {{ tag }} </RouterLink> </td>
                    <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" to="/admin/user/edit"> {{ tag }} </RouterLink> </td>
                    <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" to="/admin/user/edit"> {{ tag }} </RouterLink> </td>
                </tr>
            </tbody>
        </table>
    </div>
        




</template>

<style scoped>

body{
    background-color: var(--noir);
}




.card{
  background-color: var(--gris-moyen);
  filter: drop-shadow(20px 13px 4px var(--noir)) ;

 
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

.tables{
    width: 100%;
}

.btgris{
    color:white;
    background-color:var(--gris-moyen);
    border-radius: 2em;
    border: none;
    
}





.search-bar {
    max-width: 500px;
    margin: auto auto;
}

.search-bar .input-group {
    border-radius: 30px;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.search-bar .form-control {
    border: none;
    padding-left: 20px;
}

.search-bar .btn {
    border: none;
    padding: 10px 20px;
}

</style>
