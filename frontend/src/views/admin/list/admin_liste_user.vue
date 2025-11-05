<script>
import { markRaw } from 'vue';
import comp_baradmin from '../../../components/components_admin/nav_admin.vue';

import User from "../../../model/utilisateur.js";

export default {
    name: "page_admin_listuser",
    components: {
        comp_baradmin,
    },data() {
        return {
            utilisateurs:{type:User},
        };
    },

    async mounted() {
        
        this.utilisateurs = markRaw(await User.list());
        // console.log("liste des utilisateurs")
        console.log(this.utilisateurs)
    },
};


</script>

<template>

    <comp_baradmin/>

    <h1 class="text-center">User</h1>

    <div class="row"> 
        <button class="col btgris btn"> Ajouter un utilisateur  <img src="/imgs/add.svg" alt="ajouter"></button>


        <div class="container col">
            <div class="search-bar">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                    <button class="btn btn-outline-secondary buttonsearch" type="button" id="search-addon">
                            <img src="/imgs/search.svg" alt="button search">
                    </button>
                </div>
            </div>
        </div>


    </div>

    <div class="raw main-triev2">    


        <table class="scroller ultagger table tables table-striped ">
            <thead>
                <tr>
                    <th class="btgrisv2  col">Pseudo</th>
                    <th class="btgrisv2  col">Nom</th>
                    <th class="btgrisv2  col">Prénom</th>
                    <th class="btgrisv2  col">État du compte</th>
                </tr>
            </thead>
            <tbody class="tobodd">
                <tr class="col" v-for="utilisateur in this.utilisateurs">
                    <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="{path:'/admin/user/'+ utilisateur.uuid}"> {{ utilisateur.pseudo }} </RouterLink> </td>
                    <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="{path:'/admin/user/'+ utilisateur.uuid}"> {{ utilisateur.nom }} </RouterLink> </td>
                    <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="{path:'/admin/user/'+ utilisateur.uuid}"> {{ utilisateur.prenom }} </RouterLink> </td>
                    <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="{path:'/admin/user/'+ utilisateur.uuid}"> <button class="bt"> Details </button> </RouterLink> </td>
                </tr>
            </tbody>
        </table>
    </div>
        




</template>

<style scoped>

body{
    background-color: var(--noir);
}


.main-triev2{
    padding: 2em;
}

.card{
  background-color: var(--gris-moyen);
  filter: drop-shadow(20px 13px 4px var(--noir)) ;

 
}

li > .card{
    padding: 20px 50px 150px;
    margin: 10px 10px 10px 10px;
  
}

.table-striped {
    --bs-table-bg: var();         
    --bs-table-striped-bg: var(); 
    --bs-table-color: #1a1a1a;      
    --bs-table-striped-color: #1a1a1a; 
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



.btgrisv2{
    color:white;
    background-color:var(--gris-moyen);
    padding: 1em;
}

.tobodd{
    padding-top: 1em;
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

.buttonsearch{
    background-color: var(--vert-pale);
}






</style>



