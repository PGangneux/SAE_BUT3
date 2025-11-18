import { markRaw } from 'vue';
import Artiste from "./artiste.js";
import Extrait from "./extrait.js";
import Interview from "./interview.js";
import Nation from "./nation.js";
import Question from "./question.js";
import StyleMusical from "./style_musical.js";
import Tag from "./tag.js";
import Theme from "./theme.js";
import { videoStore } from "./videoStore";
import router from "../router.js";

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
    loading;
    constructor(x, y, depth, category, content) {
        this.x = x;
        this.y = y;
        this.depth = depth;
        this.childrens = [];
        this.category = category;
        this.content = content;
        this.loading = false;
    }

    getStyle(scale, baseOffsetX, baseOffsetY) {
        const size = 100 * scale;
        const sizetext = 20 * scale;
        const scaledX = this.x * scale;
        const scaledY = this.y * scale;

        /// "width": size + "px",
        return {
            "background-color": LegendColorMap[this.category.name] || "#000000",
            "left": (scaledX + baseOffsetX) + "px",
            "top": (scaledY + baseOffsetY) + "px",
            "font-size": sizetext + "px",
            "line-height": size + "px",
        };
    }
}

// check video
function mmcheckvideo(vueobj){
    if (vueobj.chemin.length == 0) return;
    let last = vueobj.chemin[vueobj.chemin.length-1];
    if ((last.category == Extrait || last.category == Interview) && last.content){
        videoStore.uuid = last.content.uuid;
        vueobj.$router.push({ 
            path: "/lecteur_video/"
        });
        throw true;
    } 
    return
}

// pos the children of a node in a circle 
function set_children_pos(vueobj, root, origin_angle) {
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

// mmchemin_filter - filter chemin to maintain proper depth hierarchy
function mmchemin_filter(vueobj) {
    // console.log("before olders prune", vueobj.chemin);
    // Validate depth and handle depth mismatches
    if (mmcheckvideo(vueobj)) return true,false;
    let original_lenght = vueobj.chemin.length;
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
    let didchange = original_lenght != vueobj.chemin.length;
    vueobj.chemin = vueobj.chemin.filter(item => item.category !== mmRoot);
    // console.log("after olders prune", vueobj.chemin);
    return false , didchange;
}

// mmreset - recreate the root node and reset everything
function mmreset(vueobj) {
    // reset
    vueobj.nodes = [];
    vueobj.linkages = [];
    // create root
    let root = new mmNode(0, 0, 1, mmRoot, null);
    vueobj.nodes.push(markRaw(root));
    // put defaults
    for (const cat of categorys) {
        let tmp_child = new mmNode(0, 0, 2, cat, null);
        vueobj.nodes.push(markRaw(tmp_child));
        root.childrens.push({
            childnode: tmp_child,
            angle: null
        });
    }
    if (vueobj.searchval){
        for (const cat of [Question,Extrait,Interview]) {
        let tmp_child = new mmNode(0, 0, 2, cat, null);
        vueobj.nodes.push(markRaw(tmp_child));
        root.childrens.push({
            childnode: tmp_child,
            angle: null
        });
    }
    }
    // put default circle position + links
    set_children_pos(vueobj, root, null);
}

// mmget_chemin_from_root - return list of nodes from mmRoot to previous chemin node
function mmget_chemin_from_root(vueobj, chemin_node) {
    const path = [];
    let current_node = vueobj.nodes[0]; // start from root
    console.log("mmget_chemin_from_root chemin",vueobj.chemin);
    // Traverse through chemin to find the path to the target node
    for (let i = 0; i < vueobj.chemin.length; i++) {
        const current_chemin = vueobj.chemin[i];
        // Find the child that matches the current chemin element
        const childMatch = current_node.childrens.find(obj => {
            if (obj.childnode.category?.name !== current_chemin.category?.name) return false;
            if (current_chemin.content) {
                return obj.childnode.content?.uuid === current_chemin.content?.uuid;
            }
            return true;
        });
        console.log("mmget_chemin_from_root current_node",current_node);
        console.log("mmget_chemin_from_root childMatch",childMatch);
        if (childMatch) {
            path.push(childMatch);
            current_node = childMatch.childnode;
        } else {
            throw new Error("Path broken");
        }
    }
    return path;
}

export function mmdraw_root(vueobj) {
    mmreset(vueobj);
    let changevideo , changepath = mmchemin_filter(vueobj);
    if (changevideo) return;
    let path = mmget_chemin_from_root(vueobj, vueobj.chemin[vueobj.chemin.length - 1]);
    console.log("mmdraw_root chemin path",path);
    for (const cheminpath of path) {
        mmget_onecat(vueobj, cheminpath);
    }
}

export function mmdraw_update(vueobj) {
    if (vueobj.chemin.length <= 0) return mmdraw_root(vueobj);
    let changevideo , changepath = mmchemin_filter(vueobj);
    if (changevideo) return;
    if (changepath) return mmdraw_root(vueobj);
    const path = mmget_chemin_from_root(vueobj, vueobj.chemin[vueobj.chemin.length - 1]);
    console.log("mmdraw_update chemin path",path);
    mmget_onecat(vueobj, path[path.length - 1]);
}

function mmget_onecat(vueobj, cheminnode) {
    console.log("mmget_onecat",cheminnode);
    let node = cheminnode.childnode;
    let origin_angle = cheminnode.angle;

    // Get categories that are NOT in the current path
    const currentPathCategories = vueobj.chemin.map(item => item.category.name);
    const availableCategories = categorys.filter(cat =>
        !currentPathCategories.includes(cat.name)
    );

    if (node.content) {
        // Current node has content - add CATEGORY nodes
        console.log("Adding category nodes to content node");
        node.loading = true;
        for (const element of availableCategories) {
            let tmp_child = new mmNode(node.x, node.y, node.depth + 1, element, null);
            vueobj.nodes.push(markRaw(tmp_child));
            node.childrens.push({
                childnode: tmp_child,
                angle: null
            });
        }
        (vueobj.searchval ? Extrait.search(vueobj.searchval) : Extrait.list()).then(extraits => {
            for (let index = 0; index < extraits.length && index < 5 && node.childrens.length < 8; index++) {
                let tmp_child = new mmNode(node.x, node.y, node.depth + 1, Extrait, extraits[index]);
                vueobj.nodes.push(markRaw(tmp_child));
                node.childrens.push({
                    childnode: tmp_child,
                    angle: null
                });
            }
            set_children_pos(vueobj, node, origin_angle);
            node.loading = false;
        }).catch(error => {
            console.error("Error loading category list:", error);
            set_children_pos(vueobj, node, origin_angle);
            node.loading = false;
        });
    } else {
        // Current node is a category - add content nodes using category.list()
        node.loading = true;
        
        (vueobj.searchval ? node.category.search(vueobj.searchval) : node.category.list()).then(contentList => {
            console.log("getting detail from category", node.category, contentList);
            for (const element of contentList.slice(0, 5)) {
                let tmp_child = new mmNode(node.x, node.y, node.depth + 1, node.category, element);
                vueobj.nodes.push(markRaw(tmp_child));
                node.childrens.push({
                    childnode: tmp_child,
                    angle: null
                });
            }
            set_children_pos(vueobj, node, origin_angle);
            node.loading = false;
        }).catch(error => {
            console.error("Error loading category list:", error);
            set_children_pos(vueobj, node, origin_angle);
            node.loading = false;
        });
    }
}