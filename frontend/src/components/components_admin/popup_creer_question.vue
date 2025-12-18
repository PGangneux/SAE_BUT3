<script>
import { markRaw } from 'vue';
import Tags from '../../model/tag.js';

import Theme from '../../../model/theme.js';
import Question from "../../../model/question";


export default {
    name: "popup_creer_question",
    props: {
        Element_Creer: {
            type:Object,
            required:true
        },
        popupCreerQuestion: {
            type:Boolean,
            required:true
            }

    },data(){
        return {
            typefichier:null,
            listeQuestion:[],   //liste des Questions totals
            listetheme:[],   //liste des Questions totals
        }
    },
    methods: {
        changement_etat_popup () {
            this.$emit('popup_creation_question', !this.popupCreerQuestion)
        },

        async recupetheme(){
            //reccupere la liste des Questions
            this.listetheme =  markRaw(await Theme.list());
        },

        async recupeQuestion(){
            //reccupere la liste des Questions
            this.listeQuestion =  markRaw(await Question.list());
        },


        creerExtrait(e) {
            const value = e.submitter.value

            if(value == "envoyer"){
                alert("nous avons: " + value);
                this.$emit('popup_creation_question', !this.popupCreerQuestion)
            }else{
                this.$emit('popup_creation_question', !this.popupCreerQuestion)
            }
            
        }
        
    },
    emits : [ "popup_creation_question"],   
    
    
    computed: {
        
    },

    async mounted() {
       
    }
};




</script>



<template>
<div class="allmightygris" @click="changement_etat_popup"></div>

<div class="grisee allmighty trie-tagsfoncer row">
    <div class="col collumpopu ">
        <h1> creation d'nouveau artiste </h1>

        <form @submit.prevent="creerExtrait">
            <div class="row"  style="--bs-gutter-x: 0em;">
                <div class=" input-group mb-3" >
                    <span  class="input-group-text colovert" id="basic-addon3" > Question :</span>

                    <input list="Questiondata" id="question" name="question" class="form-control colovert" style="border: solid; border-color: var(--vert-midel);"  v-model="laselectedQuestion" @input="FoncSelectedQuestion"/>

                    <span  class="input-group-text colovert" id="basic-addon3" > Question theme :</span>
                    <input list="Questiontheme" id="question" name="question" class="form-control colovert" style="border: solid; border-color: var(--vert-midel);"  v-model="laselectedQuestion" @input="FoncSelectedQuestion"/>

                    <datalist id="Questiondata">
                    <option v-for="question in listeQuestion" :key="question.id" :value="question.texte" :label="question.texte" > </option> 
                    </datalist>

                    <datalist id="Questiontheme">
                    <option v-for="theme in listetheme" :key="theme.id" :value="theme.theme" :label="theme.name" > </option> 
                    </datalist>


                    <button class="bt" style="background-color: var(--gris-ultraclair);">  <img src="/imgs/add_black.svg" alt="add" class="col "> </button>
                </div>
            </div>
        </form>


    </div>

    <div class="col collx">
        <div class="row">
            <button type="button" class="btn-close btn-close-white" aria-label="Close" @click="changement_etat_popup"></button>
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