<script>
import { mmInfo, mmLegendClassMap, mmNode } from "../../model/mindmap/mindmap_base.js";

export default {
    name: "mindmap_node",
    props: {
        node: {
            type: mmNode,
            required: true,
        },
        mminfo: {
            type: mmInfo,
            required: true,
        }
    },
    data() {
        return {
            mmLegendClassMap: mmLegendClassMap,
            thumbnailUrl: null,
            thumbnailLoading: false,
            isAppearing: true,
            // Default dimensions for different node types
            nodeDimensions: {
                default: { width: 100, height: 100 },
                squircle: { width: 300, height: 150 }, // Adjust based on your design
                round: { width: 100, height: 100 }
            }
        };
    },
    computed: {
        isVideoContent() {
            return this.node.content && (this.node.category.name === 'Extrait' || this.node.category.name === 'Interview');
        },
        currentNodeDimensions() {
            if (this.isVideoContent) {
                return this.nodeDimensions.squircle;
            }
            return this.nodeDimensions.round;
        }
    },
    methods: {
        getStyle() {
            const baseWidth = this.currentNodeDimensions.width;
            const baseHeight = this.currentNodeDimensions.height;
            
            const scaledWidth = baseWidth * this.mminfo.scale;
            const scaledHeight = baseHeight * this.mminfo.scale;
            const sizetext = 20 * this.mminfo.scale;
            
            // Calculate position - adjust for node center
            const scaledX = (this.node.x * this.mminfo.scale) - (scaledWidth / 2);
            const scaledY = (this.node.y * this.mminfo.scale) - (scaledHeight / 2);
            
            return {
                "left": (scaledX + this.mminfo.offx) + "px",
                "top": (scaledY + this.mminfo.offy) + "px",
                "width": scaledWidth + "px",
                "height": scaledHeight + "px",
                "font-size": sizetext + "px",
                "line-height": (scaledHeight * 0.8) + "px", // Adjust line-height based on height
            };
        },

        async get_miniature() {
            if (!this.node.content) return null;
            if (this.thumbnailUrl) return this.thumbnailUrl;

            try {
                // Cas 1 : c'est un extrait
                if (this.node.category.name === 'Extrait') {
                    return (this.node.content.url_miniature_yt
                        /// await video.get_url_miniature_vimeo() || 
                    );
                }

                // Cas 2 : c'est une interview
                const extraits = await this.node.content.extraits;
                if (!extraits || extraits.length === 0) {
                    console.warn(`Aucun extrait trouvé pour l'interview ${this.node.content}`);
                    return null;
                }

                const firstExtrait = extraits[0];

                return (
                    firstExtrait.url_miniature_yt
                    /// await firstExtrait.get_url_miniature_vimeo() || 
                );

            } catch (err) {
                console.error("Erreur lors de la récupération de la miniature :", err);
                return null;
            }
        },
    },
    watch: {
        'node.loading': {
            async handler() {
                if (this.isVideoContent) {
                    this.thumbnailLoading = true;
                    this.thumbnailUrl = await this.get_miniature();
                    this.thumbnailLoading = false;
                }
            },
            deep: true
        }
    },
    async mounted() {
        if (this.isVideoContent) {
            this.thumbnailLoading = true;
            this.thumbnailUrl = await this.get_miniature();
            this.thumbnailLoading = false;
        }
        setTimeout(() => {
            this.isAppearing = false;
        }, 50);
    },
}
</script>

<template>
    <div class="mm_node"
        :class="`mmLegendColorMap${node.category.name} mm_node${isVideoContent ? 'Squircle' : 'Round'} ${isAppearing ? 'mm_node_appearing' : ''}`"
        :style="getStyle()">
        <div style="display: none;">
            {{ this.node }}
        </div>
        <template v-if="node.loading" class="mm_node_loading-spinner">
            <img src="/imgs/spinner.gif" alt="Loading..." />
        </template>
        <template v-else>
            <template v-if="!node.content">
                <div class="mm_node_content">
                    <p class="mm_node_title">{{ mmLegendClassMap[node.category.name] }}</p>
                </div>
            </template>
            <template v-else-if="node.content && !isVideoContent">
                <div class="mm_node_content">
                    <p class="mm_node_title">
                        {{ node.content.name || node.content.titre || 'nom Inconnue' }}
                    </p>
                    <p class="mm_node_subtitle">{{ mmLegendClassMap[node.category.name] }}</p>
                </div>
            </template>
            <template v-if="node.content && isVideoContent">
                <div class="mm_node_content">
                    <p class="mm_node_title">
                        {{ node.content.name || node.content.titre || 'nom Inconnue' }}
                    </p>
                    <p class="mm_node_subtitle">{{ mmLegendClassMap[node.category.name] }}</p>
                    <div class="mm_node_description">
                        <p>uploaded_at : {{ this.node.content.uploaded_at }}</p>
                        <p>duree : {{ this.node.content.duree }}</p>
                    </div>
                </div>
                <div class="mm_node_preview">
                    <template v-if="thumbnailLoading">
                        <img src="/imgs/spinner.gif" alt="Loading thumbnail..." class="mm_node_loading-spinner" />
                    </template>
                    <template v-else-if="thumbnailUrl">
                        <img :src="thumbnailUrl" alt="Miniature" class="mm_node_thumbnail">
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