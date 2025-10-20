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

    <div class="bg-danger col ">

        <div class="row text-center">
            <button type="button" class="btn btn-primary col"> Ajouter un Extrait</button>
            <img src="../../assets/imgs/add.svg" alt="add" class="col add">
        </div>

        <search class="row">
            <form>
                <div class="text-center">
                    <input class="col" type="search" id="mySearch" name="q" placeholder="Rechercher" />
                    <button class="col"> <img src="../../assets/imgs/search.svg" alt=""> </button>
                </div>
            </form>
        </search>

        <div class="row text-center">

            <p class="row text-center">Trier par tag</p>

            <ul class="scroller ultagger">
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
    scrollbar-color: #FFFFFF #A6A6A6;
    scrollbar-width: thin;
}

.add {
    size: 10px;
    height: 10px;
    width: 10px;
}




.ultagger {
    list-style-type: none;

}
</style>