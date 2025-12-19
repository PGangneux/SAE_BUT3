import { mm_draw_root , mm_interface_handleclick } from "./mm_funcs/mm_interface.js";
import mm_Linkage from "./mm_linkage.js";
import mmch_CheminT from './mm_chemin_submod/mmch_chemin.js';

export default class mm_Mindmap {
    /** @type {Object} */
    vueobj;
    /** @type {Array<mm_Linkage>} */
    linkages;
    /** @type {Array<mmch_CheminT>} */
    nodes;
    /** @type {Array<mmch_CheminT>} */
    chemin;
    /** @type {Array<mm_Linkage>} */
    previewlinkages;
    /** @type {Array<mmch_CheminT>} */
    previewnodes;
    /** @type {boolean} */
    fullscreen;
    /** @type {boolean} */
    togglelegend;
    /** @type {number} */
    scale;
    /** @type {number} */
    offx;
    /** @type {number} */
    offy;
    /** @type {number} */
    lastMouseX;
    /** @type {number} */
    lastMouseY;
    /** @type {number} */
    clickTimer;
    /** @type {boolean} */
    dragging;
    /** @type {String} */
    searchval;

    interview_current;
    extrait_current;

    /**
     * @param {Object} vueobj 
     * @param {any} interview_current 
     * @param {any} extrait_current 
     */
    constructor(vueobj, interview_current, extrait_current) {        
        // vue object reference
        this.vueobj = vueobj;
        // mm data
        this.linkages = [];
        this.nodes = [];
        // mm preview data
        this.previewlinkages = [];
        this.previewnodes = [];
        // mm chemin
        this.chemin = [];
        // vars
        this.fullscreen = false;
        this.togglelegend = true;
        this.scale = 1;
        this.offx = 0;
        this.offy = 0;
        this.lastMouseX = 0;
        this.lastMouseY = 0;
        this.clickTimer = null;
        this.dragging = false;
        this.searchval = "";

        // funcs ref
        this.interview_current = interview_current;
        this.extrait_current = extrait_current;
    }

    toJSON() {
        return {
            // linkages: this.linkages,
            // nodes: this.nodes,
            chemin: this.chemin,
            fullscreen: this.fullscreen,
            togglelegend: this.togglelegend,
            scale: this.scale,
            offx: this.offx,
            offy: this.offy,
            lastMouseX: this.lastMouseX,
            lastMouseY: this.lastMouseY,
            clickTimer: this.clickTimer,
            dragging: this.dragging,
            searchval: this.searchval
        };
    }

    toggleFullscreen() {
        this.fullscreen = !this.fullscreen;
        const element = this.vueobj.$el;
        if (this.fullscreen) {
            if (element.requestFullscreen) {
                element.requestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    }

    async draw_root() {
        this.centerMindmap();
        await mm_draw_root(this);
        this.centerOnNode(this.nodes[0]);
    }

    startDrag(event) {
        this.dragging = true;
        const { clientX, clientY } = this.getEventCoordinates(event);
        this.lastMouseX = clientX;
        this.lastMouseY = clientY;
        event.preventDefault();
    }

    stopDrag() {
        this.dragging = false;
    }

    startDragTouch(event) {
        this.startDrag(event);
    }

    zoomin() {
        this.scale += 0.2;
        this.scale = Math.min(5, this.scale);
    }

    zoomout() {
        this.scale -= 0.2;
        this.scale = Math.max(0.2, this.scale);
    }

    zoomreset() {
        this.scale = 1;
    }

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

    async handleClick(node) {
        this.centerOnNode(node);
        await mm_interface_handleclick(this,node);
    }

    centerMindmap() {
        const container = this.vueobj.$el;
        if (container) {
            this.offx = container.clientWidth / 2;
            this.offy = container.clientHeight / 2;
        }
    }

    centerOnNode(node) {
        const container = this.vueobj.$el;
        if (container) {
            // Calculate target position to center the node
            const targetOffx = container.clientWidth / 2 - node.x * this.scale;
            const targetOffy = container.clientHeight / 2 - node.y * this.scale;

            // Animate over 1 second (1000ms)
            this.animateToPosition(targetOffx, targetOffy, 1000);
        }
    }

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
                this.vueobj.$forceUpdate();
            }
        };

        requestAnimationFrame(animate);
    }

    easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    doDrag(event) {
        if (!this.dragging) return;

        const { clientX, clientY } = this.getEventCoordinates(event);
        const deltaX = clientX - this.lastMouseX;
        const deltaY = clientY - this.lastMouseY;

        this.offx += deltaX;
        this.offy += deltaY;

        this.lastMouseX = clientX;
        this.lastMouseY = clientY;
    }

    // Helper methods
    getEventCoordinates(event) {
        if (event.type.includes('touch')) {
            const touch = event.touches[0];
            return {
                clientX: touch.clientX,
                clientY: touch.clientY
            };
        }
        return {
            clientX: event.clientX,
            clientY: event.clientY
        };
    }
}