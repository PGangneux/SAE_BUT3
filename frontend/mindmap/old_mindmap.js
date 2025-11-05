setup() {
        // Inject searchterm here for Composition API
        const searchterm = inject("searchterm");
        
        const artistes = ref([]);
        const nodes = ref([]);
        const currentPath = ref([0]);
        const selectionHistory = ref([]);
        const viewport = reactive({
            x: 0,
            y: 0,
            scale: 1
        });

        // Compute visible nodes based on current path
        const visibleNodes = computed(() => {
            const visible = new Set();
            
            // Always show root and its direct children
            const rootNode = nodes.value.find(n => n.id === 0);
            if (rootNode) {
                visible.add(rootNode);
                nodes.value.filter(n => n.parentId === 0).forEach(child => visible.add(child));
            }

            // Show current path and their children
            currentPath.value.forEach(nodeId => {
                const node = nodes.value.find(n => n.id === nodeId);
                if (node) {
                    visible.add(node);
                    // Show children of the current path nodes
                    nodes.value.filter(n => n.parentId === nodeId).forEach(child => visible.add(child));
                }
            });

            return Array.from(visible);
        });

        // Compute links for visible nodes
        const visibleLinks = computed(() => {
            const linkList = [];
            visibleNodes.value.forEach(node => {
                if (node.parentId !== null && node.parentId !== undefined) {
                    const parentNode = nodes.value.find(n => n.id === node.parentId);
                    if (parentNode && visibleNodes.value.includes(parentNode)) {
                        linkList.push({
                            id: `link-${node.parentId}-${node.id}`,
                            parentId: node.parentId,
                            childId: node.id
                        });
                    }
                }
            });
            return linkList;
        });

        // Get the current selected node (last in history)
        const currentSelection = computed(() => {
            return selectionHistory.value.length > 0 
                ? selectionHistory.value[selectionHistory.value.length - 1]
                : null;
        });

        const searchValue = computed({
            get() { 
                return searchterm ? searchterm.get() : ""; // Add null check
            },
            set(v) { 
                if (searchterm) searchterm.set(v); // Add null check
            }
        });

        // Rest of your setup code remains the same...
        const initializeNodes = async () => {
            artistes.value = await Artiste.list();
            
            // Root node
            nodes.value = [
                {
                    id: 0,
                    recdata: null,
                    parentId: null,
                    position: { x: 50, y: 50 },
                    width: 200,
                    height: 80,
                    type: 'root'
                }
            ];

            // Add artist nodes as children of root
            artistes.value.forEach((art, index) => {
                const angle = (index / artistes.value.length) * 2 * Math.PI;
                const radius = 200;
                nodes.value.push({
                    id: art.id || `artiste-${index + 1}`,
                    recdata: art,
                    parentId: 0,
                    position: {
                        x: 50 + Math.cos(angle) * radius,
                        y: 50 + Math.sin(angle) * radius
                    },
                    width: 180,
                    height: 70,
                    type: 'artiste'
                });
            });
        };

        // Handle node click
        const handleNodeClick = (nodeData) => {
            if (nodeData.type === 'root') {
                currentPath.value = [0];
                return;
            }

            // Add to selection history
            if (!selectionHistory.value.some(item => item.id === nodeData.id)) {
                selectionHistory.value.push({
                    id: nodeData.id,
                    type: nodeData.type,
                    name: nodeData.recdata?.name || `Node ${nodeData.id}`,
                    data: nodeData.recdata,
                    timestamp: new Date()
                });
            }

            const hasChildren = nodeData.recdata && 
                (nodeData.recdata.styles || nodeData.recdata.extraits);
            
            if (hasChildren) {
                if (!currentPath.value.includes(nodeData.id)) {
                    currentPath.value.push(nodeData.id);
                    spawnChildren(nodeData);
                }
            } else {
                handleNodeAction(nodeData);
            }
        };

        // Spawn children nodes for a given node
        const spawnChildren = (parentNode) => {
            const parentId = parentNode.id;
            const parentData = parentNode.recdata;
            
            nodes.value = nodes.value.filter(n => n.parentId !== parentId);
            
            let childrenData = [];
            
            if (parentData) {
                if (parentData.styles && parentData.styles.length > 0) {
                    childrenData = parentData.styles.map((style, index) => ({
                        id: `${parentId}-style-${index}`,
                        name: style,
                        type: 'style'
                    }));
                } else if (parentData.extraits && parentData.extraits.length > 0) {
                    childrenData = parentData.extraits.map((extrait, index) => ({
                        id: `${parentId}-extrait-${index}`,
                        name: `Extrait ${index + 1}`,
                        data: extrait,
                        type: 'extrait'
                    }));
                }
            }
            
            childrenData.forEach((child, index) => {
                const angle = (index / childrenData.length) * 2 * Math.PI;
                const radius = 150;
                const parentPos = parentNode.position;
                
                nodes.value.push({
                    id: child.id,
                    recdata: child,
                    parentId: parentId,
                    position: {
                        x: parentPos.x + Math.cos(angle) * radius,
                        y: parentPos.y + Math.sin(angle) * radius
                    },
                    width: 160,
                    height: 60,
                    type: child.type
                });
            });
        };

        // Handle node actions (video playback, etc.)
        const handleNodeAction = (nodeData) => {
            console.log('Node action:', nodeData);
            
            if (nodeData.type === 'extrait') {
                const playbackData = {
                    extrait: nodeData.recdata,
                    selectionHistory: [...selectionHistory.value],
                    fullPath: getFullSelectionPath()
                };
                
                console.log('Video playback with history:', playbackData);
            }
        };

        // Get the full selection path as a readable string
        const getFullSelectionPath = () => {
            return selectionHistory.value.map(item => item.name).join(' → ');
        };

        // Clear selection history
        const clearSelectionHistory = () => {
            selectionHistory.value = [];
        };

        // Remove last selection from history
        const undoLastSelection = () => {
            if (selectionHistory.value.length > 0) {
                selectionHistory.value.pop();
                
                if (selectionHistory.value.length > 0) {
                    const lastSelection = selectionHistory.value[selectionHistory.value.length - 1];
                    currentPath.value = [0, lastSelection.id];
                } else {
                    currentPath.value = [0];
                }
            }
        };

        // Viewport controls
        const panViewport = (dx, dy) => {
            viewport.x += dx;
            viewport.y += dy;
        };

        const zoomViewport = (factor) => {
            viewport.scale *= factor;
        };

        const resetViewport = () => {
            viewport.x = 0;
            viewport.y = 0;
            viewport.scale = 1;
        };

        onMounted(() => {
            initializeNodes();
        });

        return {
            artistes,
            nodes,
            visibleNodes,
            links: visibleLinks,
            currentPath,
            selectionHistory,
            currentSelection,
            viewport,
            searchValue,
            handleNodeClick,
            clearSelectionHistory,
            undoLastSelection,
            getFullSelectionPath,
            panViewport,
            zoomViewport,
            resetViewport
        };
    },
    watch: {
        searchValue(newVal) {
            console.log("Search term changed:", newVal);
            // Implement search filtering if needed
        }
    }