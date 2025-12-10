<script>
import { mm_LegendClassMap } from '../../model/mindmap/mm_const.js';
import { mm_mindmap } from '../../model/mindmap/mm_mindmap.js';
import { mm_node } from '../../model/mindmap/mm_node.js';

export default {
    name: "mindmap_node",
    props: {
        jsclass: {
            type: mm_node,
            required: true,
        },
        jsmm: {
            type: mm_mindmap,
            required: true,
        }
    },
    data() {
        return {
            mm_LegendClassMap: mm_LegendClassMap,
            thumbnailLoading: false,
            isAppearing: true,
        };
    },
    async mounted() {
        // console.table(this.jsclass.toJSON());
        // console.log("isVideoContent",this.jsclass.isVideoContent());
        
        setTimeout(() => {
            this.isAppearing = false;
        }, 50);
        if (this.jsclass.isVideoContent()) {
            this.thumbnailLoading = true;
            this.jsclass.get_miniature().then(value => {
                this.thumbnailUrl = value;
                this.thumbnailLoading = false;
            }).catch(error => {
                console.error(error);
                this.thumbnailLoading = false;
            });
        }
    },
}
</script>

<template>
    <div class="mm_node"
        :class="`mmLegendColorMap${jsclass.category.name} mm_node${this.jsclass.isVideoContent() ? 'Squircle' : 'Round'} ${isAppearing ? 'mm_node_appearing' : ''}`"
        :style="jsclass.getStyle()">
        <div style="display: none;">
            {{ jsclass }}
        </div>
        <template v-if="jsclass.loading">
            <img src="/imgs/spinner.gif" alt="Loading..." class="mm_node_loading-spinner" />
        </template>
        <template v-else>
            <template v-if="!jsclass.content">
                <div class="mm_node_content">
                    <p class="mm_node_title">{{ mm_LegendClassMap[jsclass.category.name] }}</p>
                </div>
            </template>
            <template v-else-if="jsclass.content && !this.jsclass.isVideoContent()">
                <div class="mm_node_content">
                    <p class="mm_node_title">
                        {{ jsclass.content.name || jsclass.content.titre || 'nom Inconnue' }}
                    </p>
                    <p class="mm_node_subtitle">{{ mm_LegendClassMap[jsclass.category.name] }}</p>
                </div>
            </template>
            <template v-if="jsclass.content && this.jsclass.isVideoContent()">
                <div class="mm_node_content">
                    <p class="mm_node_title">
                        {{ jsclass.content.name || jsclass.content.titre || 'nom Inconnue' }}
                    </p>
                    <p class="mm_node_subtitle">{{ mm_LegendClassMap[jsclass.category.name] }}</p>
                    <div class="mm_node_description">
                        <p>uploaded_at : {{ jsclass.content.uploaded_at }}</p>
                        <p>duree : {{ jsclass.content.duree }}</p>
                    </div>
                </div>
                <div class="mm_node_preview">
                    <template v-if="jsclass.thumbnailLoading">
                        <img src="/imgs/spinner.gif" alt="Loading thumbnail..." class="mm_node_loading-spinner" />
                    </template>
                    <template v-else-if="jsclass.thumbnailUrl">
                        <img :src="jsclass.thumbnailUrl" alt="Miniature" class="mm_node_thumbnail">
                    </template>
                    <template v-else>
                        <img src="/imgs/close.svg" alt="erreur image" class="mm_node_no-thumbnail">
                    </template>
                </div>
            </template>
        </template>
    </div>
</template>

<style scoped>
.mm_node {
    position: absolute;
    display: flex;
    flex-direction: row;
    align-items: stretch;
    justify-content: space-between;
    text-align: center;
    color: white;
    cursor: pointer;
    z-index: 5;
    border: 2px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    transition: transform 0.5s ease, opacity 0.5s ease;
    transform: scale(0);
    opacity: 0;
    overflow: hidden;
    /* Remove fixed max-height as it's now controlled by dimensions */
}

.mm_node:not(.mm_node_appearing) {
    transform: scale(1);
    opacity: 1;
}

.mm_node:hover {
    transform: scale(1.08);
    box-shadow: 0 0 25px var(--vert-neon);
}

.mm_nodeSquircle {
    border-radius: 10%;
}

.mm_nodeRound {
    aspect-ratio: 1;
    border-radius: 50%;
}

/* Node content layout title subtitle description */
.mm_node_content {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 12px;
    box-sizing: border-box;
    overflow: hidden;
}

.mm_node_title {
    font-size: 0.9em;
    margin: 0 0 4px 0;
    line-height: 1.1;
    font-weight: bold;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.mm_node_subtitle {
    font-size: 0.7em;
    margin: 0 0 8px 0;
    line-height: 1;
    opacity: 0.9;
    font-weight: normal;
}

.mm_node_description {
    flex: 1;
    overflow-y: auto;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    padding: 6px;
    margin-top: 4px;
}

.mm_node_description p {
    font-size: 0.6em;
    margin: 2px 0;
    line-height: 1.2;
    opacity: 0.8;
}

/* Preview/thumbnail section */
.mm_node_preview {
    width: auto;
    min-width: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px;
    box-sizing: border-box;
    background: rgba(255, 255, 255, 0.05);
}

.mm_node_thumbnail {
    height: 100%;
    max-height: 250px;
    width: auto;
    aspect-ratio: 1;
    object-fit: cover;
    border-radius: 4px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.mm_node_loading-spinner {
    height: 100%;
    max-height: 250px;
    width: auto;
    aspect-ratio: 1;
}

.mm_node_no-thumbnail {
    height: 100%;
    max-height: 250px;
    width: auto;
    aspect-ratio: 1;
    opacity: 0.7;
    padding: 20%;
    box-sizing: border-box;
}
</style>