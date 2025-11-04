<script>
export default {
    name: "mindmap_node",
    props: {
        nodedata: {
            type: Object,
            class : Object, uuid : String,
            required: true
        },
        position: {
            type: Object,
            x: Number, y: Number, 
            zoom : Number, depth : Number,
            required: true,
        },
    },
};
</script>

<template>
    <div 
        class="mindmap-node" 
        :class="nodeClasses"
        :style="nodeStyle"
        @mousedown="handleMouseDown"
        @click="handleClick"
        :title="nodeContent"
    >
        <div class="node-content">
            {{ nodeContent }}
        </div>
        <div v-if="nodeData.recdata" class="node-subtitle">
            {{ nodeType }}
            <span v-if="hasChildren" class="children-indicator">▶</span>
            <span v-if="isSelected" class="selection-indicator">✓</span>
        </div>
    </div>
</template>