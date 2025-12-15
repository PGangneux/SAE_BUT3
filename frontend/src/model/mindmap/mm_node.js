import Extrait from "../extrait.js";
import Interview from "../interview.js";
import mmch_CheminT from "./mm_chemin_submod/mmch_chemin.js";

export class mm_node {
    // Real/current positions (animating positions)
    x;           
    y;           
    // Target positions
    targetX;
    targetY;
    depth;
    childrens;
    origin_angle;
    category;
    content;
    loading;
    thumbnailUrl;
    mminfo; // Reference to mindmap instance

    /**
    * constructor for mindmap node
    * @param {mm_mindmap} mminfo mm_mindmap
    * @param {number} x x pos
    * @param {number} y y pos
    * @param {number} depth depth
    * @param {mmch_CheminT} category mindmap chemin class db category mmch_Artiste
    * @param {mmch_CheminT} content an instance with info of class category mmch_*
    */
    constructor(mminfo, x, y, depth, category, content) {
        this.mminfo = mminfo;
        // Both start at same position initially
        this.x = x;
        this.y = y;
        this.targetX = x;
        this.targetY = y;
        this.depth = depth;
        this.origin_angle = null;
        this.childrens = [];
        this.category = category;
        this.content = content;
        this.loading = false;
        this.thumbnailUrl = null;
    }

    toJSON() {
        return {
            x: this.x,
            y: this.y,
            targetX: this.targetX,
            targetY: this.targetY,
            depth: this.depth,
            childrens: this.childrens,
            origin_angle: this.origin_angle,
            category: this.category,
            content: this.content,
            loading: this.loading,
            thumbnailUrl: this.thumbnailUrl,
            // mminfo: this.mminfo
        };
    }

    isVideoContent() {
        return !!this.content && (this.category === Extrait || this.category === Interview);
    }

    // Get style for rendering (using x/y for smooth animation)
    getStyle() {
        // console.table(this.toJSON());

        const isVideoContent = this.isVideoContent();
        const nodeDimensions = isVideoContent ?
            { width: 300, height: 150 } : // Squircle dimensions
            { width: 100, height: 100 };  // Round dimensions

        const scaledWidth = nodeDimensions.width * this.mminfo.scale;
        const scaledHeight = nodeDimensions.height * this.mminfo.scale;
        const sizetext = 20 * this.mminfo.scale;

        // Calculate position - adjust for node center using x/y (real positions)
        const scaledX = (this.x * this.mminfo.scale) - (scaledWidth / 2);
        const scaledY = (this.y * this.mminfo.scale) - (scaledHeight / 2);

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
            if (this.category === Extrait) {
                return this.content.url_miniature_yt;
            }

            if (this.category != Interview) {
                throw new Error("unreachable mm_node category isn't Extrait or Interview in get_miniature");
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

    // Animate to target position
    animateToTarget(duration = 1000) {
        // TODO : TEST
        // this.childrens.forEach(child => {
        //     child.animateToTarget();
        // });

        // console.table(this.toJSON());
        
        const startX = this._x;
        const startY = this._y;
        const endX = this.targetX;
        const endY = this.targetY;
        const startTime = performance.now();

        const animate = (currentTime) => {
            
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const easeProgress = this.easeInOutCubic(progress);
            
            this.x = startX + (endX - startX) * easeProgress;
            this.y = startY + (endY - startY) * easeProgress;
            // console.log("animating",startX + (endX - startX) * easeProgress,startY + (endY - startY) * easeProgress,this);

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }
}