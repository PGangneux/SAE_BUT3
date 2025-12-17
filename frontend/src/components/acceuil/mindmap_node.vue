<script>
import { mm_LegendClassMap } from '../../model/mindmap/mm_const.js';

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
            nodeDescription: [],
            hasMiniature: false,
        };
    },
    methods: {
        hasContent() {
            // Safe check for content - handles markRaw objects
            return this.node_instance.mmch_obj !== null && 
                   this.node_instance.mmch_obj !== undefined;
        },
        async loadNodeData() {
            // console.log("loading ", this.node_instance, this.node_instance.mmch_obj);
            
            // Use the safe hasContent method
            if (this.hasContent()) {
                try {
                    this.nodeTitle = await this.node_instance.mmch_getTitle() || 'Inconnue';
                } catch (error) {
                    console.error('Failed to load title:', error);
                    this.nodeTitle = 'Inconnue';
                }
            }

            // Check if has miniature
            this.thumbnailLoading = true;
            try {
                this.hasMiniature = await this.node_instance.mmch_hasMiniature();
            } catch (error) {
                console.error('Failed to check miniature:', error);
                this.hasMiniature = false;
            }

            // Load miniature if available
            if (this.hasMiniature) {
                try {
                    this.thumbnailUrl = await this.node_instance.mmch_getMiniature();
                } catch (error) {
                    console.error('Failed to load thumbnail:', error);
                    this.thumbnailUrl = null;
                }
            }
            this.thumbnailLoading = false;

            // Load description if available - fixed: check mmch_obj not content
            if (this.hasContent() && this.hasMiniature) {
                try {
                    this.nodeDescription = await this.node_instance.mmch_getDescription();
                } catch (error) {
                    console.error('Failed to load description:', error);
                    this.nodeDescription = [];
                }
            }
        }
    },
    computed: {
        nodeSubtitle() {
            return this.mm_LegendClassMap[this.node_instance.constructor.name] || 'Inconnue';
        },
        nodeClass() {
            const baseClass = `mm_node ${this.node_instance.mmch_getStyle()}`;
            const shapeClass = this.hasMiniature ? 'mm_nodeSquircle' : 'mm_nodeRound';
            const appearingClass = this.isAppearing ? 'mm_node_appearing' : '';

            return `${baseClass} ${shapeClass} ${appearingClass}`;
        },
        // Computed property for safe content checking in template
        hasContentComputed() {
            return this.hasContent();
        }
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
            thumbnailLoading {{ thumbnailLoading }}
            isAppearing {{ isAppearing }}
            thumbnailUrl {{ thumbnailUrl }}
            nodeTitle {{ nodeTitle }}
            nodeDescription {{ nodeDescription }}
            hasMiniature {{ hasMiniature }}
            hasContent {{ hasContentComputed }}
            node_instance {{ node_instance.toJSON() }}
        </div>

        <!-- Case 1: No content -->
        <template v-if="!hasContentComputed">
            <div class="mm_node_content">
                <p class="mm_node_title">{{ nodeSubtitle }}</p>
                <template v-if="node_instance.loading">
                    <img src="/imgs/spinner.gif" alt="Loading..." class="mm_node_loading-spinner" />
                </template>
            </div>
        </template>

        <!-- Case 3: Has content and miniature -->
        <template v-else-if="hasContentComputed && hasMiniature">
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
        <template v-else-if="hasContentComputed && !hasMiniature">
            <div class="mm_node_content">
                <p class="mm_node_title">
                    {{ nodeTitle }}
                </p>
                <p class="mm_node_subtitle">{{ nodeSubtitle }}</p>
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