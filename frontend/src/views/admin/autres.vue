<script>
export default {
    name: "page_autres",
};
</script>

<template>
    <h1 class="vert-neon">À propos de nous</h1>

    <div class="row">
        <h2 class="vert-neon">Questions</h2>
        <p>nb Questions</p>
        <p>nb Questions utiliser</p>
        <p>nb Questions non utiliser</p>
    </div>

    <div class="row">
        <h2 class="vert-neon">Tags</h2>
        <p>nb Tags</p>
        <p>nb Tags utiliser</p>
        <p>nb Tags non utiliser</p>
    </div>

    <div class="row">
        <h2 class="vert-neon">Artistes</h2>
        <p>nb Artistes</p>
        <p>nb Artistes utiliser</p>
        <p>nb Artistes non utiliser</p>
    </div>

</template>

<style scoped>
.vert-neon { 
    color : var(--vert-neon);
    justify-self: center;
}
.local-flex {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;
    flex: 1 1 200px;
}
.spacy {
    border-radius: 20px;    
    width: 500px;
    height: 500px;
    background-color: var(--gris-moyen);
}
.logo{
    max-width: 100px;
}
</style>