<script>
/// import { BASE_URL } from "../config.js";
var BASE_URL = "http://localhost:5000";
export default {
    name: "comp_recent",
    data() {
        return {
            items: [],
        };
    },
    async mounted() {
        try {
            const response = await fetch(BASE_URL + "/api/recent");
            const data = await response.json();
            this.items = data;
        } catch (error) {
            this.items = [];
        }
    },
};
</script>

<template>
    <div class="recent-flex">
        <div
            v-for="item in items"
            :key="item.id"
            class="recent-item"
        >
            <router-link :to="`/video/${item.id}`">
                <p>preview</p>
                <iframe src="${item.url}" frameborder="0"></iframe>
                <h3>{{ item.title }}</h3>
                <p>{{ item.description }}</p>
            </router-link>
        </div>
    </div>
</template>

<style scoped>
.recent-flex {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
}
.recent-item {
    background: #fff;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    border-radius: 8px;
    padding: 16px;
    min-width: 200px;
    max-width: 300px;
    flex: 1 1 200px;
}
.recent-item h3 {
    margin: 0 0 8px 0;
}
</style>