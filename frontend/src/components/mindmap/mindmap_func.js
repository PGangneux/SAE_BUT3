import Artiste from '../../model/artiste.js';
import Extrait from '../../model/extrait.js';
import Interview from '../../model/interview.js';
import Nation from '../../model/nation.js';
import Question from '../../model/question.js';
import StyleMusical from '../../model/style_musical.js';
import Tag from '../../model/tag.js';
import Theme from '../../model/theme.js';

export class mmRoot {
}

export const LegendColorMap = {
    'mmRoot': "#fff",
    'Artiste': "#A0522D",
    'Extrait': "#941C1C",
    'Interview': "#9747FF",
    'Nation': "#c24e00ff",
    'Question': "#FFCD06",
    'StyleMusical': "#010582",
    'Tag': "#02b360ff",
    'Theme': "#016969ff",
};

const categorys = [
    Artiste,
    Extrait,
    Interview,
    Nation,
    StyleMusical,
    Tag,
    Theme,
]

export class mmLinkage {
    startnode;
    endnode;
    thickness;

    constructor(startnode, endnode, thickness) {
        this.startnode = startnode;
        this.endnode = endnode;
        this.thickness = thickness;
    }

    get length() {
        return Math.sqrt(Math.pow(this.endnode.x - this.startnode.x, 2) + Math.pow(this.endnode.y - this.startnode.y, 2));
    }

    get angle() {
        return Math.atan2(this.endnode.y - this.startnode.y, this.endnode.x - this.startnode.x) * 180 / Math.PI;
    }

    getStyle(scale, baseOffsetX, baseOffsetY) {
        return {
            'height': (this.thickness * scale) + 'px',
            'width': (this.length * scale) + 'px',
            'left': (this.startnode.x + baseOffsetX) + 'px',
            'top': (this.startnode.y + baseOffsetY) + 'px',
            'transform': `rotate(${this.angle}deg)`,
        };
    }
}

export class mmNode {
    x;
    y;
    depth;
    parent;
    category;
    uuid;
    constructor(x, y, depth, parent, category, uuid) {
        this.x = x;
        this.y = y;
        this.depth = depth;
        this.parent = parent;
        this.category = category;
        this.uuid = uuid;
    }

    getStyle(scale, baseOffsetX , baseOffsetY ) {
        const size = 100 * scale; // Base size 100px multiplied by scale

        return {
            'background-color': LegendColorMap[this.category.name] || '#000000',
            'left': (this.x + baseOffsetX) + 'px',
            'top': (this.y + baseOffsetY) + 'px',
            'width': size + 'px',
            'height': size + 'px',
            'font-size': (16 * scale) + 'px',
            'line-height': size + 'px',
        };
    }
}

export async function mmget_all(nodelist, linkages) {
    let root = new mmNode(0,0,0,null,mmRoot,null);
    nodelist.push(root);
    nodelist.push(new mmNode(100, -300, 1, root, Artiste, null));
    linkages.push(new mmLinkage(root, nodelist[nodelist.length - 1], 1));
    nodelist.push(new mmNode(200, 0, 1, root, Extrait, null));
    linkages.push(new mmLinkage(root, nodelist[nodelist.length - 1], 1));
    nodelist.push(new mmNode(300, 0, 1, root, Interview, null));
    linkages.push(new mmLinkage(root, nodelist[nodelist.length - 1], 1));
    nodelist.push(new mmNode(0, 100, 1, root, Nation, null));
    linkages.push(new mmLinkage(root, nodelist[nodelist.length - 1], 1));
    nodelist.push(new mmNode(100, 100, 1, root, StyleMusical, null));
    linkages.push(new mmLinkage(root, nodelist[nodelist.length - 1], 1));
    nodelist.push(new mmNode(200, 100, 1, root, Tag, null));
    linkages.push(new mmLinkage(root, nodelist[nodelist.length - 1], 1));
    nodelist.push(new mmNode(300, 100, 1, root, Theme, null));
    linkages.push(new mmLinkage(root, nodelist[nodelist.length - 1], 1));
}

export function mmget(chemin){
    
}

export function mmsearch(obj, searchterm) {
    if (this.nodes[1]?.category.name != "question") {
        this.nodes.splice(1, 0, new mmNode(0, 0, 1, this.nodes[0], Question, null));
        linkages.push(new mmLinkage(nodelist[0], nodelist[1], 1));
    }
}