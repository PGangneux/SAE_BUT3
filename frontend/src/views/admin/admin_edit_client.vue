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
    <form action="">
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
                        <input type="text" class="form-control row " id="Adresse" name="Adresse" placeholder="Adresse e-mail" aria-label="Adresse e-mail">
                </div>

            </div>
        </div>
        <div class="row">

            <button  type="button"   class=" btn btred col" > <img src="/imgs/delete.svg" alt="Supprimer"> Supprimer </button>
            <button  type="submit"   class="bt btn col" > <img src="/imgs/save.svg" alt="Enregistrer"> Enregistrer </button>
            <button  type="reset"  class="bt btn col" > <img src="/imgs/cancel.svg" alt="Annuler"> Annuler </button>
        </div>
    </form>

    
    </template>

<style scoped>

.bt{
    color: var(--blanc);
    background-color:var(--vert-pale);
    border-radius: 2em;
    
}

.btred{
    color: var(--blanc);
    background-color:var(--rouge);
    border-radius: 2em;
    
}



label{
    color: var(--blanc);
}

.colorneon{
  color: var(--vert-neon);
}

</style>
