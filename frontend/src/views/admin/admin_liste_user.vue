<script>
import comp_baradmin from '../../components/components_admin/nav_admin.vue';

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
        <button class="col btgris"> Ajouter un utilisateur  <img src="/imgs/add.svg" alt="ajouter"></button>

        <div class="col">
            <input type="search" id="site-search" name="q" class="col" />
            <button class="col" ><img src="/imgs/search.svg" alt="button search"></button>
        </div>

    </div>

    <div class="raw">    
        <table class="scroller ultagger table table-bordered">
            <thead>
                <tr>
                    <th scope="col">Pseudo</th>
                    <th scope="col">Nom</th>
                    <th scope="col">Prénom</th>
                    <th scope="col">État du compte</th>
                </tr>
            </thead>
            <tbody>
                <tr class="col" v-for="tag in tags">
                    <td> {{ tag }} </td>
                    <td> {{ tag }} </td>
                    <td> {{ tag }} </td>
                    <td> {{ tag }} </td>
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


.btgris{
    color:white;
    background-color:var(--gris-moyen);
    border-radius: 2em;
    border: none;
    
}



</style>
