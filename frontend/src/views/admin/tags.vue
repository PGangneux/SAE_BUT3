<script>
import { markRaw } from 'vue';

export default {
    name: "tags",
    props: {
        video: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            liste_tags: [],
        }
    },
    async mounted() {
        console.log("video", this.video);
        this.liste_tags = markRaw(await this.video.tags());
        console.log("liste tag", this.liste_tags);
    }
};
</script>

<template>
    <div>
        <h1>Tags</h1>

        <div>
            <input type="text" placeholder="Tags..." />
            <button>Créer</button>
        </div>
        <div class="champ_tags">
            <ul>
                <li v-for="tag in liste_tags" :key="tag.uuid">
                    {{ tag.name }}
                </li>
            </ul>
        </div>
    </div>
</template>

<style scoped>

h1 {
    text-align: center;
}

.champ_tags{
    min-height: 30vh;
    background-color: var(--gris-moyen );
}
</style>