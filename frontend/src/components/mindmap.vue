<script>
import { LegendColorMap, mmget } from '../model/mindmap_func.js';

export default {
    name: "comp_mindmap",
    inject: ["searchterm"],
    data() {
        return {
            LegendColorMap: LegendColorMap,
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
        };
    },
    async mounted() {
        this.centerMindmap();
        mmget(this);
    },
    computed: {
        searchValue() {
            return this.searchterm;
        },
    },
    watch: {
        searchValue(newVal) {
            console.log("Search term changed:", newVal);
            mmget(this);
        }
    },
    methods: {
        toggleFullscreen() {
            this.fullscreen = !this.fullscreen;
            const element = this.$el.querySelector('.mm_relative');
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
        centerMindmap(){
            this.offx= window.screen.width/2;
            this.offy= window.screen.height/2;
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
        }
    },
};
</script>

<template>
    <div>
        <h2 class="vert-neon">Mindmap Component</h2>
        <div>Search: {{ searchValue }}</div>
        <div>
            <p v-for="chem in chemin" :key="chem.name">{{ chem.name }}</p>
        </div>
        <div class="mm_relative" 
            @mousedown="startDrag"
            @mousemove="doDrag"
            @mouseup="stopDrag"
            @mouseleave="stopDrag"
            @wheel="handleWheel"
            >
            <button class="mm_fullscreenbtn" @click="toggleFullscreen">
                {{ fullscreen ? '⤢' : '⤢' }}
            </button>
            <div class="mm_control_outer">
                <div class="mm_controls">
                    <button @click="scale += 0.2 ; scale = Math.min(5,scale)">+</button>
                    <button @click="scale -= 0.2 ; scale = Math.max(0.2,scale)">-</button>
                    <button @click="scale = 1">reset zoom</button>
                    <button @click="centerMindmap()">recenter</button>
                </div>
                <div class="mm_legend_outer">
                    <button v-if="togglelegend" @click="togglelegend = false">></button>
                    <button v-else @click="togglelegend = true"><</button>
                    <transition name="slide">
                        <div class="mm_legend" v-if="togglelegend">
                            <div v-for="(legend_color, legend_class) in LegendColorMap" :key="legend_class">
                                <div class="mm_legend_cercle" :style="{ backgroundColor: legend_color }"></div>
                                <p>{{ legend_class }}</p>
                            </div>
                        </div>
                    </transition>
                </div>
            </div>
            <div v-for="link in linkages" :key="link.id" :style="link.getStyle(scale, offx, offy)" class="mm_link"></div>
            <div v-for="node in nodes" :key="node.id" :style="node.getStyle(scale, offx, offy)"
                    class="mm_node"> {{ node.category.name }} </div>
        </div>
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
    width: calc(100% - 5%);
    height: 75vh;
    margin: 0 auto;

    /* Backdrop */
    background-color : var(--gris-moyen);
    border: 3px solid var(--vert-neon);
    box-shadow: 12px 8px 3.2px 6px var(--vert-pale);
    border-radius: 20px;
    padding: 20px;

    overflow: hidden;
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
    background-color : var(--noir);
    color: var(--blanc);
    cursor: pointer;
    transition: all 0.3s ease;
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
    background-color : var(--noir);
    color: var(--blanc);
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
}

.mm_controls button:hover {
    background-color : var(--vert-pale);
    transform: translateY(-2px);
    box-shadow: 0 0 10px var(--vert-neon);
}

/* Legend with animation */
.mm_legend_outer {
    display: flex;
    align-items: center;
    justify-content: flex-end
}
.mm_legend_outer button {
    background-color: var(--noir);
    color: var(--blanc);
    border-radius: 50%;
}

.mm_legend {
    max-width: 400px;
    gap: 1em;
    display: flex;
    flex-wrap: wrap;
    border: 2px solid var(--blanc);
    border-radius: 12px;
    padding: 20px;
    background-color: var(--noir);
    overflow-y: auto;
}

/* Vue Transition Classes */
.slide-enter-active {
    animation: slideIn 0.3s ease-out;
}

.slide-leave-active {
    animation: slideOut 0.3s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideOut {
    from {
        opacity: 1;
        transform: translateX(0);
    }
    to {
        opacity: 0;
        width : 0px;
        height : 0px;
        transform: translateX(30px);
    }
}

.mm_legend>div {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    padding: 6px 0;
}

.mm_legend_cercle {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 15px;
    border: 2px solid var(--blanc);
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
    background-color :  var(--blanc);
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
    background-color : var(--gris-taupe);
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
    background-color : var(--gris-taupe);
    border-radius: 4px;
}

.mm_legend::-webkit-scrollbar-thumb {
    background-color : var(--vert-neon);
    border-radius: 4px;
    box-shadow: 0 0 8px var(--vert-neon);
}

.mm_legend::-webkit-scrollbar-thumb:hover {
    background-color : var(--vert-midel);
}
</style>