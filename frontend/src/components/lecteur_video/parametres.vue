<script>
export default {
    props: {
    pos_x_iframe: {
        type: Number,
        required: true
    },
    pos_y_iframe: {
        type: Number,
        required: true
    }
    },

    data() {
        return {
            lecteur: 'YouTube',
            sous_titres: 'Désactivés',
            pos_x : 0,
            pos_y : 0,
        };
    },

    methods: {
        get_pos_x(rect) {
            return this.pos_x_iframe - rect.width - 10;
        },

        get_pos_y(rect) {
            return this.pos_y_iframe - rect.height - 10;
        },  
    },
    mounted() {
        this.$nextTick(() => {
            const rect = this.$refs.popup_parametres.getBoundingClientRect();
            this.pos_x= this.get_pos_x(rect);
            this.pos_y= this.get_pos_y(rect);
        });
    }
};
</script>

<template>
  <!-- popup avec le choix du lecteur et les sous-titres -->
  <div 
    class="popup-parametres"
    ref="popup_parametres"
    :style="{ top: pos_y + 'px', left: pos_x + 'px' }"
  >
    <div class="popup-content">
      <ul class="popup-labels">
        <li>Lecteur vidéo</li>
        <li>Sous-titres</li>
      </ul>
      <ul class="popup-values">
        <li>{{ lecteur }}</li>
        <li>{{ sous_titres }}</li>
      </ul>
    </div>
  </div>
</template>


<style scoped>
.popup-parametres {
  position: absolute; /* flottante */
  background-color: var(--gris-foncer);
  color: var(--third-color);
  border: 2px solid var(--gris-taupe);
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  z-index: 1000; /* au-dessus du lecteur et du reste */
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
