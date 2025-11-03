<script>
import { ref, computed } from 'vue';

export default {
    name: "mindmap_node",
    props: {
        nodeData: {
            type: Object,
            required: true
        },
        position: {
            type: Object,
            x: 0, y: 0
        },
        width: {
            type: Number,
            default: 150
        },
        height: {
            type: Number,
            default: 60
        },
        viewport: {
            type: Object,
            default: () => ({ x: 0, y: 0, scale: 1 })
        },
        isSelected: {
            type: Boolean,
            default: false
        },
        isCurrentSelection: {
            type: Boolean,
            default: false
        }
    },
    setup(props, { emit }) {
        const isDragging = ref(false);
        const dragStart = ref({ x: 0, y: 0 });
        const nodePosition = ref({ ...props.position });

        const nodeStyle = computed(() => {
            return {
                left: `${nodePosition.value.x}%`,
                top: `${nodePosition.value.y}%`,
                width: `${props.width}px`,
                height: `${props.height}px`,
                transform: `translate(-50%, -50%) scale(${1 / props.viewport.scale})`,
                transformOrigin: 'center'
            };
        });

        const nodeContent = computed(() => {
            if (!props.nodeData.recdata) return 'Root Node';
            return props.nodeData.recdata.name || `Node ${props.nodeData.id}`;
        });

        const nodeType = computed(() => props.nodeData.type || 'default');

        const hasChildren = computed(() => {
            const data = props.nodeData.recdata;
            return data && (data.styles || data.extraits);
        });

        const nodeClasses = computed(() => [
            nodeType.value,
            { 
                'has-children': hasChildren.value,
                'selected': props.isSelected,
                'current-selection': props.isCurrentSelection,
                'dragging': isDragging.value
            }
        ]);

        const handleMouseDown = (event) => {
            if (event.button !== 0) return; // Only left click
            
            isDragging.value = true;
            dragStart.value = {
                x: event.clientX,
                y: event.clientY,
                nodeX: nodePosition.value.x,
                nodeY: nodePosition.value.y
            };
            
            event.preventDefault();
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', handleMouseUp);
        };

        const handleMouseMove = (event) => {
            if (!isDragging.value) return;
            
            const dx = (event.clientX - dragStart.value.x) / props.viewport.scale;
            const dy = (event.clientY - dragStart.value.y) / props.viewport.scale;
            
            nodePosition.value = {
                x: dragStart.value.nodeX + (dx / window.innerWidth * 100),
                y: dragStart.value.nodeY + (dy / window.innerHeight * 100)
            };
            
            emit('node-move', props.nodeData.id, nodePosition.value);
        };

        const handleMouseUp = () => {
            isDragging.value = false;
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        };

        const handleClick = (event) => {
            if (!isDragging.value) {
                emit('node-click', props.nodeData);
            }
        };

        return {
            nodeStyle,
            nodeContent,
            nodeType,
            hasChildren,
            nodeClasses,
            handleMouseDown,
            handleClick
        };
    }
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

<style scoped>
.mindmap-node {
    position: absolute;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
    user-select: none;
    border: 2px solid transparent;
}

.mindmap-node:hover {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    transform: translate(-50%, -50%) scale(calc(1 / var(--viewport-scale, 1) * 1.05));
}

.mindmap-node:active {
    cursor: grabbing;
}

/* Selection States */
.mindmap-node.selected {
    border-color: rgba(255, 255, 255, 0.5);
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.3);
}

.mindmap-node.current-selection {
    border-color: #68d391;
    box-shadow: 0 0 0 3px rgba(104, 211, 145, 0.4);
    animation: pulse 2s infinite;
}

.mindmap-node.dragging {
    opacity: 0.8;
    z-index: 1000;
}

/* Node Type Styles */
.root {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-weight: bold;
    font-size: 16px;
    min-width: 200px;
    min-height: 80px;
    z-index: 10;
}

.artiste {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    font-size: 14px;
    min-width: 180px;
    min-height: 70px;
}

.style {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    font-size: 13px;
    min-width: 160px;
    min-height: 60px;
}

.extrait {
    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    color: #2d3748;
    font-size: 12px;
    min-width: 140px;
    min-height: 50px;
}

.has-children {
    border: 2px dashed rgba(255, 255, 255, 0.5);
}

.node-content {
    padding: 8px 12px;
    font-weight: 600;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 100%;
}

.node-subtitle {
    font-size: 11px;
    opacity: 0.9;
    padding: 0 12px 8px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.children-indicator {
    font-size: 10px;
    animation: bounce 2s infinite;
}

.selection-indicator {
    font-size: 12px;
    color: #68d391;
    font-weight: bold;
}
</style>