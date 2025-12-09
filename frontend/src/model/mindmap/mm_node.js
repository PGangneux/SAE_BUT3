export class mm_node {
    x;           // Target X position
    y;           // Target Y position
    reelx;       // Current/animating X position
    reely;       // Current/animating Y position
    depth;
    childrens;
    origin_angle;
    category;
    content;
    loading;
    thumbnailUrl;
    mminfo; // Reference to mindmap instance

    constructor(mminfo,x, y, depth, category, content) {
        this.mminfo = mminfo;
        this.x = x;
        this.y = y;
        this.reelx = x; // Start at target position
        this.reely = y; // Start at target position
        this.depth = depth;
        this.origin_angle = null;
        this.childrens = [];
        this.category = category;
        this.content = content;
        this.loading = false;
        this.thumbnailUrl = null;
    }

    // Get style for rendering (using reelx/reely for smooth animation)
    getStyle() {
        if (!this.mminfo) return {};
        
        const isVideoContent = this.isVideoContent();
        const nodeDimensions = isVideoContent ? 
            { width: 300, height: 150 } : // Squircle dimensions
            { width: 100, height: 100 };  // Round dimensions
        
        const scaledWidth = nodeDimensions.width * this.mminfo.scale;
        const scaledHeight = nodeDimensions.height * this.mminfo.scale;
        const sizetext = 20 * this.mminfo.scale;
        
        // Calculate position - adjust for node center using reelx/reely
        const scaledX = (this.reelx * this.mminfo.scale) - (scaledWidth/16);
        const scaledY = (this.reely * this.mminfo.scale) - (scaledHeight/16);
        
        return {
            "left": (scaledX + this.mminfo.offx) + "px",
            "top": (scaledY + this.mminfo.offy) + "px",
            "width": scaledWidth + "px",
            "height": scaledHeight + "px",
            "font-size": sizetext + "px",
            "line-height": (scaledHeight * 0.8) + "px",
        };
    }

    // Get thumbnail URL
    async get_miniature() {
        if (!this.content) return null;
        if (this.thumbnailUrl) return this.thumbnailUrl;

        try {
            // Case 1: It's an extract
            if (this.category.name === 'Extrait') {
                return this.content.url_miniature_yt;
            }

            // Case 2: It's an interview
            const extraits = await this.content.extraits();
            if (!extraits || extraits.length === 0) {
                console.warn(`Aucun extrait trouvé pour l'interview ${this.content}`);
                return null;
            }

            const firstExtrait = extraits[0];
            return firstExtrait.url_miniature_yt;

        } catch (err) {
            console.error("Erreur lors de la récupération de la miniature :", err);
            return null;
        }
    }

    // Load thumbnail
    async loadThumbnail() {
        if (!this.isVideoContent() || this.thumbnailLoading) return;
        
        this.thumbnailLoading = true;
        try {
            this.thumbnailUrl = await this.get_miniature();
        } catch (error) {
            console.error(error);
        } finally {
            this.thumbnailLoading = false;
        }
    }

    // Animate to target position
    animateToTarget(duration = 1000) {
        const startX = this.reelx;
        const startY = this.reely;
        const targetX = this.x;
        const targetY = this.y;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Use cubic easing
            const easeProgress = this.easeInOutCubic(progress);
            
            // Update reel positions
            this.reelx = startX + (targetX - startX) * easeProgress;
            this.reely = startY + (targetY - startY) * easeProgress;
            
            // Continue animation if not complete
            requestAnimationFrame(animate);
        };
        
        requestAnimationFrame(animate);
    }

    // Cubic easing function
    easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }
}