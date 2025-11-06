import Artiste from "../../model/artiste.js";
import Extrait from "../../model/extrait.js";
import Interview from "../../model/interview.js";
import Nation from "../../model/nation.js";
import Question from "../../model/question.js";
import StyleMusical from "../../model/style_musical.js";
import Tag from "../../model/tag.js";
import Theme from "../../model/theme.js";
import router from "../../router.js";

class mmRoot {
}

export const LegendClassMap = {
    "Artiste": "Artiste",
    "Extrait": "Extrait",
    "Interview": "Interview",
    "Nation": "Pays",
    "Question": "Question",
    "StyleMusical": "Style Musical",
    "Tag": "Tag",
    "Theme": "Thème",
}

export const LegendColorMap = {
    "mmRoot": "#fff",
    "Artiste": "#A0522D",
    "Extrait": "#941C1C",
    "Interview": "#9747FF",
    "Nation": "#c24e00ff",
    "Question": "#FFCD06",
    "StyleMusical": "#010582",
    "Tag": "#02b360ff",
    "Theme": "#016969ff",
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
            "transform-origin": "0 50%",
        };
    }
}

export class mmNode {
    x;
    y;
    depth;
    childrens;
    category;
    content;
    constructor(x, y, depth, category, content) {
        this.x = x;
        this.y = y;
        this.depth = depth;
        this.childrens = [];
        this.category = category;
        this.content = content;
    }

    getStyle(scale, baseOffsetX, baseOffsetY) {
        const size = 100 * scale;
        const sizetext = 20 * scale;
        const scaledX = this.x * scale;
        const scaledY = this.y * scale;

        return {
            "background-color": LegendColorMap[this.category.name] || "#000000",
            "left": (scaledX + baseOffsetX) + "px",
            "top": (scaledY + baseOffsetY) + "px",
            "width": size + "px",
            "height": size + "px",
            "font-size": sizetext + "px",
            "line-height": size + "px",
        };
    }
}

function set_children(vueobj, root, origin_angle) {
    // failsafe , si pas enfant
    if (!root.childrens.length) return;
    // distance entre root et enfant ;
    // on a un cercle de 360° , et on doit divisier ca par le nombre d"enfants (moins le trait d"origine) 
    let nb_child = root.childrens.length + (origin_angle ? 2 : 0);
    let angle_per_child = (360 / nb_child);
    // so the distance is inversly proportional to the number of angle_per_child
    let taille_max_node = 300; // TODO : compute that 
    let distance = taille_max_node + (1 / angle_per_child) * taille_max_node;
    // we iterate over an angle
    let current_angle = origin_angle || 0;
    let thickness_base = (vueobj.chemin.length + 1) * 3;
    let base_rootx = root.x - 25 * vueobj.scale;
    let base_rooty = root.y - 25 * vueobj.scale;
    for (let index = 0; index < root.childrens.length; index++) {
        const child = root.childrens[index].childnode;
        const angleRad = current_angle * Math.PI / 180;

        child.x = base_rootx + Math.cos(angleRad) * distance;
        child.y = base_rooty + Math.sin(angleRad) * distance;
        root.childrens[index].angle = current_angle;
        // create link
        // console.log("thicness",vueobj.chemin.length,root.depth,thickness_base,thickness_base * (1 / root.depth));
        vueobj.linkages.push(new mmLinkage(root, child, thickness_base * (1 / root.depth)));
        // advance the angle
        current_angle += angle_per_child;
    }
}

export function mmget(vueobj) {
    // reset
    vueobj.nodes = [];
    vueobj.linkages = [];
    // create root
    let root = new mmNode(0, 0, 1, mmRoot, null);
    vueobj.nodes.push(root);
    // put defaults
    for (const cat of categorys) {
        // so for each cat in the default categorys
        // create a "root" category buble
        let tmp_child = new mmNode(0, 0, 2, cat, null);
        // render it
        vueobj.nodes.push(tmp_child);
        // they are children of the white root node
        root.childrens.push({
            childnode: tmp_child,
            angle: null
        });
    }
    // put default cercle position + links
    set_children(vueobj, root, null);
    let current_node = root;
    try {
        for (const child of vueobj.chemin) {
            let next = current_node.childrens.find(obj => obj.childnode === child);

            if (next) {
                current_node = child;
                
                // Filter out categories that are already in the chemin path
                // const availableCategories = categorys.filter(elem => !vueobj.chemin.category.includes(elem));
                
                // Add available categories as children
                for (const element of categorys) {
                    let tmp_child = new mmNode(0, 0, current_node.depth + 1, element, null);
                    vueobj.nodes.push(tmp_child);
                    current_node.childrens.push({
                        childnode: tmp_child,
                        angle: null
                    });
                }
                
                // Update positions for the new children
                set_children(vueobj, current_node, null);
                
            } else {
                console.warn(`Child node with category "${child}" not found`);
                break;
            }
        }
    } catch (error) {
        console.error("Error during path traversal:", error);
        throw error;
    }
    // console.log(root);
}