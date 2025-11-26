import { markRaw } from "vue";
import { mmRoot, mmCategorysDefault, mmCategorysSearch, mmLinkage, mmNode, mmInfo } from "./mindmap_base.js";
import Extrait from "../extrait.js";
import Interview from "../interview.js";
import router from "../../router.js";

/**
    check video
 * @param {mmInfo} mminfo mminfo  
 * @return {boolean} if there is a goto video or not
*/
function mmcheckvideo(mminfo) {
    if (mminfo.chemin.length == 0) return false;
    let last = mminfo.chemin[mminfo.chemin.length - 1];
    if (last.category == Extrait && last.content){
        mminfo.extrait_current.set(last.content);
        router.push({
            path: "/lecteur_video/"
        });
        return true;
    } else if (last.category == Interview && last.content){
        mminfo.interview_current.set(last.content);
        router.push({
            path: "/lecteur_video/"
        });
        return true;
    }
    return false;
}

/**
    pos the children of a node in a circle
 * @param {mmInfo} mminfo mminfo  
    @param {mmNode} root the root node to witch the children has been added
 * @return {boolean} if there is a goto video or not
*/
function set_children_pos(mminfo, root) {
    // failsafe , si pas enfant
    if (!root.childrens.length) return;
    // distance entre root et enfant ;
    // on a un cercle de 360° , et on doit divisier ca par le nombre d"enfants (moins le trait d"origine) 
    let nb_child = root.childrens.length + (root.origin_angle ? 2 : 0);
    let angle_per_child = (360 / nb_child);
    // so the distance is inversly proportional to the number of angle_per_child
    let taille_max_node = 300; // TODO : compute that 
    let distance = taille_max_node + (1 / angle_per_child) * taille_max_node;
    // we iterate over an angle
    let current_angle = root.origin_angle || 0;
    let base_rootx = root.x - 25 * mminfo.scale;
    let base_rooty = root.y - 25 * mminfo.scale;
    for (let index = 0; index < root.childrens.length; index++) {
        const child = root.childrens[index];
        const angleRad = current_angle * Math.PI / 180;

        child.x = base_rootx + Math.cos(angleRad) * distance;
        child.y = base_rooty + Math.sin(angleRad) * distance;
        root.childrens[index].angle = current_angle;
        // create link
        // console.log("thicness",mminfo.chemin.length,root.depth,thickness_base,thickness_base * (1 / root.depth));
        // advance the angle
        current_angle += angle_per_child;
    }
    // console.log("set_children",root.childrens);
}

/**
    filter chemin to maintain proper depth hierarchy
 * @param {mmInfo} mminfo mminfo  
 * @return {boolean,boolean} change goto video , change in path
*/
function mmchemin_filter(mminfo) {
    // Validate depth and handle depth mismatches
    if (mmcheckvideo(mminfo)) return true, false;
    let original_lenght = mminfo.chemin.length;
    if (mminfo.chemin.length > 0) {
        let lastElement = mminfo.chemin[mminfo.chemin.length - 1];
        let minDepth = lastElement.depth;
        mminfo.chemin = mminfo.chemin.filter((element, index) => {
            // Always keep the last element
            if (index === mminfo.chemin.length - 1) return true;
            // Keep if depth is smaller
            if (element.depth < minDepth) {
                return true;
            } else {
                return false;
            }
        });
    }
    // Filter out mmRoot from chemin if present
    let didchange = original_lenght != mminfo.chemin.length;
    mminfo.chemin = mminfo.chemin.filter(item => item.category !== mmRoot);
    return false, didchange;
}

/**
    recreate the root node and reset everything
 * @param {mmInfo} mminfo mminfo  
*/
function mmreset(mminfo) {
    // reset
    mminfo.nodes = [];
    mminfo.linkages = [];
    // create root
    let root = new mmNode(0, 0, 1, null, mmRoot, null);
    mminfo.nodes.push(root);
    let thickness_base = (mminfo.chemin.length + 1) * 3;

    // put defaults
    for (const cat of mmCategorysDefault) {
        let tmp_child = new mmNode(0, 0, 2, 0, cat, null);
        mminfo.nodes.push(markRaw(tmp_child));
        root.childrens.push(markRaw(tmp_child));
        mminfo.linkages.push(new mmLinkage(root, tmp_child, thickness_base * (1 / root.depth)));

        // put default circle position + links
        set_children_pos(mminfo, root);
    }
    if (mminfo.searchval) {
        for (const cat of mmCategorysSearch) {
            let tmp_child = new mmNode(0, 0, 2, 0, cat, null);
            mminfo.nodes.push(markRaw(tmp_child));
            root.childrens.push(markRaw(tmp_child));
            mminfo.linkages.push(new mmLinkage(root, tmp_child, thickness_base * (1 / root.depth)));

            set_children_pos(mminfo, root);
        }
    }
}

/**
    redraw everynode from root
 * @param {mmInfo} mminfo mminfo  
*/
export function mmdraw_root(mminfo) {
    mmreset(mminfo);
    let changevideo, changepath = mmchemin_filter(mminfo);
    if (changevideo) return;
    console.log("mmdraw_root chemin path", mminfo.chemin);
    for (const cheminpath of mminfo.chemin) {
        mmget_onecat(mminfo, cheminpath);
    }
}

/**
    redraw an update
 * @param {mmInfo} mminfo mminfo  
*/
export function mmdraw_update(mminfo) {
    if (mminfo.chemin.length <= 0) return mmdraw_root(mminfo);
    let changevideo, changepath = mmchemin_filter(mminfo);
    if (changevideo) return;
    if (changepath) return mmdraw_root(mminfo);
    console.log("mmdraw_update chemin path", mminfo.chemin);
    mmget_onecat(mminfo, mminfo.chemin[mminfo.chemin.length - 1]);
}

function mmget_onecat(mminfo, cheminnode) {
    console.log("mmget_onecat", cheminnode);
    let node = cheminnode;
    let thickness_base = (mminfo.chemin.length + 1) * 3;

    // Get categories that are NOT in the current path
    const currentPathCategories = mminfo.chemin.map(item => item.category.name);
    const availableCategories = mmCategorysDefault.filter(cat =>
        !currentPathCategories.includes(cat.name)
    );

    if (node.content) {
        // Current node has content - add CATEGORY nodes
        console.log("Adding category nodes to content node");
        node.loading = true;
        // TODO : use mmCheminMap
        for (const element of availableCategories) {
            let tmp_child = new mmNode(node.x, node.y, node.depth + 1, 0, element, null);
            mminfo.nodes.push(markRaw(tmp_child));
            node.childrens.push(markRaw(tmp_child));
            mminfo.linkages.push(new mmLinkage(node, tmp_child, thickness_base * (1 / node.depth)));

            set_children_pos(mminfo, node);
        }
        (mminfo.searchval ? Extrait.search(mminfo.searchval) : Extrait.list()).then(extraits => {
            for (let index = 0; index < extraits.length && index < 5 && node.childrens.length < 8; index++) {
                let tmp_child = new mmNode(node.x, node.y, node.depth + 1, 0, Extrait, extraits[index]);
                mminfo.nodes.push(markRaw(tmp_child));
                node.childrens.push(markRaw(tmp_child));
                mminfo.linkages.push(new mmLinkage(node, tmp_child, thickness_base * (1 / node.depth)));

                set_children_pos(mminfo, node);
            }
            node.loading = false;
        }).catch(error => {
            console.error("Error loading category list:", error);
            set_children_pos(mminfo, node);
            node.loading = false;
        });
    } else {
        // Current node is a category - add content nodes using category.list()
        node.loading = true;

        (mminfo.searchval ? node.category.search(mminfo.searchval) : node.category.list()).then(contentList => {
            console.log("getting detail from category", node.category, contentList);
            for (const element of contentList.slice(0, 5)) {
                let tmp_child = new mmNode(node.x, node.y, node.depth + 1, 0, node.category, element);
                mminfo.nodes.push(markRaw(tmp_child));
                node.childrens.push(markRaw(tmp_child));
                mminfo.linkages.push(new mmLinkage(node, tmp_child, thickness_base * (1 / node.depth)));

                set_children_pos(mminfo, node);
            }
            node.loading = false;
        }).catch(error => {
            console.error("Error loading category list:", error);
            set_children_pos(mminfo, node);
            node.loading = false;
        });
    }
}