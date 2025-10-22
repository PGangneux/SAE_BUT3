<script>

export default {
    name: "comp_admin_trie_extrait",
    components: {
    },
    data() {
        return {
            tags: ['Foo', 'Bar', 'Bsq', 'Bar2']
        };
    }
};




</script>



<template>

    <div class="main-trie col-md-3 ">

        <div class="row ">
            <button type="button" class="btn button-blanc col"> Ajouter un Extrait <img src="/imgs/add.svg" alt="add" class="col "> </button>
            
        </div>

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





</template>

<style scoped>
.scroller {
    width: 300px;
    height: 100px;
    overflow-y: scroll;
    scrollbar-color: var(---blanc) #A6A6A6;
    scrollbar-width: thin;
}



.main-trie{
    padding-top: 10px;
    background-color: var(--gris-moyen);
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