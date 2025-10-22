<script>

import comp_baradmin from "../../components/components_admin/nav_admin.vue";


export default {
  name: "page_admin_edit_client",
  components: {
    comp_baradmin,

  },
};



</script>

<template>
    <comp_baradmin/>

    <h1 class="text-center colorneon"> Éditer un Compte </h1>
    <div class="row">
        <div class="row">

            <div class="input-group mb-3 col">
                <label class="row" for="Pseudo"> Pseudo </label>
                <input type="text" class="form-control" id="Pseudo" name="Pseudo" placeholder="Pseudo" aria-label="Pseudo">
            </div>

            <div class="input-group mb-3 col">
                <label class="row" for="Prénom">Prénom</label>
                <input type="text" class="form-control row" id="Prénom" name="Prénom" placeholder="Prénom" aria-label="Prénom">
            </div>

        </div>

        <div class="row">


            <div class="input-group mb-3 col">
                <label class="row" for="Nom">Nom</label>
                <input type="text" class="form-control row" id="Nom" name="Nom" placeholder="Nom" aria-label="Nom">
            </div>

            <div class="input-group mb-3 col">
                <label class="row" for="Adresse">Adresse</label>
                <div class="row" >
                    <input type="text" class="form-control col" id="Adresse" name="Adresse" placeholder="Adresse e-mail" aria-label="Adresse e-mail">
                    <span class="input-group-text col">@</span>
                    <input type="text" class="form-control col" id="Server" name="Server" placeholder="Server" aria-label="Server">
                </div>
            </div>

        </div>

    </div>

    </template>

<style scoped>

label{
    color: var(--blanc);
}

.colorneon{
  color: var(--vert-neon);
}

</style>
