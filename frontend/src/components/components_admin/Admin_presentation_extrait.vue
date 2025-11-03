<script>

import Extrait from '../../model/extrait.js';



export default {
    name: "comp_admin_presentation_extrait",

    props: {
        current_extrait: {
            type: Extrait,
            required: true
        },
    },
    data() {
        return {
            thumbnail: '/imgs/width551.png', // vignette par défaut
        };
    },

    async mounted() {
        this.thumbnail = await this.current_extrait.url_miniature_vi();
    },




};
</script>

<template>
    <RouterLink class="container container_extrait col "  style="text-decoration: none; color: inherit;" to="/admin/details/extrait">
        <div class="row base">
            <div class="col-xl vigniette ">
                <h1 class="row decallage_droite"> {{current_extrait.titre}}</h1>

                <div class="row text-center clairepart decallage_droite ">
                    <p> {{current_extrait.description}} </p>
                </div>

                <div class="row decallage_droite">
                    <ul>

                        <li class="row vigniette">
                            <img src="/imgs/date.svg" alt="date logo" class="col" height="32" width="32">
                            <p class="col" > {{current_extrait.uploaded_at}} </p>
                        </li>

                        <li class="row vigniette">
                            <img src="/imgs/tags.svg" alt="tags logo " class="col" height="32" width="32">
                            <div class="col">
                                <p class="col">tags :</p>
                                 <ul>
                                    <li v-for="tag in current_extrait.tags">
                                        <p class="col">{{ tag }}</p>
                                    </li>
                                </ul>
                            </div>
                            
                            <!-- faire get des tags TODO-->
                        </li>


                    </ul>
                </div>
            </div>
            
            <div class="col-sm reduction_image" v-if="thumbnail != '/imgs/width551.png'" >
                <img :src="thumbnail" class="video" alt="Video logo vimeo" height="150" width="150">
            </div>
            
            <div class="col-sm reduction_image" v-else>
                <img :src=current_extrait.url_miniature_yt class="video" alt="Video logo" height="150" width="150">
            </div>

        </div>
    </RouterLink>






</template>

<style scoped>

.bt{
    color:white;
    background-color:var(--vert-pale);
    border-radius: 19%;
    
}

ul ,base{
  display: flex;
  flex-wrap: nowrap;
  list-style-type: none;
  flex-grow: 1;

}

.vigniette{
    flex-grow: 1;
}

.decallage_droite{
    margin-left: 10px;
}

.container {
     border-radius: 2em;
}

.video{
    border-radius: 2em;
}

.headeradmin{
    
    background-color:var(--gris-moyen);
    margin: 10px 10px 10px 10px; 
}

.reduction_image{
    flex-grow: 0;
    padding: 10px;
    padding-left: 50px;
    align-content: center;
}

.container_extrait{
    filter: drop-shadow(10px 8px 4px var(--noir)) ;
    background-color:var(--gris-moyen);

    
}

.container_extrait h1, p{
    color: var(--vert-neon);
    
}

.clairepart{
    background-color : #4C4C4C;
}

</style>