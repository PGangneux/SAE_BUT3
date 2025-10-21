<script>
import BASE_URL from "../config.js";
export default {
    name: "comp_recent",
    data() {
        return {
            failed : false,
            loading : true,
            interviews: [],
        };
    },
    async mounted() {
        this.loading = true;
        try {
            const response = await fetch(BASE_URL + "API/interviews/");
            this.interviews = await response.json();
            this.loading = false;
        } catch (error) {
            this.loading = false;
            this.failed = true;
        }
    },
};
</script>

<template>
    <div class="local-flex">
        <div v-if="loading" v-for="i in [1,2,3]" :key="i" class="local">
            <img src="/imgs/spinner.gif" alt="loading image...">
            <p>loading ...</p>
        </div>
        <div v-else-if="failed" v-for="k in [1,2,3]" :key="k" class="local">
            <img src="/imgs/Close.png" alt="erreur image">
            <p>erreur</p>
        </div>
        <div v-else
            v-for="inter in interviews"
            :key="inter.uuid"
            class="local"
        >
            <router-link to="/lecteur_video">
                <p>preview</p>
                <iframe src="https://player.vimeo.com/video/1128762950?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0"></iframe>
                <h3>lieu {{ inter.lieu }}</h3>
                <p>lieu {{ inter.description }}</p>
                <p>url {{inter.extraits}}</p>
            </router-link>
        </div>
    </div>
</template>

<style scoped>
.local-flex {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: space-evenly
}
.local {
    background: var(--gris-moyen);

    border: 3px solid var(--vert-neon);
    box-shadow: 12px 8px 3.2px 6px var(--vert-pale);
    border-radius: 20px;

    padding: 16px;
    min-width: 350px;
    min-height: 350px;
    max-width: 400px;
    flex: 1 1 200px;
}
.local h3 {
    margin: 0 0 8px 0;
}
</style>