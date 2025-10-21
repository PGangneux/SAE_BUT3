<script>

export default {
    name: "comp_admin_edit_popup",
    components: {
    },data() {
        return {
            tags: ['Foo', 'Bar', 'Bsq', 'Bar2'],
            popup: true
        };
    }
    
};




</script>



<template>

    <div class="grisee allmighty row">
        <div class="col-md-3 ">
            <search class="row">
                <form>
                    <div>
                        <input class="col" type="search" id="mySearch" name="q" placeholder="Rechercher" />
                        <button class="col"> <img src="/imgs/search.svg" alt=""> </button>
                    </div>
                </form>
            </search>

            <div class="row  trie-tags">

                <p class="row ">Trier par tag</p>

                <ul class="scroller ultagger row">
                    <li class="col" v-for="tag in tags">
                        <button class="btn btn-primary"> {{ tag }} </button>
                    </li>
                </ul>
            </div>
        </div>

        <div class="col-md-6 ">

                <table class="scroller ultagger table table-bordered">
                    <thead>
                        <tr>
                        <th scope="col">Nom interview</th>
                        <th scope="col">Nb video</th>
                        <th scope="col">Tags</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="col" v-for="tag in tags">
                            <td> {{ tag }} </td>
                            <td> {{ tag }} </td>
                            <td> {{ tag }} </td>
                        </tr>
                    </tbody>
                </table>
            
        </div>
        <div class="col-md-1 ">
            <div class="row">
                <button class="bt btn col" type="button" @click="popup = !popup" ><img src="/imgs/close.png" alt=""></button>
            </div>
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


.button-blanc{
    background-color: var(--blanc);
}




.trie-tags{
    background-color: var(--gris-taupe);
}

</style>