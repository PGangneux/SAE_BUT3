<script>
export default {
    name: "page_account",
    data() {
        return {
            pseudo: "JohnDoe",
            nom: "Doe",
            prenom: "John",
            email: "john.doe@example.com",
            newPassword: "",
            confirmPassword: "",
        };
    },
};
</script>

<template>
    <div>
        <div>
            <p>Pseudo</p>
            <input type="text" v-model="pseudo">
        </div>
        <div>
            <p>Nom</p>
            <input type="text" v-model="nom">
        </div>
        <div>
            <p>Prénom</p>
            <input type="text" v-model="prenom">
        </div>
        <div>
            <p>Adresses e-mail</p>
            <input type="text" v-model="email">
        </div>
        <div>
            <p>Nouveau mot de passe</p>
            <input type="password" v-model="newPassword">
        </div>
        <div>
            <p>Confirmer le nouveau mot de passe</p>
            <input type="password" v-model="confirmPassword">
        </div>
    </div>
    <input type="button" value="Annuler">
    <input type="button" value="Enregistrer les modifications">
</template>