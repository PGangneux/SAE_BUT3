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
            <button type="button" class="btn button-blanc col"> Ajouter un Extrait</button>
            <img src="/imgs/add.svg" alt="add" class="col add">
        </div>

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





</template>

<style scoped>
.scroller {
    width: 300px;
    height: 100px;
    overflow-y: scroll;
    scrollbar-color: var(---blanc) #A6A6A6;
    scrollbar-width: thin;
}

.add {
    size: 10px;
    height: 10px;
    width: 10px;
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
</style>