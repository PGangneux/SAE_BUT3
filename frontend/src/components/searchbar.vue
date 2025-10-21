<script>
export default {
    name: "comp_searchbar",
    data() {
        var tags = ["pop"];
        return {
            tags: tags,
        };
    },
    emits: [
        "search",
    ],
};
</script>

<template>
    <div>
        <input type="text" placeholder="Search..." />
    </div>
    <button @click="$emit('search')"></button>
    <img src="" alt="">

</template>