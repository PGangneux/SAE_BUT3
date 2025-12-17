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
            mminst : new mm_Mindmap(this, inter, ext),
            searchval : "",
        };
    },
    async mounted() {
        this.searchval = this.searchterm.get();
        this.mminst.searchval = this.searchval;
        this.mminst.draw_root();
    },
    computed: {
        searchValue: {
            get() { return this.searchterm.get(); },
        }
    },
    watch: {
        searchValue(newVal) {
            this.searchval = newVal;
            this.mminst.searchval = this.searchval;
            this.mminst.redraw_root();
        }
    },
};
</script>

<template>
    <div class="mm_main_relative" 
        @mousedown="mminst.startDrag" @mouseup="mminst.stopDrag"
        @mousemove="mminst.doDrag" @mouseleave="mminst.stopDrag"
        @wheel="mminst.handleWheel"
        @touchstart="mminst.startDragTouch" @touchend="mminst.stopDrag"
        @touchmove="mminst.doDragTouch"
        >
        <button class="mm_fullscreenbtn" @click="mminst.toggleFullscreen" @touchend="mminst.toggleFullscreen">
            <img :src="mminst.fullscreen ? '/imgs/reduire.svg' : '/imgs/agrandir.svg'" 
                :alt="mminst.fullscreen ? 'Exit fullscreen' : 'Enter fullscreen'" 
                class="fullscreen-icon">
        </button>
        <div class="mm_control_outer">
            <div class="mm_controls">
                <button @click="mminst.zoomin()" @touchend="mminst.zoomin()">+</button>
                <button @click="mminst.zoomout()" @touchend="mminst.zoomout()">-</button>
                <button @click="mminst.zoomreset()" @touchend="mminst.zoomreset()">reset zoom</button>
                <button @click="mminst.centerOnNode(mminst.nodes[0])" @touchend="mminst.centerOnNode(mminst.nodes[0])">recenter</button>
                <button @click="mminst.draw_root()" @touchend="mminst.redraw_root()">redraw</button>
            </div>
            <div class="mm_legend_outer">
                <button v-if="mminst.togglelegend" @click="mminst.togglelegend = false" @touchend="mminst.togglelegend = false;">></button>
                <button v-else @click="mminst.togglelegend = true" @touchend="mminst.togglelegend = true;"><</button>
                <transition name="mm_legend_anim">
                    <div class="mm_legend" v-if="mminst.togglelegend">
                        <div v-for="(nameproper, nameclass) in mm_LegendClassMap">
                            <div class="mm_legend_cercle"
                                :class="`mmLegendColorMap${nameclass}`"></div>
                            <p>{{ nameproper }}</p>
                        </div>
                    </div>
                </transition>
            </div>
        </div>
        <div v-for="link in mminst.linkages" :key="link.id" :style="link.getStyle(mminst.scale, mminst.offx, mminst.offy)" class="mm_linkage">
        </div>
        <mindmap_node v-for="node in mminst.nodes" :jsclass="node"
            @click="mminst.handleClick(node);" @touchend="mminst.handleClick(node);" />
    </div>
</template>