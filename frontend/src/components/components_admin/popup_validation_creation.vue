<script>
import { markRaw } from 'vue';
import Tags from '../../model/tag.js';


import Interview from '../../model/interview.js';

export default {
    name: "comp_admin_edit_popup",
    props: {
        popup2: Boolean

    },
    methods: {
        sendData () {
            this.$emit('ecoutepopup2', !this.popup2)
        },
        
    },
    emits : [ "ecoutepopup2"],   
    
    
    async mounted() {
    this.interviews = markRaw(await Interview.list());
    this.tags = markRaw(await Tags.list())

    try {
        for (let interview of this.interviews) {
            this.dico_interviews[interview.uuid] = {"length": (await interview.extraits).length, "tags": markRaw(await interview.tags)};
            // console.log(markRaw(this.dico_interviews));
        }

    } catch (error) {
        console.error('Erreur lors de la récupération des interviews ou des extraits:', error);
    }
    

    },
    
};




</script>



<template>
<div class="allmightygris" @click="sendData"></div>

<div class="grisee allmighty trie-tagsfoncer row">
    <div class="col collumpopu ">
        
        <div class="container row fullwith" style="max-height: 4em;">
            
        </div>

        <div class="row  trie-tags fullwith">

        </div>
    </div>

    <div class="col collumpopu ">

    </div>
    <div class="col collx">
        <div class="row">
            <button type="button" class="btn-close btn-close-white" aria-label="Close" @click="sendData"></button>
        </div>
    </div>
</div>





</template>

<style scoped>

.scroller {
    width: 300px;
    height: 100vh;
    overflow-y: scroll;
    scrollbar-color: var(---blanc) #A6A6A6;
    scrollbar-width: thin;
}

.tables{
    height: 1em;
    width: 100%;
}

.collumpopu{
    display: flex;
    flex-wrap: wrap;
    flex-grow: 1;
}

.collx{
    flex-grow: 0;
}

.tableheight{
    height: 100%;
}

.fullwith{
    width: 100%;
}

thead{
    height: 10%;
}

.tagsfully {
  width: 100%;
  height: 100%;
  flex-grow: 1;
}


.allmighty {
  display: flex;
  position: fixed;        
  top: 50%;
  left: 50%;
  height: 50%;
  transform: translate(-50%, -50%); 
  z-index: 9999;          
  padding: 1em ;
  border: 1em solid;
  border-color: var(--vert-neon);
  border-radius: 6px;
  width: 80%;
}

.allmightygris{
    position: fixed;        
    top: 0%;
    left: 0%;
    height: 100%;
    width: 100%;
    z-index: 9998;          
    padding: 1em ;
    background-color: rgba(188, 212, 221, 0.521);
    cursor: pointer;
}

.ultagger {
    list-style-type: none;

}


.button-blanc{
    background-color: var(--blanc);
}


.trie-tagsfoncer{
    background-color: var(--gris-moyen);
}


.trie-tags{
    background-color: var(--gris-taupe);
}



.pcentrer {
  margin-top: 1em;
  margin-bottom: 1em;
  justify-content: center;
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