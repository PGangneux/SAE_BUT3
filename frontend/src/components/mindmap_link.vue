<script>
import { computed } from 'vue';

export default {
    name: "mindmap_link",
    props: {
        parentNode: {
            type: Object,
            required: true
        },
        childNode: {
            type: Object,
            required: true
        }
    },
    setup(props) {
        // Reactive computed properties that update when node positions change
        const linkData = computed(() => {
            if (!props.parentNode || !props.childNode) return null;

            const parentX = props.parentNode.position.x;
            const parentY = props.parentNode.position.y;
            const childX = props.childNode.position.x;
            const childY = props.childNode.position.y;

            // Calculate the vector between nodes
            const dx = childX - parentX;
            const dy = childY - parentY;
            const distance = Math.sqrt(dx * dx + dy * dy);
            const angle = Math.atan2(dy, dx) * 180 / Math.PI;

            // Calculate node dimensions for proper connection points
            const parentWidth = props.parentNode.width || 0;
            const parentHeight = props.parentNode.height || 0;
            const childWidth = props.childNode.width || 0;
            const childHeight = props.childNode.height || 0;
            
            // Calculate the actual connection points at node edges
            const parentRadius = Math.max(parentWidth, parentHeight) / 200; // Convert to % since positions are in %
            const childRadius = Math.max(childWidth, childHeight) / 200;
            
            // Adjust distance to connect to node edges instead of centers
            const adjustedDistance = Math.max(0, distance - parentRadius - childRadius);

            // Calculate start position (from parent edge)
            const startX = parentX + (dx / distance) * parentRadius;
            const startY = parentY + (dy / distance) * parentRadius;

            return {
                startX,
                startY,
                distance: adjustedDistance,
                angle,
                dx,
                dy
            };
        });

        const linkStyle = computed(() => {
            if (!linkData.value) return {};
            
            return {
                width: `${linkData.value.distance}%`,
                left: `${linkData.value.startX}%`,
                top: `${linkData.value.startY}%`,
                transform: `rotate(${linkData.value.angle}deg)`,
                transformOrigin: '0 0'
            };
        });

        const linkClasses = computed(() => {
            const parentType = props.parentNode?.type || 'default';
            const childType = props.childNode?.type || 'default';
            
            return [
                parentType,
                childType
            ];
        });

        const isValidLink = computed(() => {
            return props.parentNode && props.childNode && 
                   props.parentNode.position && props.childNode.position &&
                   props.parentNode.position.x !== undefined && 
                   props.parentNode.position.y !== undefined &&
                   props.childNode.position.x !== undefined && 
                   props.childNode.position.y !== undefined &&
                   linkData.value && linkData.value.distance > 0;
        });

        // Debug info (optional)
        const debugInfo = computed(() => {
            if (!linkData.value) return '';
            return `P:(${props.parentNode.position.x},${props.parentNode.position.y}) → C:(${props.childNode.position.x},${props.childNode.position.y}) Dist:${linkData.value.distance.toFixed(1)}%`;
        });

        return {
            linkStyle,
            linkClasses,
            isValidLink,
            debugInfo
        };
    }
};
</script>

<template>
    <div 
        v-if="isValidLink"
        class="mindmap-link" 
        :class="linkClasses"
        :style="linkStyle"
        :title="debugInfo"
    >
        <!-- Optional: Add connection points for debugging -->
        <div class="connection-point start"></div>
        <div class="connection-point end"></div>
    </div>
</template>

<style scoped>
.mindmap-link {
    position: absolute;
    height: 2px;
    background: linear-gradient(90deg, 
        rgba(255, 255, 255, 0.9) 0%, 
        rgba(255, 255, 255, 0.7) 50%, 
        rgba(255, 255, 255, 0.9) 100%);
    pointer-events: none;
    z-index: -1;
    border-radius: 1px;
    transition: all 0.3s ease; /* Smooth transitions when nodes move */
}

/* Connection points for debugging (optional) */
.connection-point {
    position: absolute;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: red;
    transform: translate(-50%, -50%);
}

.connection-point.start {
    left: 0;
    top: 0;
}

.connection-point.end {
    left: 100%;
    top: 0;
}

/* Different link styles based on node types */
.mindmap-link.root.artiste {
    background: linear-gradient(90deg, 
        rgba(102, 126, 234, 0.9) 0%, 
        rgba(247, 87, 108, 0.9) 100%);
    height: 3px;
    box-shadow: 0 0 8px rgba(102, 126, 234, 0.5);
}

.mindmap-link.artiste.style {
    background: linear-gradient(90deg, 
        rgba(247, 87, 108, 0.9) 0%, 
        rgba(79, 172, 254, 0.9) 100%);
    height: 2px;
    box-shadow: 0 0 6px rgba(247, 87, 108, 0.4);
}

.mindmap-link.artiste.extrait,
.mindmap-link.style.extrait {
    background: linear-gradient(90deg, 
        rgba(79, 172, 254, 0.9) 0%, 
        rgba(67, 233, 123, 0.9) 100%);
    height: 2px;
    animation: flow 2s infinite linear;
    box-shadow: 0 0 6px rgba(79, 172, 254, 0.4);
}

/* Arrow head at the end of the link */
.mindmap-link::after {
    content: '';
    position: absolute;
    right: -4px;
    top: -3px;
    width: 8px;
    height: 8px;
    border-right: 2px solid rgba(255, 255, 255, 0.9);
    border-top: 2px solid rgba(255, 255, 255, 0.9);
    transform: rotate(45deg);
    border-radius: 1px;
    transition: all 0.3s ease;
}

/* Specific arrow colors for different link types */
.mindmap-link.root.artiste::after {
    border-color: rgba(247, 87, 108, 0.9);
}

.mindmap-link.artiste.style::after {
    border-color: rgba(79, 172, 254, 0.9);
}

.mindmap-link.artiste.extrait::after,
.mindmap-link.style.extrait::after {
    border-color: rgba(67, 233, 123, 0.9);
    animation: pulse 1.5s infinite;
}

/* Animations */
@keyframes flow {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: rotate(45deg) scale(1); }
    50% { opacity: 0.7; transform: rotate(45deg) scale(1.2); }
}

/* Hover effects for better visual feedback */
.mindmap-link:hover {
    height: 4px;
    z-index: 1;
}
</style>