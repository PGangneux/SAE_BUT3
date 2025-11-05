<script>
import { markRaw} from 'vue';
import Interview from '../../../model/interview.js';

import comp_baradmin from "../../../components/components_admin/nav_admin.vue";


export default {
  name: "page_admin_interview",
  components: {
    comp_baradmin,

  },data() {
        return {
            interviews:{type:Interview},
            dico_interviews:{},
        };
    },


  async mounted() {
    //console.log("mounted admin interview list");
    this.interviews = markRaw(await Interview.list());

    

    try {
        for (let interview of this.interviews) {
            this.dico_interviews[interview.uuid] = {"length": (await interview.extraits).length, "tags": markRaw(await interview.tags)};
            //console.log(markRaw(this.dico_interviews));
        }



    } catch (error) {
      console.error('Erreur lors de la récupération des interviews ou des extraits:', error);
    }
  },
  methods: {
    tags_to_string(tags_array) {
        let string_tags = "";
        for (let tag of tags_array){
            string_tags += tag.name + " ";
        }
        return string_tags.trim();
    },


},
};




</script>

<template>

<comp_baradmin/>

<h1 class="text-center">Interview-Playlist</h1>

<div class="grisee row " style="margin-right:0;margin-left:0; padding-left: 10px; padding-right: 20px;">
    
    <div class="col-md-4 main-trie">

        <div class="row ">
            <button type="button" class="btn button-blanc col"> Ajouter un Playlist <img src="/imgs/add_black.svg" alt="add" class="col "> </button>
        </div>

        
        <div class="container col recherche">
            <div class="search-bar">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                    <button class="btn btn-outline-secondary buttonsearch" type="button" id="search-addon">
                            <img src="/imgs/search.svg" alt="button search">
                        </button>
                </div>
            </div>
        </div>

        <div class="row">
            <button class="bt btn col ">Date</button>
            <button class="bt btn col ">Name</button>
        </div>

        <div class="row  trie-tags centrer">

            <p class="row pcentrer">Trier par tag</p>

            <!--tagfully futur probleme-->

            <ul class="scroller ultagger row tagsfully">
                <li class="col" v-for="tag in tags">
                    <button class="btn btn-primary"> {{ tag }} </button>
                </li>
            </ul>
        </div>
    </div>

    <div class="col-md-6 recherche aggrandir">
            <table class="scroller ultagger table tables  table-bordered">
                <thead>
                    <tr>
                        <th class="btgrisv2" scope=" col">Nom interview</th>
                        <th class="btgrisv2" scope=" col">Nb video</th>
                        <th class="btgrisv2" scope=" col">Tags</th>
                    </tr>
                </thead>
                <tbody>
                    
                        <tr class="col"  v-for="interview in this.interviews">
                            
                                <td class="col"> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="{path:'/admin/interview/'+ interview.uuid}"> {{ interview.titre }} </RouterLink></td>
                                <td class="col"> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;"  :to="{path:'/admin/interview/'+ interview.uuid}"> {{ this.dico_interviews[interview.uuid] ? this.dico_interviews[interview.uuid]["length"] : null}} </RouterLink></td>
                                <td class="col"> <RouterLink class="container container_extrait row "  style="text-decoration: none; color: inherit;" :to="{path:'/admin/interview/'+ interview.uuid}"> {{ this.dico_interviews[interview.uuid] ? tags_to_string(this.dico_interviews[interview.uuid]["tags"]) : null }} </RouterLink> </td>
                            
                        </tr>
                    
                </tbody>
            </table>
        
    </div>
</div>

    

</template>


<style scoped>

.scroller {
    width: 300px;
    height: 100px;
    overflow-y: scroll;
    scrollbar-color: var(---blanc) #A6A6A6;
    scrollbar-width: thin;
}

.btgrisv2{
    color:white;
    background-color:var(--gris-moyen);
    padding: 1em;
}

.allmighty {
  position: fixed;        
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); 
  z-index: 9999;          
  padding: 1em 2em;
  border: 1em solid;
  border-color: var(--vert-neon);
  border-radius: 6px;
  cursor: pointer;
}

.ultagger {
    list-style-type: none;

}

.tables{
    width: 100%;
}

.bt{
    color: var(--blanc);
    background-color:var(--vert-pale);
    border-radius: 2em;
    
}

.button-blanc{
    background-color: var(--blanc);
}

.grisee{
  background-color: var(--gris-moyen);
}

.centrer{
justify-content: center
}


.recherche{
    padding-top: 1em;
    padding-bottom: 1em;
}

.pcentrer{
margin-top: 1em;
margin-bottom: 1em;
justify-content: center
}

.tagsfully{
    width: 100%;
    height:100%;
}

.main-trie{
    padding: 2em;
    background-color: var(--gris-moyen);
}

.trie-tags{
    background-color: var(--gris-taupe);
}

ul> li{

    padding-bottom: 1em;

}

.aggrandir{
  display: flex;
  flex-wrap: nowrap;
  list-style-type: none;
  flex-grow: 1;

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


