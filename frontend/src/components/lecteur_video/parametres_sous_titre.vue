<script>
export default {
  props: {
    pos_x: {
      type: Number,
      required: true
    },
    pos_y: {
      type: Number,
      required: true
    },
    lecteur_selected: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      lecteurs: ["Youtube", "Viméo"],
    }
  },
};
</script>

<template>
  <div 
    class="popup-parametres"
    :style="{ top: pos_y + 'px', left: pos_x + 'px' }"
  >
    <div class="popup-content">
      <ul class="popup-labels">
        <li v-for="lecteur in lecteurs" :key="lecteur">
          {{ lecteur }}
          <span v-if="lecteur === lecteur_selected">✅</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.popup-parametres {
  position: absolute;
  background-color: var(--gris-foncer);
  color: var(--third-color);
  border: 2px solid var(--gris-taupe);
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  min-width: 200px;
}

.popup-content {
  display: flex;
  justify-content: space-between;
}

.popup-labels,
.popup-values {
  list-style: none;
  padding: 0;
  margin: 0;
}

.popup-labels li,
.popup-values li {
  margin-bottom: 0.5rem;
}
</style>
