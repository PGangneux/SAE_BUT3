<script>
import { computed } from "vue";

export default {
    name: "comp_searchbar",
    inject: ["searchterm"],
    computed: {
        searchValue: {
            get() { return this.searchterm.get(); },
            set(v) { this.searchterm.set(v); }
        }
    }
};
</script>

<template>
    <div class="searchbar">
        <input type="text" v-model="searchValue" placeholder="Search..." />
        <RouterLink to="/">
            <img src="/imgs/Search.png" alt="rechercher">
        </RouterLink>
    </div>
</template>
