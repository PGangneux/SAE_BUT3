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
           
            <div class="container row">
                <div class="search-bar">
                    <div class="input-group">
                        <input type="text" class="form-control" placeholder="Search..." aria-label="Search" aria-describedby="search-addon">
                        <button class="btn btn-outline-secondary" type="button" id="search-addon">
                                <img src="/imgs/search.svg" alt="button search">
                            </button>
                    </div>
                </div>
            </div>


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