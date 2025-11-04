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