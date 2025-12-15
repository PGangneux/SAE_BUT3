<script>
import { mm_LegendClassMap } from '../../model/mindmap/mm_const.js';
import mm_Mindmap from '../../model/mindmap/mm_mindmap.js';
import mindmap_node from './mindmap_node.vue';

export default {
    name: "comp_mindmap",
    inject: ["searchterm","interview_current","extrait_current"],
    components: {
        mindmap_node
    },
    data() {
        let inter = this.interview_current;
        let ext = this.extrait_current;        
        return {
            mm_LegendClassMap: mm_LegendClassMap,
            jsclass : new mm_Mindmap(this, inter, ext),
            searchval : "",
        };
    },
    async mounted() {
        this.searchval = this.searchterm.get();
        this.jsclass.searchval = this.searchval;
        this.jsclass.draw_root();
    },
    computed: {
        searchValue: {
            get() { return this.searchterm.get(); },
        }
    },
    watch: {
        searchValue(newVal) {
            this.searchval = newVal;
            this.jsclass.searchval = this.searchval;
            this.jsclass.redraw_root();
        }
    },
};
</script>

<template>
    <div class="mm_main_relative" 
        @mousedown="jsclass.startDrag" @mouseup="jsclass.stopDrag"
        @mousemove="jsclass.doDrag" @mouseleave="jsclass.stopDrag"
        @wheel="jsclass.handleWheel"
        @touchstart="jsclass.startDragTouch" @touchend="jsclass.stopDrag"
        @touchmove="jsclass.doDragTouch"
        >
        <button class="mm_fullscreenbtn" @click="jsclass.toggleFullscreen" @touchend="jsclass.toggleFullscreen">
            <img :src="jsclass.fullscreen ? '/imgs/reduire.svg' : '/imgs/agrandir.svg'" 
                :alt="jsclass.fullscreen ? 'Exit fullscreen' : 'Enter fullscreen'" 
                class="fullscreen-icon">
        </button>
        <div class="mm_control_outer">
            <div class="mm_controls">
                <button @click="jsclass.zoomin()" @touchend="jsclass.zoomin()">+</button>
                <button @click="jsclass.zoomout()" @touchend="jsclass.zoomout()">-</button>
                <button @click="jsclass.zoomreset()" @touchend="jsclass.zoomreset()">reset zoom</button>
                <button @click="jsclass.centerOnNode(jsclass.nodes[0])" @touchend="jsclass.centerOnNode(jsclass.nodes[0])">recenter</button>
                <button @click="jsclass.draw_root()" @touchend="jsclass.redraw_root()">redraw</button>
            </div>
            <div class="mm_legend_outer">
                <button v-if="jsclass.togglelegend" @click="jsclass.togglelegend = false" @touchend="jsclass.togglelegend = false;">></button>
                <button v-else @click="jsclass.togglelegend = true" @touchend="jsclass.togglelegend = true;"><</button>
                <transition name="mm_legend_anim">
                    <div class="mm_legend" v-if="jsclass.togglelegend">
                        <div v-for="(nameproper, nameclass) in mm_LegendClassMap">
                            <div class="mm_legend_cercle"
                                :class="`mmLegendColorMap${nameclass}`"></div>
                            <p>{{ nameproper }}</p>
                        </div>
                    </div>
                </transition>
            </div>
        </div>
        <div v-for="link in jsclass.linkages" :key="link.id" :style="link.getStyle(jsclass.scale, jsclass.offx, jsclass.offy)" class="mm_linkage">
        </div>
        <mindmap_node v-for="node in jsclass.nodes" :jsclass="node" :jsmm="jsclass"
            @click="jsclass.handleClick(node);" @touchend="jsclass.handleClick(node);" />
    </div>
</template>