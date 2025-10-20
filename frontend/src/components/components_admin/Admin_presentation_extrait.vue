<script>

export default {
    name: "comp_admin_presentation_extrait",
    components: {
    },
};
</script>

<template>
    <div class="container container_extrait col">
        <div class="row base">
            <div class="col-xl vigniette ">
                <h1 class="row decallage_droite">Question Extrait</h1>

                <div class="row text-center clairepart decallage_droite ">
                    <p> description </p>
                </div>

                <div class="row decallage_droite">
                    <ul>

                        <li class="row vigniette">
                            <img src="../../assets/imgs/date.svg" alt="date logo " class="col" height="32" width="32">
                            <p class="col" >date publication</p>
                        </li>

                        <li class="row vigniette">
                            <img src="../../assets/imgs/tags.svg" alt="tags logo " class="col" height="32" width="32">
                            <p class="col">tags</p>
                            <!-- faire get des tags-->
                        </li>


                    </ul>
                </div>
            </div>

            <div class="col-sm reduction_image">
                <img src="../../assets/imgs/width550.png" class="video" alt="Video logo" height="150" width="150">
            </div>

        </div>
    </div>






</template>

<style scoped>

.bt{
    color:white;
    background-color:#26503C;
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
    border: solid 10px;
    border-radius: 2em;
}

.headeradmin{
    
    background-color:#2C2D32;
    margin: 10px 10px 10px 10px; 
}

.reduction_image{
    flex-grow: 0;
    padding: 10px;
    padding-left: 50px;
}

.container_extrait{
    filter: drop-shadow(10px 8px 4px #000000) ;
    background-color:#2C2D32;
    
}

.container_extrait h1, p{
    color: #00FF86;
    
}

.clairepart{
    background-color : #4C4C4C;
}

</style>