<script>
import { computed, watch } from "vue";

export default {
    name: "comp_mindmap",
    inject: ["searchterm"],
    computed: {
        searchValue: {
            get() { return this.searchterm.get(); },
            set(v) { this.searchterm.set(v); }
        }
    },
    watch: {
        searchValue(newVal, oldVal) {
            /// //console.log("mindmap searchterm change");
            /// //console.log("Old:", oldVal);
            /// //console.log("New:", newVal);
        }
    }
};
</script>

<template>
    <div>
        <h2>Mindmap Component</h2>
        <h2>{{ searchValue }}</h2>
        <div class="local"></div>
    </div>
</template>

<style scoped>
.local {
    height: 300px;
}
</style>