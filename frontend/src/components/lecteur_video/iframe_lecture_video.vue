<script>
export default {
  props: {
    url: {
      type: String,
      required: true
    },
  },
};
</script>


<template>
  <iframe 
    :src="url" 
    title="video player" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    referrerpolicy="strict-origin-when-cross-origin" 
    allowfullscreen>
  </iframe>
</template>

<style scoped>

iframe {
  width: 100%;
  height: 100%;
  border: 3px solid var(--blanc);
  box-sizing: border-box;
  border-radius: 20px;
  background-color: #000; /* change le fond derrière l'iframe */
  flex: 3; /* si tu veux qu'il prenne 3/4 de l'espace flex parent */
}




</style>


