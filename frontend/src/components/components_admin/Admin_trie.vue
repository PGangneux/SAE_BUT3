<script>
import { markRaw } from 'vue';
import Tags from '../../model/tag.js';



export default {
    name: "comp_admin_trie_extrait",
    components: {
    },
    data() {
        return {
            tags: {type:Tags}
        };
    },

    async mounted() {
       this.tags = markRaw(await Tags.list())
    },

};




</script>



<template>

    <div class="main-trie col-md-3 ">

        <div class="row ">
            <button type="button" class="btn button-blanc col"> Ajouter un Extrait <img src="/imgs/add_black.svg" alt="add" class="col "> </button>
        </div>

        <div class="recherche row">
            <div class="search-bar">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                    <button class="btn btn-outline-secondary buttonsearch" type="button" id="search-addon">
                            <img src="/imgs/search.svg" alt="button search" style="margin-right:0;margin-left:0; padding-left: 10px; padding-right: 20px;" > </button>
                </div>
            </div>
        </div>
        
        <div class="row">
            <button class="bt btn col ">Date</button>
            <button class="bt btn col ">Question</button>
            <button class="bt btn col ">Playlist</button>
        </div>

        <div class="row  trie-tags centrer">

            <p class="row pcentrer" >Trier par tag</p>

            <ul class="scroller ultagger row tagsfully">
                <li class="col" v-for="tag in this.tags">
                    <button class="btn btn-primary"> {{ tag.name }} </button>
                </li>
            </ul>


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

.pcentrer{
margin-top: 1em;
margin-bottom: 1em;
justify-content: center
}


.tagsfully{
    width: 100%;
    height: 100%;
    flex-grow: 1;
}


.centrer{
justify-content: center
}

.main-trie{
    padding: 2em;
    background-color: var(--gris-moyen);
}


.ultagger {
    list-style-type: none;

}

.bt{
    color: var(--blanc);
    background-color:var(--vert-pale);
    border-radius: 2em;
    
}


.button-blanc{
    background-color: var(--blanc);
}


.trie-tags{
    background-color: var(--gris-taupe);
}



.recherche{
    padding-top: 1em;
    padding-bottom: 1em;
}

.buttonsearch{
    background-color: var(--vert-pale);
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