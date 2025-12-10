<script>
import { markRaw } from 'vue';
import comp_baradmin from "../../../components/components_admin/nav_admin.vue";
import comp_petit_extrait from '../../../components/components_admin/Admin_presentation_petit_extrait.vue';

import Interview from '../../../model/interview.js';
import Extrait from "../../../model/extrait.js";

export default {
    name: "page_admin_edit_interview",
    components: {
      comp_baradmin,
      comp_petit_extrait,
    },
    data() {
        return {
            Extraitlist : [],
            current_interview:{type:Interview},
            current_list_extraits:{type:Extrait},
            taillelist1:0,   
            taillelist2:0, 
        };
    },
    computed: {
        description: {
            get() {
                return this.current_interview?.description ? this.current_interview.description : 'Chargement...';
            },
            set(value) {
                if (this.current_interview) {
                    this.current_interview.description = value;
                }
            }
        },
    },
    methods : {
        startDrag(evt, item) {
            // Empêche l'image / le lien d'être la "drag image"
            const crt = evt.currentTarget; // la div.drag-wrapper

            // Crée une copie invisible de la carte à utiliser comme drag image
            const clone = crt.cloneNode(true);
            clone.style.position = 'absolute';
            clone.style.top = '-9999px';
            clone.style.left = '-9999px';
            document.body.appendChild(clone);

            evt.dataTransfer.setDragImage(clone, 0, 0);

            // Remove after a short delay (Chrome needs async)
            setTimeout(() => document.body.removeChild(clone), 0);

            evt.dataTransfer.dropEffect = 'move';
            evt.dataTransfer.effectAllowed = 'move';
            evt.dataTransfer.setData('itemID', item.uuid);
        },

        
        onDragOver(evt) {
            evt.preventDefault();
        },
        
        onDrop(evt, targetList) {
            console.log("drop")
            evt.preventDefault();
            const itemID = evt.dataTransfer.getData('itemID');
            
            if (targetList === 'playlist') {
                // Déplacer de Extraitlist vers current_list_extraits
                const itemIndex = this.Extraitlist.findIndex(item => item.uuid === itemID);
                if (itemIndex !== -1) {
                    const item = this.Extraitlist.splice(itemIndex, 1)[0];
                    this.current_list_extraits.push(item);
                    this.taillelist1 = this.Extraitlist.length;
                    this.taillelist2 = this.current_list_extraits.length;
                }
            } else if (targetList === 'available') {
                // Déplacer de current_list_extraits vers Extraitlist
                const itemIndex = this.current_list_extraits.findIndex(item => item.uuid === itemID);
                if (itemIndex !== -1) {
                    const item = this.current_list_extraits.splice(itemIndex, 1)[0];
                    this.Extraitlist.push(item);
                    this.taillelist1 = this.Extraitlist.length;
                    this.taillelist2 = this.current_list_extraits.length;
                }
            }
        },
    },

    async mounted() {
        const InterviewId = this.$route.params.id;
        this.current_interview = markRaw(await Interview.detail(InterviewId));
        this.current_list_extraits = markRaw(await this.current_interview.extraits());
        
        const allExtraits = markRaw(await Extrait.list());
        this.Extraitlist = markRaw(
            allExtraits.filter(e => 
                !this.current_list_extraits.some(c => c.uuid === e.uuid)
            )
        );

        this.taillelist1 = this.Extraitlist.length;
        this.taillelist2 = this.current_list_extraits.length;
    },
};
</script>

<template>
<comp_baradmin/>

<h1 class="text-center"> Edit Interview-Playlist </h1>

<div class="row" style=" margin-left: 0 !important; margin-right: 0 !important;">
    <h1> {{ this.current_interview.titre }} - Playlist </h1>

    <div class="row"  style=" margin-left: 0 !important; margin-right: 0 !important;">
        <div class="form-group">
            <textarea type="aera" placeholder="Description" style="background-color: var(--gris-ultraclair); border:solid 0.3em;  border-color: var(--vert-pale);" v-model="description" class="form-control"></textarea>
        </div>
    </div>
</div>

<div class="row" style=" margin-left: 0 !important; margin-right: 0 !important;" >
    <div class="col-md-4 aggrandir" style="background-color:var(--vert-midel); margin: 1%;">
        <div class="container row pcentrer " style=" margin-left: 0 !important; margin-right: 0 !important;">

            <div class="row" style=" margin-left: 0 !important; margin-right: 0 !important;">
                <h1> Question-Extrait existant</h1>
                <h1> Total Question-Extrait : {{this.taillelist1}}</h1>
            </div>

            <div class="search-bar grisee">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                    <button class="btn btn-outline-secondary" type="button" id="search-addon">
                        <img src="/imgs/search.svg" alt="button search">
                    </button>
                </div>
            </div>

            <ul 
                class="drop-zone"
                @drop="onDrop($event, 'available')"
                @dragover="onDragOver($event)"
            >
                <li  v-for="extraitv1 in this.Extraitlist"  :key="extraitv1.uuid" class="drag-el" >
                    <div
                        class="drag-wrapper"
                        draggable="true"
                        @dragstart="startDrag($event, extraitv1)"
                    >
                        <comp_petit_extrait :current_extrait=extraitv1 />
                    </div>
                </li>
            </ul>
        </div>
    </div>

    <div class="col-md-4 aggrandir" style="background-color:var(--vert-pale); margin: 1%;">
        <div class="container row pcentrer " style=" margin-left: 0 !important; margin-right: 0 !important;">

            <div class="row" style=" margin-left: 0 !important; margin-right: 0 !important;">
                <h1> Question-Extrait dans Playlist</h1>
                <h1> Total Question-Extrait : {{ this.taillelist2 }}</h1>
            </div>

            <div class="search-bar grisee">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                    <button class="btn btn-outline-secondary" type="button" id="search-addon">
                        <img src="/imgs/search.svg" alt="button search">
                    </button>
                </div>
            </div>

            <ul 
                class="drop-zone"
                @drop="onDrop($event, 'playlist')"
                @dragover="onDragOver($event)"
            >
                <li 
                    v-for="extraitv2 in this.current_list_extraits"
                    :key="extraitv2.uuid"
                    class="drag-el" 
                >
                    <div
                        class="drag-wrapper"
                        draggable="true"
                        @dragstart="startDrag($event, extraitv2)"
                    >
                        <comp_petit_extrait :current_extrait=extraitv2 />
                    </div>
                </li>
            </ul>
        </div>
    </div>
</div>

<div class="row pad"  style=" margin-left: 0 !important; margin-right: 0 !important;">
    <RouterLink to="/admin/extrait/creer/" class="btn button-blanc col"> Ajouter un Extrait <img src="/imgs/add_black.svg" alt="add" class="col "> </RouterLink>          
    <RouterLink to="/admin/interview/creer/" type="button" class="btn button-blanc col"> Ajouter un Playlist <img src="/imgs/add_black.svg" alt="add" class="col "> </RouterLink>
    <button type="submit" class="bt btn col" > <img src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>
    <button type="button" class="btred btn col" > <img src="/imgs/delete.svg" alt="Supprimer"> Supprimer </button>
</div>
</template>

<style scoped>
.pad{
  padding-top: 1em;
  padding-bottom: 1em;
}

.carte{
  padding: 5px;
  padding-bottom: 1em;
}

.btred{
    color: var(--blanc);
    background-color:var(--rouge);
    border-radius: 2em;
}



.pcentrer{
  margin-top: 1em;
  justify-content: center
}

.button-blanc{
    background-color: var(--blanc);
}

.bt{
    color:white;
    background-color:var(--vert-pale);
    border-radius: 2em;
}


ul {
  list-style-type: none;
  justify-content: space-between;
}

.scroller2 {
  height: 70vh;
  overflow-y: scroll;
  scrollbar-color: var(---blanc) #A6A6A6;
  scrollbar-width: thin;
}

.aggrandir{
  list-style-type: none;
  flex-grow: 1;
}

.grisee{
  background-color: var(--gris-moyen);
}

.drop-zone {
  background-color: #eee;
  margin-bottom: 10px;
  padding: 10px;
}

.drag-el {
  background-color: #fff;
  margin-bottom: 10px;
  padding: 5px;
  cursor: move;
}

.drag-el * {
    user-select: none
}


li {
  display: block;
}

li[draggable="true"] {
  transform: translateZ(0); /* hack Chrome */
}

.drag-wrapper {
    cursor: grab;
}
.drag-wrapper:active {
    cursor: grabbing;
}
</style>