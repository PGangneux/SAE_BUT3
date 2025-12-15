<script>
export default {
    name: "components_supprimer",
    props: {
        Element_Supp: {
            type: Object,
            required: true
        }
    },
    methods: {
        async deleteElement() {
            await this.Element_Supp.delete();
            this.$router.push("/admin/interview");
        }
    },
    emits : ["closePopup"],
};
</script>

<template>
    <div class="overlay">
        <div class="popup">
            <h1> Voulez vous vraiment supprimer {{ this.Element_Supp.titre }} </h1>
            <button @click="$emit('closePopup')" class="col bt button-blanc"> Annuler </button>
            <button @click="deleteElement()" class="col bt button-blanc">Valider</button>
        </div>
    </div>
</template>

<style scoped>
.button-blanc {
    background-color: var(--blanc);
}
</style>
