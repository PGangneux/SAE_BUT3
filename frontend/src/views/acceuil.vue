<script>
import comp_mindmap from "../components/mindmap.vue";
import comp_recent from "../components/home_recent.vue";
export default {
    name: "page_accueil",
    components: {
        comp_mindmap,
        comp_recent,
    },
};
</script>

<template>
    <h1>Accueil rec 117</h1>
    <comp_recent />
    <comp_mindmap />
</template>