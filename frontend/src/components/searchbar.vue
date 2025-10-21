<script>
export default {
    name: "comp_searchbar",
    inject : ["searchterm"],
};
</script>

<template>
    <div>
        <input type="text" v-model="searchterm" placeholder="Search..." />
    </div>
    <RouterLink to="/">
        <img src="/imgs/Search.png" alt="rechercher">
    </RouterLink>
    <img src="" alt="">
</template>