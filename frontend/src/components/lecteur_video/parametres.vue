<script>
import { videoStore } from '../../model/videoStore';
import parametres_lecteur from './parametres_lecteur.vue';


export default {
    components : {parametres_lecteur},
    props: {
        pos_x_iframe: {
            type: Number,
            required: true
        },
        pos_y_iframe: {
            type: Number,
            required: true
        },
        lecteur : {
            type: String,
            required: true
        }
    },

    data() {
        return {
            parametre_general: true,
            parametre_lecteur: false,
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

        toggle_parametre_lecteur() {
            this.parametre_general = false;
            this.parametre_lecteur = true;
        },

    },
    mounted() {
        //console.log("videoStore dans param")
        //console.log(JSON.parse(JSON.stringify(videoStore)))
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
    v-if="parametre_general"
    class="popup-parametres"
    ref="popup_parametres"
    :style="{ top: pos_y + 'px', left: pos_x + 'px' }"
  >
    <div class="popup-content">
      <ul class="popup-labels">
        <li @click="toggle_parametre_lecteur">Lecteur vidéo</li>
      </ul>
      <ul class="popup-values">
        <li @click="toggle_parametre_lecteur">{{ lecteur }} > </li>
      </ul>
    </div>
  </div>

  <parametres_lecteur 
    v-if="parametre_lecteur"
    :pos_x="pos_x"
    :pos_y="pos_y" 
    @set_lecteur="this.$emit('set_lecteur', $event)"
  />



  

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
