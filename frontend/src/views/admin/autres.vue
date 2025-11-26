<script>
import comp_baradmin from "../../components/components_admin/nav_admin.vue";


export default {
    name: "page_autres",
    
    components: {
        comp_baradmin,
    },
    data() {
        return {
            listfictive:["a","a","b"],
            
            
        };
    }

};
</script>




<template>
    <comp_baradmin/>

    <h1 class="text-center">Autres</h1>

    <section class="row ligne">
        <h2 class="vert-neon">Questions</h2>

        <section class="row">

            <section class="col input-group mb-3">
                <span class=" col input-group-text colovert">nb Questions total</span>
                <span class=" col input-group-text">nb Questions total</span>
            </section>

            <section class="col input-group mb-3">
                <span class=" col input-group-text colovert">nb Questions utiliser</span>
                <span class=" col input-group-text">nb Questions utiliser</span>
            </section>

            <section class="col input-group mb-3">
                <span class=" col input-group-text colovert">nb Questions non utiliser</span>
                <span class=" col input-group-text">nb Questions non utiliser</span>
            </section>

        </section>

        <section>
            <table class="ultagger table tables table-striped">
                  <thead>
                      <tr>
                          <th class="btgrisv2  col">Question</th>
                          <th class="btgrisv2  col">Theme</th>
                          <th class="btgrisv2  col">nb dans extraits</th>
                      </tr>
                  </thead>
                  <tbody class="tobodd scroller">
                      <tr class="col" v-for="interview in this.listfictive">
                          <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> ha </RouterLink> </td>
                          <td> <RouterLink class="container container_extrait col "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> <button class="bt col"> modifier </button></RouterLink>  <RouterLink class="container container_extrait col "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> <button class="bt col"> supprimer </button> </RouterLink> </td>
                          <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> ha </RouterLink> </td>
                        </tr>
                  </tbody>
              </table>
        </section>


    </section>

    <section class="row ligne">
        <h2 class="vert-neon">Tags</h2>

        <section class="row"> 

            <section class="col input-group mb-3">
                <span class=" col input-group-text colovert">nb Tags total</span>
                <span class=" col input-group-text">nb Tags total</span>
            </section>

            <section class="col input-group mb-3">
                <label for="cheese" class="col input-group-text colovert">nb Tags utiliser</label>
                <p class="col textfield form-control" >nb Tags utiliser</p>
            </section>

            <section class="col input-group mb-3">
                <label for="cheese" class="col input-group-text colovert">nb Tags non utiliser</label>
                <p class="col textfield form-control" >nb Tags non utiliser</p>
            </section>
        </section>

        <section>
            <table class="ultagger table tables table-striped">
                  <thead>
                      <tr>
                          <th class="btgrisv2  col">name</th>
                          <th class="btgrisv2  col">nb dans interviews</th>
                          <th class="btgrisv2  col">nb dans extraits  </th>
                      </tr>
                  </thead>
                  <tbody class="tobodd scroller">
                      <tr class="col" v-for="interview in this.listfictive">
                          <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> ha </RouterLink> </td>
                          <td> <RouterLink class="container container_extrait col "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> <button class="bt col"> modifier </button></RouterLink>  <RouterLink class="container container_extrait col "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> <button class="bt col"> supprimer </button> </RouterLink> </td>
                          <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> ha </RouterLink> </td>
                        </tr>
                  </tbody>
            </table>
        </section>

    </section>

    <section class="row ligne">
        <h2 class="vert-neon">Artistes</h2>
        <section class="row">

            <section class="col input-group mb-3">
                <label for="cheese" class="col input-group-text colovert">nb Artistes total</label>
                <p class="col textfield form-control">nb Artistes total</p>
            </section>

            <section class="col input-group mb-3">
                <label for="cheese" class="col input-group-text colovert">nb Artistes utiliser</label>
                <p class="col textfield form-control ">nb Artistes utiliser</p>
            </section>

            <section class="col input-group mb-3">
                <label for="cheese" class="col input-group-text colovert">nb Artistes non utiliser</label>
                <p class="col textfield form-control">nb Artistes non utiliser</p>
            </section>

        </section>

        <section>
            <table class="ultagger table tables table-striped">
                  <thead>
                      <tr>
                          <th class="btgrisv2  col">Artistes</th>
                          <th class="btgrisv2  col">nation</th>
                          <th class="btgrisv2  col">styles</th>
                          <th class="btgrisv2  col">nb dans extraits  </th>
                          <th class="btgrisv2  col">nb dans interviews</th>
                      </tr>
                  </thead>
                  <tbody class="tobodd scroller">
                      <tr class="col" v-for="interview in this.listfictive">
                          <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> ha </RouterLink> </td>
                          <td> <RouterLink class="container container_extrait col "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> <button class="bt col"> modifier </button></RouterLink>  <RouterLink class="container container_extrait col "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> <button class="bt col"> supprimer </button> </RouterLink> </td>
                          <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> ha </RouterLink> </td>
                          <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> ha </RouterLink> </td>
                          <td> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="'/admin/interview/'"> ha </RouterLink> </td>
                        </tr>
                  </tbody>
            </table>
        </section>

    </section>

</template>

<style scoped>


.vert-neon { 
    color : var(--vert-neon);
    justify-self: center;
}

.colovert{
  border-color: var(--vert-pale);
  background-color:var(--vert-pale);
  color: var(--blanc);
}

.local-flex {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;
    flex: 1 1 200px;
}
.ligne {
    border-radius: 20px;    
    margin: 1em;
    background-color: var(--gris-moyen);
}
.logo{
    max-width: 100px;
}

.textfield{
  background-color: var(--gris-ultraclair);
}

</style>