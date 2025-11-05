import Artiste from './artiste.js';
import Extrait from './extrait.js';
import Interview from './interview.js';
import Nation from './nation.js';
import Question from './question.js';
import StyleMusical from './style_musical.js';
import Tag from './tag.js';
import Theme from './theme.js';

class mmRoot {
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
    Nation,
    StyleMusical,
    Tag,
    Theme,
]

class mmLinkage {
    startnode;
    endnode;
    thickness;

    constructor(startnode, endnode, thickness) {
        this.startnode = startnode;
        this.endnode = endnode;
        this.thickness = thickness;
    }

    getlength(scale) {
        return Math.sqrt(Math.pow((this.endnode.x - this.startnode.x + 100 ) * scale, 2) + Math.pow((this.endnode.y - this.startnode.y +100 ) * scale, 2));
    }

    getangle() {
        return Math.atan2(this.endnode.y - this.startnode.y, this.endnode.x - this.startnode.x) * 180 / Math.PI;
    }

    getStyle(scale, baseOffsetX, baseOffsetY) {
        return {
            'height': (this.thickness * scale) + 'px',
            'width': (this.getlength(scale)) + 'px',
            'left': (this.startnode.x + baseOffsetX + 25) + 'px',
            'top': (this.startnode.y + baseOffsetY + 25) + 'px',
            'transform': `rotate(${this.getangle(scale)}deg)`,
        };
    }
}

class mmNode {
    x;
    y;
    depth;
    childrens;
    category;
    uuid;
    constructor(x, y, depth, category, uuid) {
        this.x = x;
        this.y = y;
        this.depth = depth;
        this.childrens = [];
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

function set_children(obj,root,origin_angle){
    // failsafe , si pas enfant
    if (!root.childrens.length) return;
    // distance entre root et enfant ;
    // on a un cercle de 360° , et on doit divisier ca par le nombre d'enfants (moins le trait d'origine) 
    let nb_child = root.childrens.length + (!! origin_angle ? 2 : 0);
    let angle_per_child = (360 / nb_child);
    // so the distance is inversly proportional to the number of angle_per_child
    let distance = (1/angle_per_child) * 100 + 30;
    // we iterate over an angle
    let current_angle = origin_angle || 0;
    for (let index = 0; index < root.childrens.length; index++) {
        const child = root.childrens[index].childnode;
        child.x = root.x + Math.cos(current_angle) * distance;
        child.y = root.y + Math.sign(current_angle) * distance;
        root.childrens[index].angle = current_angle;
        // create link
        obj.linkages.push(new mmLinkage(root,child,(1/obj.chemin.length)*root.depth*2));
        // advance the angle
        current_angle += angle_per_child ;
    }
}

export function mmget(obj){
    // reset
    obj.nodes = [];
    obj.linkages = [];
    // create root
    let root = new mmNode(0,0,0,mmRoot,null);
    obj.nodes.push(root);
    // put defaults
    for (const cat of categorys) {
        // so for each cat in the default categorys
        // create a "root" category buble
        let tmp_child = new mmNode(0,0,1,cat,null);
        // render it
        obj.nodes.push(tmp_child);
        // they are children of the white root node
        root.childrens.push({
                childnode :tmp_child,
                angle : null
            });
    }
    // put default cercle position + links
    set_children(obj,root,null);
    let current_node = root;
    for (const child of obj.chemin) {
        // let next = current_node.childrens. [obj => obj.category == child] ;
    }
    console.log(root);
}