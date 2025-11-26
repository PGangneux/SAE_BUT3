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
        };
    },
    computed: {
        isVideoContent() {
            return this.node.content && (this.node.category.name === 'Extrait' || this.node.category.name === 'Interview');
        }
    },
    methods: {
        getStyle() {
            const size = 100 * this.mminfo.scale;
            const sizetext = 20 * this.mminfo.scale;
            const scaledX = this.node.x * this.mminfo.scale;
            const scaledY = this.node.y * this.mminfo.scale;
            return {
                "width": size + "px",
                "left": (scaledX + this.mminfo.offx) + "px",
                "top": (scaledY + this.mminfo.offy) + "px",
                "font-size": sizetext + "px",
                "line-height": size + "px",
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
        <div v-if="node.loading" class="loading-spinner">
            <img src="/imgs/spinner.gif" alt="Loading..." />
        </div>
        <div v-else class="node-content">
            <p class="category-name">{{ mmLegendClassMap[node.category.name] }}</p>
            <p v-if="node.content" class="content-name">
                {{ node.content.name || node.content.titre || 'Sans nom' }}
            </p>
            <div v-if="node.content && (node.category.name === 'Extrait' || node.category.name === 'Interview')"
                class="video-badge">
                {{ node.category.name === 'Extrait' ? 'Extrait' : 'Interview' }}
            </div>
            <div v-if="isVideoContent" class="thumbnail-container">
                <div v-if="thumbnailLoading" class="thumbnail-loading">
                    <img src="/imgs/spinner.gif" alt="Loading thumbnail..." class="thumbnail-spinner" />
                </div>
                <img v-else-if="thumbnailUrl" :src="thumbnailUrl" alt="Miniature" class="thumbnail"
                    @error="thumbnailUrl = null" />
                <div v-else class="no-thumbnail">
                    <img src="/imgs/close.svg" alt="erreur image">
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Nodes */
.mm_node {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
    cursor: pointer;
    z-index: 5;
    border: 2px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    transition: transform 0.5s ease, opacity 0.5s ease;
    transform: scale(0);
    opacity: 0;
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


.loading-spinner {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}

.loading-spinner img {
    width: 50%;
    height: 50%;
}

.node-content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 8px;
    box-sizing: border-box;
    gap: 4px;
}

.category-name {
    font-size: 0.9em;
    margin: 0;
    line-height: 1.1;
    font-weight: bold;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.content-name {
    font-size: 0.7em;
    margin: 0;
    line-height: 1;
    opacity: 0.9;
    font-weight: normal;
}

.video-badge {
    font-size: 0.6em;
    background: rgba(255, 255, 255, 0.2);
    padding: 2px 6px;
    border-radius: 10px;
    margin: 2px 0;
}

.thumbnail-container {
    width: 80%;
    height: 40%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.thumbnail {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 5px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.thumbnail-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}

.thumbnail-spinner {
    width: 50%;
    height: 50%;
}

.no-thumbnail {
    font-size: 1.5em;
    opacity: 0.7;
}

/* Responsive text sizing based on scale */
.node-content {
    font-size: calc(0.8em * v-bind('scale'));
}
</style>