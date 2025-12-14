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
        /**
         * Démarre le drag d’un élément
         * configure les métadonnées (UUID + liste source) et initialise l’effet de déplacement.
         *
         * @param {DragEvent} evt - L’événement de dragstart.
         * @param {Object} item - L’élément extrait en cours de déplacement.
         * @param {string} sourceList - La liste d’origine ("available" ou "playlist").
         */
        startDrag(evt, item, sourceList) {
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
            evt.dataTransfer.setData('sourceList', sourceList); // 'available' ou 'playlist'
            
        },

        /**
         * Autorise le drop en empêchant le comportement par défaut du navigateur.
         *
         * @param {DragEvent} evt - L’événement de dragover.
         */
        onDragOver(evt) {
            evt.preventDefault();
        },
        
        /**
         * Gère le drop d’un élément : récupère l’UUID, détermine la liste source/target,
         * déplace l’élément, calcule la position d’insertion dans la playlist si nécessaire,
         * et met à jour les compteurs ainsi que le rendu Vue.
         *
         * @param {DragEvent} evt - L’événement de drop.
         * @param {string} targetList - La liste cible ("available" ou "playlist").
         */
        onDrop(evt, targetList) {
            evt.preventDefault();

            const itemID = evt.dataTransfer.getData('itemID');       // UUID de l’élément drag
            const sourceList = evt.dataTransfer.getData('sourceList'); // 'available' ou 'playlist'

            let sourceArray = sourceList === 'playlist' ? this.current_list_extraits : this.Extraitlist;
            let targetArray = targetList === 'playlist' ? this.current_list_extraits : this.Extraitlist;

            // Trouver l’élément dans la liste source
            const itemIndex = sourceArray.findIndex(item => item.uuid === itemID);
            if (itemIndex === -1) return;

            const item = sourceArray.splice(itemIndex, 1)[0]; // supprime de la source

            if (targetList === 'playlist') {

                const targetItems = Array.from(evt.currentTarget.children);

                // Calcul de l'index d'insertion
                const dropY = evt.clientY;
                let insertIndex = targetArray.length; // par défaut fin
                for (let i = 0; i < targetItems.length; i++) {
                    const rect = targetItems[i].getBoundingClientRect();
                    if (dropY < rect.top + rect.height / 2) {
                        insertIndex = i;
                        break;
                    }
                }

                // Insérer à la bonne position
                targetArray.splice(insertIndex, 0, item);

                // force vue à redessiner la liste playlist, sinon affichage non mis à jour car on change l'intérieurs de la liste et pas de changement de taille ...
                if (targetList === sourceList){
                    // TRIGGER VUE RENDER 
                    // Forcer rerender sans proxifier les objets
                    this.current_list_extraits = this.current_list_extraits.map(e => markRaw(e));
                    this.Extraitlist = this.Extraitlist.map(e => markRaw(e));
                }

            } else if (targetList === 'available') {
                // ----------------------
                // Déplacer vers le début de la liste disponible
                // ----------------------
                targetArray.splice(0, 0, item);
            }

            // Mettre à jour les compteurs
            this.taillelist1 = this.Extraitlist.length;
            this.taillelist2 = this.current_list_extraits.length;
        },

        async save(){
            //BaptisteBD
            console.log("save")
            await this.current_interview.setExtraits(this.current_list_extraits)
        }

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

<div class="main_content">
    <h1 class="text-center"> Modification d'une Playlist </h1>
    <h2> {{ this.current_interview.titre }}</h2>

    <textarea type="aera" placeholder="Description" v-model="description" class="form-control"></textarea>

    <div class="row row_gap">
        <div class="col-md-4 aggrandir div_extrait_dispo">
            <div class="pcentrer ">

                <div class="row">
                    <h1> Disponible </h1>
                    <h2> Total Extraits : {{this.taillelist1}}</h2>
                </div>

                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                    <button class="btn btn-outline-secondary" type="button" id="search-addon">
                        <img src="/imgs/search.svg" alt="button search">
                    </button>
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
                            @dragstart="startDrag($event, extraitv1, 'available')"
                        >
                            <comp_petit_extrait :current_extrait=extraitv1 />
                        </div>
                    </li>
                </ul>
            </div>
        </div>

        <div class="col-md-4 aggrandir div_extrait_playlist">
            <div class="pcentrer ">

                <div class="row">
                    <h1> Playlist</h1>
                    <h2> Total Extraits : {{ this.taillelist2 }}</h2>
                </div>

                    <div class="input-group">
                        <input type="text" class="form-control" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                        <button class="btn btn-outline-secondary" type="button" id="search-addon">
                            <img src="/imgs/search.svg" alt="button search">
                        </button>
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
                            @dragstart="startDrag($event, extraitv2, 'playlist')"
                        >
                            <comp_petit_extrait :current_extrait=extraitv2 />
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <div class="bottom_button">
        <RouterLink to="/admin/extrait/creer/" class="btn btn-outline-light"> <img src="/imgs/add.svg" alt="add"> Ajouter un Extrait</RouterLink>          
        <RouterLink to="/admin/interview/creer/" type="button" class="btn btn-outline-light"> <img src="/imgs/add.svg" alt="add">  Ajouter une Playlist </RouterLink>
        <button @click="save()" type="submit" class="btn btn-outline-success" > <img src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>
        <button type="button" class="btn  btn-outline-danger" > <img src="/imgs/delete.svg" alt="Supprimer"> Supprimer </button>
    </div>
</div>
</template>

<style scoped>
/* marge globale pour le contenu */
.main_content {
    margin: 2%;
}

/* conteneur des deux colonnes */
.row_gap {
    display: flex;
    flex-wrap: nowrap;           /* interdit le retour à la ligne */
    gap: 20px;                   /* espace entre les colonnes */
    margin: 2% 0% 2% 0%  ;        /* marge pour ne pas coller aux bords */
    align-items: stretch;        /* les colonnes ont la même hauteur */
}

/* colonnes */
.aggrandir {
    display: flex;
    flex-direction: column;
    flex: 1 1 0;                 /* peut grandir mais pas rétrécir en dessous */
    min-width: 300px;             /* largeur minimale pour ne pas rétrécir */
    height: auto;                 /* hauteur basée sur la colonne la plus grande */
    border-radius: 5px;   /* arrondit les bords */
    overflow: hidden;      /* optionnel : évite que le contenu dépasse */
}

/* wrapper vertical qui contient header / search / liste */
.pcentrer {
    display: flex;
    flex-direction: column;
    height: 100%;                 /* occupe toute la hauteur de la colonne */
}

/* empêcher header et search de grandir */
.pcentrer > *:not(.drop-zone) {
    flex: 0 0 auto;
}

/* UL prend sa hauteur naturelle et ne scroll plus */
.drop-zone {
    flex: 1 1 auto;               /* occupe tout l'espace restant de la colonne */
    overflow: visible;            /* plus de scroll interne */
    padding: 10px;
    list-style: none;
    margin: 0;
}

/* reset ul default spacing */
.drop-zone { padding-left: 0; }

/* si tu veux que les li s'empilent verticalement */
.drop-zone .drag-el {
    display: block;
    margin-bottom: 8px;
    padding: 8px;
    cursor: move;
}

/* éviter que les enfants forcent la taille */
.pcentrer * {
    box-sizing: border-box;
}

/* drag wrapper visuel */
.drag-wrapper { cursor: grab; }
.drag-wrapper:active { cursor: grabbing; }

/* garde esthétique pour header et search */
.aggrandir .header-zone { padding-bottom: 8px; }

/* outlines pour debugger (enlever en production) */
.aggrandir { outline: 1px dashed rgba(0,0,0,0.05); }
.drop-zone { outline: 1px dashed rgba(0,0,0,0.05); }



/* couleurs ul */
.div_extrait_dispo{
    background-color:var(--vert-midel);
}

.div_extrait_playlist{
    background-color:var(--vert-pale);
}

textarea{
    border:solid 0.3em;  
    border-color: var(--vert-pale);
}

h1 {
    text-align: center;
}

.aggrandir h1{
    margin-top: 2%; ;
}


</style>
