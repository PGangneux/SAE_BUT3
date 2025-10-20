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
    title="YouTube video player" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    referrerpolicy="strict-origin-when-cross-origin" 
    allowfullscreen>
  </iframe>
</template>

<style scoped>

iframe {
  flex : 30;
  width: 100%;
  height: 100%;
  border: 3px solid var(--blanc);
  box-sizing: border-box;
  border-radius: 20px;
}



</style>


