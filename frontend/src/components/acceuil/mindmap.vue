<script>
// import { markRaw } from 'vue';
import { mmdraw_root , mmdraw_update } from '../../model/mindmap/mindmap_func.js';
import { mmLegendClassMap , mmInfo } from '../../model/mindmap/mindmap_base.js';
import mindmap_node from './mindmap_node.vue';

export default {
    name: "comp_mindmap",
    inject: ["searchterm","mindmap_chemin","interview_current","extrait_current"],
    components: {
        mindmap_node
    },
    data() {
        let inter = this.interview_current;
        let ext = this.extrait_current;
        console.log(inter,ext);
        
        return {
            mmLegendClassMap: mmLegendClassMap,
            mminfo : new mmInfo(inter,ext),
            searchval : "",
        };
    },
    mounted() {
        this.centerMindmap();
        this.searchval = this.searchterm.get();
        this.mminfo.searchval = this.searchval;
        mmdraw_root(this.mminfo);
    },
    computed: {
        searchValue: {
            get() { return this.searchterm.get(); },
        }
    },
    watch: {
        searchValue(newVal) {
            // console.log("Search term changed:", newVal);
            this.centerMindmap();
            this.searchval = newVal;
            this.mminfo.searchval = this.searchval;
            mmdraw_root(this.mminfo);
        }
    },
    methods: {
        toggleFullscreen() {
            this.mminfo.fullscreen = !this.mminfo.fullscreen;
            const element = this.$el;
            if (this.mminfo.fullscreen) {
                if (element.requestFullscreen) {
                    element.requestFullscreen();
                }
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                }
            }
        },
        centerMindmap() {
            const container = this.$el;
            if (container) {
                this.mminfo.offx = container.clientWidth / 2;
                this.mminfo.offy = container.clientHeight / 2;
            }
        },
        centerOnNode(node) {
            const container = this.$el;
            if (container) {
                // Calculate target position to center the node
                const targetOffx = container.clientWidth / 2 - node.x * this.mminfo.scale;
                const targetOffy = container.clientHeight / 2 - node.y * this.mminfo.scale;

                // Animate over 1 second (1000ms)
                this.animateToPosition(targetOffx, targetOffy, 1000);
            }
        },
        animateToPosition(targetOffx, targetOffy, duration) {
            const startOffx = this.mminfo.offx;
            const startOffy = this.mminfo.offy;
            const startTime = performance.now();
            
            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // Easing function for smooth animation
                const easeProgress = this.easeInOutCubic(progress);
                
                this.mminfo.offx = startOffx + (targetOffx - startOffx) * easeProgress;
                this.mminfo.offy = startOffy + (targetOffy - startOffy) * easeProgress;
                
                // Force hover state update by triggering a small, non-visible change
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    // Final position - force a complete repaint
                    this.$forceUpdate();
                }
            };
            
            requestAnimationFrame(animate);
        },
        easeInOutCubic(t) {
            return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
        },
        startDrag(event) {
            this.mminfo.dragging = true;
            this.mminfo.lastMouseX = event.clientX;
            this.mminfo.lastMouseY = event.clientY;
            event.preventDefault();
        },
        doDrag(event) {
            if (!this.mminfo.dragging) return;

            const deltaX = event.clientX - this.mminfo.lastMouseX;
            const deltaY = event.clientY - this.mminfo.lastMouseY;

            this.mminfo.offx += deltaX;
            this.mminfo.offy += deltaY;

            this.mminfo.lastMouseX = event.clientX;
            this.mminfo.lastMouseY = event.clientY;
        },
        stopDrag() {
            this.mminfo.dragging = false;
        },
        startDragTouch(event) {
            this.mminfo.dragging = true;
            const touch = event.touches[0];
            this.mminfo.lastMouseX = touch.clientX;
            this.mminfo.lastMouseY = touch.clientY;
            event.preventDefault();
        },
        doDragTouch(event) {
            if (!this.mminfo.dragging) return;
            
            const touch = event.touches[0];
            const deltaX = touch.clientX - this.mminfo.lastMouseX; // TODO : same as startDrag
            const deltaY = touch.clientY - this.mminfo.lastMouseY;
            
            this.mminfo.offx += deltaX;
            this.mminfo.offy += deltaY;
            
            this.mminfo.lastMouseX = touch.clientX;
            this.mminfo.lastMouseY = touch.clientY;
            
            event.preventDefault();
        },
        handleWheel(event) {
            event.preventDefault();
            const delta = -Math.sign(event.deltaY) * 0.1;
            const newScale = Math.max(0.1, Math.min(3, this.mminfo.scale + delta));

            // Adjust offsets to zoom toward mouse position
            const rect = event.currentTarget.getBoundingClientRect();
            const mouseX = event.clientX - rect.left;
            const mouseY = event.clientY - rect.top;

            const scaleFactor = newScale / this.mminfo.scale;
            this.mminfo.offx = mouseX - (mouseX - this.mminfo.offx) * scaleFactor;
            this.mminfo.offy = mouseY - (mouseY - this.mminfo.offy) * scaleFactor;

            this.mminfo.scale = newScale;
        },
        handleClick(node) {
            this.centerOnNode(node);
            this.mminfo.chemin.push(node);
            this.mindmap_chemin.set(this.mminfo.chemin);
            mmdraw_update(this.mminfo);
        },
        redraw_root(){
            mmdraw_root(this.mminfo);
        },
    },
};
</script>

<template>
    <div class="mm_main_relative" 
        @mousedown="startDrag" @mouseup="stopDrag"
        @mousemove="doDrag" @mouseleave="stopDrag"
        @wheel="handleWheel"
        @touchstart="startDragTouch" @touchend="stopDrag"
        @touchmove="doDragTouch"
        >
        <button class="mm_fullscreenbtn" @click="toggleFullscreen" @touchend="toggleFullscreen">
            <img :src="this.mminfo.fullscreen ? '/imgs/reduire.svg' : '/imgs/agrandir.svg'" 
                :alt="this.mminfo.fullscreen ? 'Exit fullscreen' : 'Enter fullscreen'" 
                class="fullscreen-icon">
        </button>
        <div class="mm_control_outer">
            <div class="mm_controls">
                <!-- TODO : refactor to func zoom -->
                <button @click="this.mminfo.scale += 0.2; this.mminfo.scale = Math.min(5, this.mminfo.scale)" @touchend="this.mminfo.scale += 0.2; this.mminfo.scale = Math.min(5, this.mminfo.scale)">+</button>
                <button @click="this.mminfo.scale -= 0.2; this.mminfo.scale = Math.max(0.2, this.mminfo.scale)" @touchend="this.mminfo.scale -= 0.2; this.mminfo.scale = Math.max(0.2, this.mminfo.scale)">-</button>
                <button @click="this.mminfo.scale = 1" @touchend="this.mminfo.scale = 1">reset zoom</button>
                <button @click="centerOnNode(this.mminfo.nodes[0])" @touchend="centerOnNode(this.mminfo.nodes[0])">recenter</button>
                <button @click="redraw_root()" @touchend="redraw_root()">redraw</button>
            </div>
            <div class="mm_legend_outer">
                <button v-if="mminfo.togglelegend" @click="mminfo.togglelegend = false" @touchend="mminfo.togglelegend = false;">></button>
                <button v-else @click="mminfo.togglelegend = true" @touchend="mminfo.togglelegend = true;"><</button>
                <transition name="mm_legend_anim">
                    <div class="mm_legend" v-if="mminfo.togglelegend">
                        <div v-for="(nameproper, nameclass) in mmLegendClassMap">
                            <div class="mm_legend_cercle"
                                :class="`mmLegendColorMap${nameclass}`"></div>
                            <p>{{ nameproper }}</p>
                        </div>
                    </div>
                </transition>
            </div>
        </div>
        <div v-for="link in mminfo.linkages" :key="link.id" :style="link.getStyle(this.mminfo.scale, this.mminfo.offx, this.mminfo.offy)" class="mm_linkage">
        </div>
        <mindmap_node v-for="node in mminfo.nodes" :node="node" :mminfo="this.mminfo"
            @click="handleClick(node);" @touchend="handleClick(node);" />
    </div>
</template>