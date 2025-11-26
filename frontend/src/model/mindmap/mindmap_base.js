import Artiste from "../artiste.js";
import Extrait from "../extrait.js";
import Interview from "../interview.js";
import Nation from "../nation.js";
import Question from "../question.js";
import StyleMusical from "../style_musical.js";
import Tag from "../tag.js";
import Theme from "../theme.js";

export class mmRoot {
}

export const mmLegendClassMap = {
    "Artiste": "Artiste",
    "Extrait": "Extrait",
    "Interview": "Interview",
    "Nation": "Pays",
    "Question": "Question",
    "StyleMusical": "Style Musical",
    "Tag": "Tag",
    "Theme": "Thème",
}

export const mmCategorysDefault = [
    Artiste,
    Nation,
    StyleMusical,
    Tag,
    Theme,
]

export const mmCategorysSearch = [
    Question,
    Extrait,
    Interview
]

export const mmCheminMap = {
    Artiste: [],
    Extrait: [],
    Interview: [],
    Nation: [],
    Question: [],
    StyleMusical: [],
    Tag: [],
    Theme: [],
}

export class mmLinkage {
    startnode;
    endnode;
    thickness;

    constructor(startnode, endnode, thickness) {
        this.startnode = startnode;
        this.endnode = endnode;
        this.thickness = thickness;
    }

    getStyle(scale, baseOffsetX, baseOffsetY) {
        const scaledStartX = this.startnode.x * scale;
        const scaledStartY = this.startnode.y * scale;
        const scaledEndX = this.endnode.x * scale;
        const scaledEndY = this.endnode.y * scale;

        const length = Math.sqrt(Math.pow(scaledEndX - scaledStartX, 2) + Math.pow(scaledEndY - scaledStartY, 2));
        const angle = Math.atan2(scaledEndY - scaledStartY, scaledEndX - scaledStartX) * 180 / Math.PI;

        return {
            "height": (this.thickness * scale) + "px",
            "width": length + "px",
            "left": (scaledStartX + baseOffsetX + 50 * scale) + "px", // 50 * scale to center (half of node size)
            "top": (scaledStartY + baseOffsetY + 50 * scale) + "px", // 50 * scale to center
            "transform": `rotate(${angle}deg)`,
            "transform-origin": "0 50%", // TOOD : put in css
        };
    }
}

export class mmNode {
    x;
    y;
    depth;
    childrens;
    origin_angle;
    category;
    content;
    loading;
    constructor(x, y, depth, origin_angle, category, content) {
        this.x = x;
        this.y = y;
        this.depth = depth;
        this.origin_angle = origin_angle;
        this.childrens = [];
        this.category = category;
        this.content = content;
        this.loading = false;
    }
}

export class mmInfo {
    linkages;
    nodes;
    chemin;
    previewnodes;
    fullscreen;
    togglelegend;
    scale;
    offx;
    offy;
    lastMouseX;
    lastMouseY;
    clickTimer;
    dragging;
    searchval;

    interview_current;
    extrait_current;
    constructor(interview_current,extrait_current) {
        this.linkages = [];
        this.nodes = [];
        this.chemin = [];
        this.previewnodes = [];
        this.fullscreen = false;
        this.togglelegend = true;
        this.scale = 1;
        this.offx = 0;
        this.offy = 0;
        this.lastMouseX = 0;
        this.lastMouseY = 0;
        this.clickTimer = null;
        this.dragging = false;
        this.searchval = "";

        this.interview_current = interview_current;
        this.extrait_current = extrait_current;
    }
}