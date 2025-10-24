<script>
import { videoStore } from "../../model/videoStore";

export default {
  props: {
    pos_x: Number,
    pos_y: Number,
  },
  data() {
    return {
      lecteurs: ["YouTube", "Viméo"],
      lecteur_selected: videoStore.lecteur
    }
  },

  methods : {
    set_lecteur(lecteur){
      this.$emit('set_lecteur', lecteur),
      this.lecteur_selected = videoStore.lecteur
    }
  }
}
</script>

<template>
  <div 
    class="popup-parametres"
    :style="{ top: pos_y + 'px', left: pos_x + 'px' }"
  >
    <ul class="popup-labels">
      <li v-for="lecteur in lecteurs" :key="lecteur" @click="set_lecteur(lecteur)">
        {{ lecteur }}
        <span v-if="lecteur === lecteur_selected">✅</span>
      </li>
    </ul>
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
  width: auto;
  height: auto;
}

.popup-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.popup-labels {
  list-style: none;
  padding: 0;
  margin: 0;
}

.popup-labels li {
  margin-bottom: 0.5rem;
}
</style>
