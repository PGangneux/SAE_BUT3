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


