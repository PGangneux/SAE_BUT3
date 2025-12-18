<script>
import { mm_LegendClassMap } from '../../model/mindmap/mm_const.js';
import mmch_Root  from '../../model/mindmap/mm_chemin_submod/mmch_root.js';

export default {
    name: "mindmap_node",
    props: {
        node_instance: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            mm_LegendClassMap: mm_LegendClassMap,
            thumbnailLoading: false,
            isAppearing: true,
            thumbnailUrl: null,
            nodeTitle: 'Inconnue',
            nodeSubtitle : "Inconnue",
            nodeDescription: [],
            hasMiniature: false,
        };
    },
    methods: {
        async loadNodeData() {
            if (!this.node_instance.mmch_obj) {
                if (this.node_instance.constructor != mmch_Root) {
                    this.nodeTitle = this.mm_LegendClassMap[this.node_instance.constructor.mmch_dbjsclass.name] || 'Inconnue';
                } else {
                    this.nodeTitle = '';
                }
                return;
            } else {
                this.nodeSubtitle = this.mm_LegendClassMap[this.node_instance.constructor.mmch_dbjsclass.name] || 'Inconnue';
            }
            this.nodeTitle = await this.node_instance.mmch_getTitle() || 'Titre Inconnue';
            // Load description
            this.nodeDescription = await this.node_instance.mmch_getDescription();
            // Check if has miniature
            this.thumbnailLoading = true;
            this.hasMiniature = await this.node_instance.mmch_hasMiniature();
            // Load miniature if available
            if (this.hasMiniature) {
                this.thumbnailUrl = await this.node_instance.mmch_getMiniature();
            }
            this.thumbnailLoading = false;
        }
    },
    computed: {
        nodeClass() {
            const baseClass = `mm_node ${this.node_instance.mmch_getStyle()}`;
            const shapeClass = this.hasMiniature ? 'mm_nodeSquircle' : 'mm_nodeRound';
            const appearingClass = this.isAppearing ? 'mm_node_appearing' : '';

            return `${baseClass} ${shapeClass} ${appearingClass}`;
        },
    },
    async mounted() {
        setTimeout(() => {
            this.isAppearing = false;
        }, 50);
        // Load all async data
        await this.loadNodeData();
    },
}
</script>

<template>
    <div class="mm_node" :class="nodeClass" :style="node_instance.getStyle()">
        <div style="display: none;">
            typeof node_instance {{ typeof this.node_instance }}
            thumbnailLoading {{ thumbnailLoading }}
            isAppearing {{ isAppearing }}
            thumbnailUrl {{ thumbnailUrl }}
            nodeTitle {{ nodeTitle }}
            nodeDescription {{ nodeDescription }}
            hasMiniature {{ hasMiniature }}
            node_instance {{ this.node_instance }}
        </div>

        <!-- Case 1: No content -->
        <template v-if="!this.node_instance.mmch_obj">
            <div class="mm_node_content">
                <p class="mm_node_title">{{ nodeTitle }}</p>
                <template v-if="node_instance.loading">
                    <img src="/imgs/spinner.gif" alt="Loading..." class="mm_node_loading-spinner" />
                </template>
            </div>
        </template>

        <!-- Case 3: Has content and miniature -->
        <template v-else-if="this.node_instance.mmch_obj && hasMiniature">
            <div class="mm_node_content">
                <p class="mm_node_title">
                    {{ nodeTitle }}
                </p>
                <p class="mm_node_subtitle">{{ nodeSubtitle }}</p>
                <div class="mm_node_description">
                    <p v-for="(line, index) in nodeDescription" :key="index">
                        {{ line }}
                    </p>
                </div>
                <template v-if="node_instance.loading">
                    <img src="/imgs/spinner.gif" alt="Loading..." class="mm_node_loading-spinner" />
                </template>
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

        <!-- Case 2: Has content but no miniature -->
        <template v-else-if="this.node_instance.mmch_obj && !hasMiniature">
            <div class="mm_node_content">
                <p class="mm_node_title">
                    {{ nodeTitle }}
                </p>
                <p class="mm_node_subtitle">{{ nodeSubtitle }}</p>
                <div class="mm_node_description">
                    <p v-for="(line, index) in nodeDescription" :key="index">
                        {{ line }}
                    </p>
                </div>
                <template v-if="node_instance.loading">
                    <img src="/imgs/spinner.gif" alt="Loading..." class="mm_node_loading-spinner" />
                </template>
            </div>
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