<script>
import { LegendClassMap, mmNode } from "./mindmap_func";

export default {
    name: "mindmap_node",
    props: {
        node: {
            type: mmNode,
            required: true,
        },
        scale: {
            type: Number,
            required: true,
        },
        offx: {
            type: Number,
            required: true,
        },
        offy: {
            type: Number,
            required: true,
        },
    },
    data() {
        return {
            LegendClassMap: LegendClassMap,
            thumbnailUrl: null,
            thumbnailLoading: false,
        };
    },
    computed: {
        displayName() {
            // Always show the category name
            const categoryName = this.LegendClassMap[this.node.category.name] || this.node.category.name;

            // If there's content, show it alongside the category
            if (this.node.content) {
                const contentName = this.node.content.nom || this.node.content.titre || 'Sans nom';
                return `${categoryName}: ${contentName}`;
            }

            // If no content, just show the category
            return categoryName;
        },
        isVideoContent() {
            return this.node.content &&
                (this.node.category.name === 'Extrait' || this.node.category.name === 'Interview');
        }
    },
    methods: {
        async get_miniature(video) {
            if (!video) return null;

            try {
                // Cas 1 : c'est un extrait
                if (!video.extraits) {
                    return (
                        video.url_miniature_yt ||
                        (await video.get_url_miniature_vimeo())
                    );
                }

                // Cas 2 : c'est une interview
                const extraits = await video.extraits;
                if (!extraits || extraits.length === 0) {
                    console.warn(`Aucun extrait trouvé pour l'interview ${video.uuid}`);
                    return null;
                }

                const firstExtrait = extraits[0];
                return (
                    firstExtrait.url_miniature_yt ||
                    (await firstExtrait.get_url_miniature_vimeo())
                );

            } catch (err) {
                console.error("Erreur lors de la récupération de la miniature :", err);
                return null;
            }
        },

        async loadThumbnail() {
            if (!this.isVideoContent) return;

            this.thumbnailLoading = true;
            this.thumbnailUrl = await this.get_miniature(this.node.content);
            this.thumbnailLoading = false;
        }
    },
    mounted() {
        if (this.isVideoContent) {
            this.loadThumbnail();
        }
    },
    watch: {
        'node.content': {
            handler() {
                if (this.isVideoContent) {
                    this.loadThumbnail();
                } else {
                    this.thumbnailUrl = null;
                }
            },
            deep: true
        }
    }
}
</script>

<template>
    <div class="mindmap-node" :style="node.getStyle(scale, offx, offy)">
        <div v-if="node.loading" class="loading-spinner">
            <img src="/imgs/spinner.gif" alt="Loading..." />
        </div>
        <div v-else class="node-content">
            <!-- Always show category name -->
            <p class="category-name">{{ LegendClassMap[node.category.name] }}</p>

            <!-- Show content name if available -->
            <p v-if="node.content" class="content-name">
                {{ node.content.titre || 'Sans nom' }}
            </p>

            <!-- Show video type badge for Interview/Extrait -->
            <div v-if="node.content && (node.category.name === 'Extrait' || node.category.name === 'Interview')"
                class="video-badge">
                {{ node.category.name === 'Extrait' ? 'Extrait' : 'Interview' }}
            </div>

            <!-- Thumbnail with loading state -->
            <div v-if="isVideoContent" class="thumbnail-container">
                <div v-if="thumbnailLoading" class="thumbnail-loading">
                    <img src="/imgs/spinner.gif" alt="Loading thumbnail..." class="thumbnail-spinner" />
                </div>
                <img v-else-if="thumbnailUrl" :src="thumbnailUrl" alt="Miniature" class="thumbnail"
                    @error="thumbnailUrl = null" />
                <div v-else class="no-thumbnail">
                    📹
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.mindmap-node {
    position: absolute;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
    font-weight: bold;
    overflow: hidden;
    border: 2px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
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