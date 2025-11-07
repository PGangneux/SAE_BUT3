<script>
import { markRaw } from 'vue';
import { LegendClassMap, LegendColorMap, mmdraw_root , mmdraw_update } from './mindmap_func.js';
import mindmap_node from './mindmap_node.vue';

export default {
    name: "comp_mindmap",
    inject: ["searchterm"],
    components: {
        mindmap_node
    },
    data() {
        return {
            LegendColorMap: LegendColorMap,
            LegendClassMap: LegendClassMap,
            linkages: [],
            nodes: [],
            chemin: [],
            fullscreen: false,
            togglelegend: true,
            scale: 1,
            offx: 0,
            offy: 0,
            dragging: false,
            lastMouseX: 0,
            lastMouseY: 0,
            clickTimer: null, // For click-and-hold functionality
        };
    },
    async mounted() {
        this.centerMindmap();
        mmdraw_root(this);
    },
    computed: {
        searchValue: {
            get() { return this.searchterm.get(); },
        }
    },
    watch: {
        searchValue(newVal) {
            console.log("Search term changed:", newVal);
            mmdraw_root(this);
        }
    },
    methods: {
        toggleFullscreen() {
            this.fullscreen = !this.fullscreen;
            const element = this.$el;
            if (this.fullscreen) {
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
                this.offx = container.clientWidth / 2;
                this.offy = container.clientHeight / 2;
            }
        },
        centerOnNode(node) {
            const container = this.$el;
            if (container) {
                // Calculate target position to center the node
                const targetOffx = container.clientWidth / 2 - node.x * this.scale;
                const targetOffy = container.clientHeight / 2 - node.y * this.scale;

                // Animate over 1 second (1000ms)
                this.animateToPosition(targetOffx, targetOffy, 1000);
            }
        },
        animateToPosition(targetOffx, targetOffy, duration) {
            const startOffx = this.offx;
            const startOffy = this.offy;
            const startTime = performance.now();
            
            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // Easing function for smooth animation
                const easeProgress = this.easeInOutCubic(progress);
                
                this.offx = startOffx + (targetOffx - startOffx) * easeProgress;
                this.offy = startOffy + (targetOffy - startOffy) * easeProgress;
                
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
            this.dragging = true;
            this.lastMouseX = event.clientX;
            this.lastMouseY = event.clientY;
            event.preventDefault();
        },
        doDrag(event) {
            if (!this.dragging) return;

            const deltaX = event.clientX - this.lastMouseX;
            const deltaY = event.clientY - this.lastMouseY;

            this.offx += deltaX;
            this.offy += deltaY;

            this.lastMouseX = event.clientX;
            this.lastMouseY = event.clientY;
        },
        stopDrag() {
            this.dragging = false;
        },
        startDragTouch(event) {
            this.dragging = true;
            const touch = event.touches[0];
            this.lastMouseX = touch.clientX;
            this.lastMouseY = touch.clientY;
            event.preventDefault();
        },
        doDragTouch(event) {
            if (!this.dragging) return;
            
            const touch = event.touches[0];
            const deltaX = touch.clientX - this.lastMouseX;
            const deltaY = touch.clientY - this.lastMouseY;
            
            this.offx += deltaX;
            this.offy += deltaY;
            
            this.lastMouseX = touch.clientX;
            this.lastMouseY = touch.clientY;
            
            event.preventDefault();
        },
        handleWheel(event) {
            event.preventDefault();
            const delta = -Math.sign(event.deltaY) * 0.1;
            const newScale = Math.max(0.1, Math.min(3, this.scale + delta));

            // Adjust offsets to zoom toward mouse position
            const rect = event.currentTarget.getBoundingClientRect();
            const mouseX = event.clientX - rect.left;
            const mouseY = event.clientY - rect.top;

            const scaleFactor = newScale / this.scale;
            this.offx = mouseX - (mouseX - this.offx) * scaleFactor;
            this.offy = mouseY - (mouseY - this.offy) * scaleFactor;

            this.scale = newScale;
        },
        handleClick(node) {
            // console.log("mm click handle node");
            this.centerOnNode(node); // Center on the clicked node
            this.chemin.push(markRaw(node));
            // console.log(this.chemin);
            mmdraw_update(this);
        },
        redraw_root(){
            mmdraw_root(this);
        }
    },
};
</script>

<template>
    <div class="mm_relative" 
        @mousedown="startDrag" @mouseup="stopDrag"
        @mousemove="doDrag" @mouseleave="stopDrag"
        @wheel="handleWheel"
        @touchstart="startDragTouch" @touchend="stopDrag"
        @touchmove="doDragTouch"
        >
        <button class="mm_fullscreenbtn" @click="toggleFullscreen">
            <img :src="fullscreen ? '/imgs/reduire.svg' : '/imgs/agrandir.svg'" 
                :alt="fullscreen ? 'Exit fullscreen' : 'Enter fullscreen'" 
                class="fullscreen-icon">
        </button>
        <div class="mm_control_outer">
            <div class="mm_controls">
                <button @click="scale += 0.2; scale = Math.min(5, scale)">+</button>
                <button @click="scale -= 0.2; scale = Math.max(0.2, scale)">-</button>
                <button @click="scale = 1">reset zoom</button>
                <button @click="centerOnNode(nodes[0])">recenter</button>
                <button @click="redraw_root">redraw</button>
            </div>
            <div class="mm_legend_outer">
                <button v-if="togglelegend" @click="togglelegend = false">></button>
                <button v-else @click="togglelegend = true"><</button>
                <transition name="slide">
                    <div class="mm_legend" v-if="togglelegend">
                        <div v-for="(nameproper, nameclass) in LegendClassMap">
                            <div class="mm_legend_cercle"
                                :style="{ backgroundColor: LegendColorMap[nameclass] }"></div>
                            <p>{{ nameproper }}</p>
                        </div>
                    </div>
                </transition>
            </div>
        </div>
        <div v-for="link in linkages" :key="link.id" :style="link.getStyle(scale, offx, offy)" class="mm_link">
        </div>
        <mindmap_node v-for="node in nodes" :node="node" :scale="scale" :offx="offx" :offy="offy"
            @click="handleClick(node);" class="mm_node" />
    </div>
</template>

<style scoped>
/* Main container */
.vert-neon {
    color: var(--vert-neon);
    text-align: center;
    margin: 0;
    padding: 1rem 0;
    text-shadow: 0 0 10px var(--vert-neon);
}

/* Mindmap container with backdrop */
.mm_relative {
    position: relative;
    width: 100%;
    height: 100%;

    /* Backdrop */
    background-color: var(--gris-moyen);
    border: 3px solid var(--vert-neon);
    box-shadow: 8px 8px 3.2px 5px var(--vert-pale);
    border-radius: 20px;
    padding: 20px;

    overflow: hidden;
    touch-action: none;
}

/* Fullscreen mode */
.mm_relative:fullscreen {
    width: 100vw;
    height: 100vh;
    padding: 2.5%;
    border: 3px solid var(--vert-neon);
}

/* Fullscreen button - top right */
.mm_fullscreenbtn {
    position: absolute;
    width: 30px;
    height: 30px;
    vertical-align: baseline;
    top: 20px;
    right: 20px;
    z-index: 101;
    text-align: center;
    border-radius: 50%;
    border: none;
    background-color: var(--noir);
    color: var(--blanc);
    cursor: pointer;
    transition: all 0.3s ease;
}
.mm_fullscreenbtn img {
    width: 20px;
}

.mm_fullscreenbtn:hover {
    transform: translateY(-2px) scale(1.08);
    box-shadow: 0 0 10px var(--vert-neon);
}

/* Controls - vertical flex on right bottom */
.mm_control_outer {
    position: absolute;
    bottom: 30px;
    right: 30px;
    display: flex;
    flex-direction: column;
    z-index: 100;
    align-items: flex-end
}

.mm_controls {
    display: flex;
    flex-direction: column;
    gap: 15px;
    align-items: center;
}

.mm_controls button {
    padding: 10px;
    border-radius: 40%;
    background-color: var(--noir);
    color: var(--blanc);
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
}

.mm_controls button:hover {
    background-color: var(--vert-pale);
    transform: translateY(-2px);
    box-shadow: 0 0 10px var(--vert-neon);
}

/* Legend with animation */
.mm_legend_outer {
    display: flex;
    align-items: center;
    justify-content: space-evenly;
}

.mm_legend_outer button {
    background-color: var(--noir);
    color: var(--blanc);
    border-radius: 50%;
    transition: all 0.3s ease;
}
.mm_legend_outer button:hover {
    background-color: var(--vert-pale);
    transform: translateY(-2px);
    box-shadow: 0 0 10px var(--vert-neon);
}

.mm_legend {
    max-width: 450px;
    display: flex;
    flex-wrap: wrap;
    border: 2px solid var(--blanc);
    border-radius: 12px;
    padding: 10px;
    background-color: var(--noir);
    overflow: hidden; /* Change from auto to hidden during animation */
    margin-left: 10px; /* Space between legend and toggle button */
}

/* Vue Transition Classes */
.slide-enter-active,
.slide-leave-active {
    transition: all 0.3s ease-out;
}

.slide-enter-from {
    opacity: 0;
    max-width: 0;
    max-height: 0;
    padding: 0;
    margin-right: 0;
    transform: translateX(30px);
}

.slide-enter-to {
    opacity: 1;
    max-width: 400px;
    max-height: 400px; /* Adjust based on your content */
    padding: 10px;
    margin-right: 10px;
    transform: translateX(0);
}

.slide-leave-from {
    opacity: 1;
    max-width: 400px;
    max-height: 500px;
    padding: 10px;
    margin-right: 10px;
    transform: translateX(0);
}

.slide-leave-to {
    opacity: 0;
    max-width: 0;
    max-height: 0;
    padding: 0;
    margin-right: 0;
    transform: translateX(30px);
}

.mm_legend>div {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    padding: 0 6px;
    min-width: 100px; /* Prevent content from squeezing during animation */
}

.mm_legend_cercle {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 15px;
    flex-shrink: 0;
}

.mm_legend p {
    margin: 0;
    font-weight: 500;
    color: var(--blanc);
}

/* Links */
.mm_link {
    position: absolute;
    background-color: var(--blanc);
    transform-origin: 0 0;
    pointer-events: none;
    z-index: 2;
}

/* Nodes */
.mm_node {
    position: absolute;
    border-radius: 100%;
    cursor: pointer;
    z-index: 5;
    text-align: center;
    color: var(--blanc);
}

.mm_node:hover {
    transform: scale(1.08);
    box-shadow: 0 0 25px var(--vert-neon);
}

/* Toggle buttons for legend */
.mm_controls>div {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.mm_controls>div button {
    padding: 6px 10px;
    background-color: var(--gris-taupe);
}

/* Mobile styles - controls at top right when screen < 800px */
@media (max-width: 800px) {
    .mm_controls {
        position: absolute;
        top: 20px;
        right: 20px;
        bottom: auto;
        flex-direction: column;
        gap: 8px;
        padding: 15px;
    }

    .mm_fullscreenbtn {
        top: 20px;
        right: auto;
        left: 20px;
    }

    .mm_relative {
        width: calc(100% - 10%);
        height: 70vh;
        padding: 15px;
    }

    .mm_legend {
        max-height: 200px;
        padding: 15px;
    }
}

/* Scrollbar for legend */
.mm_legend::-webkit-scrollbar {
    width: 8px;
}

.mm_legend::-webkit-scrollbar-track {
    background-color: var(--gris-taupe);
    border-radius: 4px;
}

.mm_legend::-webkit-scrollbar-thumb {
    background-color: var(--vert-neon);
    border-radius: 4px;
    box-shadow: 0 0 8px var(--vert-neon);
}

.mm_legend::-webkit-scrollbar-thumb:hover {
    background-color: var(--vert-midel);
}
</style>