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
 * pos the children of a node in a circle
 * @param {mmInfo} mminfo mminfo  
 * @param {mmNode} root the root node to witch the children has been added
 */
function set_children_pos(mminfo, root) {
    // failsafe , si pas enfant
    if (!root.childrens.length) return;
    // est ce que c'est mmroot ou pas 
    const isRoot = root.category == mmRoot;
    const totalArc = isRoot ? 360 : 160; // Full circle for root, semicircle for others
    const nb_child = root.childrens.length;
    // distance entre root et enfant ;
    let angle_per_child = totalArc / nb_child;
    // so the distance is inversly proportional to the number of angle_per_child
    const depthFactor = Math.max(0.7, 1 / root.depth); // Reduce distance as depth increases
    const spreadFactor = Math.max(1,nb_child * 0.5); // Slightly increase distance for more children
    const distance = 200 * mminfo.scale * depthFactor * spreadFactor;

    // Calculate starting position - centered on origin_angle
    let start_angle = isRoot ? 0 : root.origin_angle - (totalArc / 2) + (angle_per_child / 2);
    const degree_to_rad = Math.PI / 180;
    for (let index = 0; index < root.childrens.length; index++) {
        const child = root.childrens[index];
        const current_angle = start_angle + (angle_per_child * index);
        const angleRad = current_angle * degree_to_rad;

        child.x = root.x + Math.cos(angleRad) * distance;
        child.y = root.y + Math.sin(angleRad) * distance;
        child.origin_angle = current_angle;

        console.table({
        Child: index + 1,
        Angle: `${current_angle.toFixed(1)}°`,
        Position: `(${child.x.toFixed(2)}, ${child.y.toFixed(2)})`,
        Distance: distance,
        Origin: `(${root.x}, ${root.y})`
    });
    }
    console.log(`Positioned ${nb_child} children from ${root.origin_angle} around ${isRoot ? 'root' : root.category.name} distance ${distance} at depth ${root.depth}, arc: ${angle_per_child*nb_child}°/${angle_per_child}°`);
    console.log(root);
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
    utils to create a child node
 * @param {mmInfo} mminfo mminfo  
 * @param {mmNode} node the parent node  
 * @param {class} category the class of node  
 * @param {class} content the content instance of class category
 * @param {boolean} createLink = true do we draw the white line or not
 * @return {mmNode} the created child
*/
function mmcreateChildNode(mminfo, node , category ,content  , createLink = true) {
    const thickness_base = (mminfo.chemin.length + 1) * 3;
    const tmp_child = new mmNode(node.x, node.y, node.depth + 1, category, content);
    mminfo.nodes.push(markRaw(tmp_child));
    node.childrens.push(markRaw(tmp_child));
    // console.log("thicness",mminfo.chemin.length,root.depth,thickness_base,thickness_base * (1 / root.depth));
    if (createLink){
        mminfo.linkages.push(new mmLinkage(node, tmp_child, thickness_base * (1 / node.depth)));
    }
    set_children_pos(mminfo, node);
    return tmp_child;
}

/**
    recreate the root node and reset everything
 * @param {mmInfo} mminfo mminfo  
*/
function mmreset(mminfo) {
    console.log("mmreset mminfo",mminfo);
    
    // reset
    mminfo.nodes = [];
    mminfo.linkages = [];
    // create root
    let root = new mmNode(0, 0, 1, mmRoot, null);
    mminfo.nodes.push(root);
    
    // put defaults
    for (const cat of mmCategorysDefault) {
        mmcreateChildNode(mminfo,root,cat,null,false);
    }
    if (mminfo.searchval) {
        for (const cat of mmCategorysSearch) {
            mmcreateChildNode(mminfo,root,cat,null,false);
        }
    }
}

/**
    redraw everynode from root
 * @param {mmInfo} mminfo mminfo  
*/
export async function mmdraw_root(mminfo) {
    mmreset(mminfo);
    let changevideo, changepath = mmchemin_filter(mminfo);
    if (changevideo) return;
    console.log("mmdraw_root chemin path", mminfo.chemin);
    for (const cheminpath of mminfo.chemin) {
        await mmget_onecat(mminfo, cheminpath);
    }
}

/**
    redraw an update
 * @param {mmInfo} mminfo mminfo  
*/
export async function mmdraw_update(mminfo) {
    if (mminfo.chemin.length <= 0) return mmdraw_root(mminfo);
    let changevideo, changepath = mmchemin_filter(mminfo);
    if (changevideo) return;
    if (changepath) return mmdraw_root(mminfo);
    console.log("mmdraw_update chemin path", mminfo.chemin);
    await mmget_onecat(mminfo, mminfo.chemin[mminfo.chemin.length - 1]);
}

async function mmget_onecat(mminfo, node) {
    console.log("mmget_onecat", node);

    // failsafe videonode
    // normally we should have goto video before
    if (node.content && (node.category.name === 'Extrait' || node.category.name === 'Interview')) return;
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
        for (const cat of availableCategories) {
            mmcreateChildNode(mminfo,node,cat,null);
            // await new Promise(resolve => { setTimeout(resolve, 1000); });
        }
        (mminfo.searchval ? Extrait.search(mminfo.searchval) : Extrait.list()).then(async extraits => {
            for (let index = 0; index < extraits.length && index < 5 && node.childrens.length < 8; index++) {
                mmcreateChildNode(mminfo,node,Extrait,extraits[index]);
                // await new Promise(resolve => { setTimeout(resolve, 1000); });
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

        (mminfo.searchval ? node.category.search(mminfo.searchval) : node.category.list()).then(async contentList => {
            // console.log("getting detail from category", node.category, contentList);
            for (const element of contentList.slice(0, 5)) {
                mmcreateChildNode(mminfo,node,node.category,element);
                // await new Promise(resolve => { setTimeout(resolve, 1000); });
            }
            node.loading = false;
        }).catch(error => {
            console.error("Error loading category list:", error);
            set_children_pos(mminfo, node);
            node.loading = false;
        });
    }
}