import { markRaw } from 'vue';
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
    // console.log("set_children",root.childrens);
}

function mmreset(vueobj) {
    // reset
    vueobj.nodes = [];
    vueobj.linkages = [];
    // create root
    let root = new mmNode(0, 0, 1, mmRoot, null);
    vueobj.nodes.push(markRaw(root));
    // console.log("before olders prune", vueobj.chemin);
    // Validate depth and handle depth mismatches
    if (vueobj.chemin.length > 0) {
        let lastElement = vueobj.chemin[vueobj.chemin.length - 1];
        let minDepth = lastElement.depth;
        // console.log("minDepth chemin", minDepth);

        vueobj.chemin = vueobj.chemin.filter((element, index) => {
            // Always keep the last element
            if (index === vueobj.chemin.length - 1) return true;
            // Keep if depth is smaller
            if (element.depth < minDepth) {
                return true;
            } else {
                return false;
            }
        });
    }
    // Filter out mmRoot from chemin if present
    vueobj.chemin = vueobj.chemin.filter(item => item.category !== mmRoot);
    // console.log("after olders prune", vueobj.chemin);

    // put defaults
    for (const cat of categorys) {
        let tmp_child = new mmNode(0, 0, 2, cat, null);
        vueobj.nodes.push(markRaw(tmp_child));
        root.childrens.push({
            childnode: tmp_child,
            angle: null
        });
    }

    // put default circle position + links
    set_children(vueobj, root, null);
}

export function mmget(vueobj) {
    mmreset(vueobj);
    let current_node = vueobj.nodes[0]; // get root
    for (let indexchem = 0; indexchem < vueobj.chemin.length; indexchem++) {
        try {
            // Get categories that are NOT in the current path up to this index
            const currentPathCategories = vueobj.chemin.slice(0, indexchem + 1).map(item => item.category.name);
            const availableCategories = categorys.filter(cat =>
                !currentPathCategories.includes(cat.name)
            );
            // Find the child node that matches the current chemin element
            const cheminNode = vueobj.chemin[indexchem];
            // First filter by category
            const categoryMatches = current_node.childrens.filter(obj =>
                obj.childnode.category?.name === cheminNode.category?.name
            );
            console.log(`Category matches for ${cheminNode.category?.name}:`, categoryMatches);
            // Then filter by content.uuid if there is content
            let next;
            if (cheminNode.content) {
                // Look for exact match with content.uuid
                next = categoryMatches.find(obj =>
                    obj.childnode.content?.uuid === cheminNode.content?.uuid
                );
                console.log(`UUID match search:`, { 
                    lookingFor: cheminNode.content?.uuid,
                    found: next ? next.childnode.content?.uuid : 'none'
                });
            } else {
                // No content - take first category match
                next = categoryMatches[0];
                console.log(`No content - taking first category match:`, next);
            }
            console.log("whole chemin",vueobj.chemin);
            console.log("seelcted category",indexchem, vueobj.chemin[indexchem]);
            console.log("available cat", availableCategories);
            console.log("current_node", current_node);
            console.log("next", next);
            if (!next) throw new Error("no child node found in chemin");

            // Alternate based on CURRENT node type, not next node type
            if (next.childnode.content) {
                // Current node has content - add CATEGORY nodes
                console.log("Adding category nodes to content node");
                for (const element of availableCategories) {
                    let tmp_child = new mmNode(next.childnode.x + 100, next.childnode.y + 100, next.childnode.depth + 1, element, null);
                    vueobj.nodes.push(markRaw(tmp_child));
                    next.childnode.childrens.push({
                        childnode: tmp_child,
                        angle: null
                    });
                }
            } else {
                // Current node is a category - add content nodes using category.list()                
                const contentList = next.childnode.category.list().then(contentList => {
                    console.log("getting detail from category", next.childnode.category, contentList);
                    for (const element of contentList.slice(0, 5)) { // Limit to 5 items
                        let tmp_child = new mmNode(next.childnode.x + 100, next.childnode.y + 100, next.childnode.depth + 1, next.childnode.category, element);
                        vueobj.nodes.push(markRaw(tmp_child));
                        next.childnode.childrens.push({
                            childnode: tmp_child,
                            angle: null
                        });
                    }
                });
            }
            // Update positions for the new children
            set_children(vueobj, next.childnode, next.angle);
            current_node = next.childnode;
        } catch (error) {
            console.error("Error during path traversal:", error);
            throw error;
        }
    }
}

export function mmdelta(vueobj){
    
}