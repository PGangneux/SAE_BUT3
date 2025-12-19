<script>
import { mm_LegendClassMap } from '../../model/mindmap/mm_const.js';
import mmch_Root from '../../model/mindmap/mm_chemin_submod/mmch_root.js';

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
            isAppearing: true,
            isDisappearing: false,
            nodeTitle: 'Inconnue',
            nodeSubtitle: "Inconnue",
            nodeDescription: [],
            hasMiniature: false,
            thumbnailLoading: false,
            thumbnailUrl: null,
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
            const disappearingClass = this.isDisappearing ? 'mm_node_disappearing' : '';

            return `${baseClass} ${shapeClass} ${appearingClass} ${disappearingClass}`;
        },
    },
    async mounted() {
        setTimeout(() => {
            this.isAppearing = false;
        }, 50);
        // Load all async data
        await this.loadNodeData();
    },
    beforeUnmount() {
        this.isDisappearing = true;
        // Wait for animation to complete before actually unmounting
        return new Promise(resolve => {
            setTimeout(() => {
                resolve();
            }, 1000);
        });
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
            node_instance {{ }}
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