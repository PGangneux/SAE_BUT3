import { markRaw } from "vue";
import router from "../../router.js";
import Model from "../model.js";
import mm_Mindmap from "./mm_mindmap.js";
import mm_Linkage from "./mm_linkage.js";
import mmch_CheminT from "./mm_chemin_submod/mmch_chemin.js";
import mmch_Root from "./mm_chemin_submod/mmch_root.js";
import mmch_Extrait from "./mm_chemin_submod/mmch_extrait.js";
import mmch_Interview from "./mm_chemin_submod/mmch_interview.js";

/**
    check video
 * @param {mm_Mindmap} mminfo mm_mindmap  
 * @return {boolean} if there is a goto video or not
*/
export function mm_checkvideo(mminfo) {
    if (mminfo.chemin.length == 0) return false;
    let last = mminfo.chemin[mminfo.chemin.length - 1];
    if (!!last) return false;
    if (last.category == mmch_Extrait && last.category.mmch_obj) {
        mminfo.extrait_current.set(last.category);
        router.push({
            path: "/lecteur_video/"
        });
        return true;
    } else if (last.category == mmch_Interview && last.category.mmch_obj) {
        mminfo.interview_current.set(last.category);
        router.push({
            path: "/lecteur_video/"
        });
        return true;
    }
    return false;
}

/**
    filter chemin to maintain proper depth hierarchy
 * @param {mm_Mindmap} mminfo mm_mindmap  
 * @return {boolean,boolean} change goto video , change in path
*/
export function mm_chemin_filter(mminfo) {
    // Validate depth and handle depth mismatches
    if (mm_checkvideo(mminfo)) return true, false;
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
    // Filter out mm_Root from chemin if present
    let didchange = original_lenght != mminfo.chemin.length;
    mminfo.chemin = mminfo.chemin.filter(item => item.category !== mmch_Root);
    return false, didchange;
}

/**
 * clear the preview nodes and linkages
 * @param {mm_Mindmap} mminfo mm_mindmap  
 * @return {boolean,boolean} change goto video , change in path
*/
export function mm_clean_preview(mminfo){
    mminfo.previewlinkages = [];
    for (let pparent of mminfo.chemin.at(-2).childrens){
        for (let pnode of pparent.childrens){
            if (pnode.ispreview){
                let pindex = pparent.childrens.indexOf(pnode);
                if (pindex == -1) console.warn("index of preview node not found in parent childrens");
                delete pparent.childrens[pindex];
            }
        }
    }
}   

/**
    utils to create a child node
 * @param {mm_Mindmap} mminfo mm_Mindmap  
 * @param {mmch_CheminT} node the parent node  
 * @param {mmch_CheminT} category the class of node  
 * @param {Model} content the content of the node  
 * @param {boolean} createLink = true do we draw the white line or not
 * @param {boolean} isPreview = false whether this is a preview node
 * @return {mmch_CheminT} the created child
*/
export function mm_createChildNode(mminfo, node, category,content=null, createLink = true, isPreview = false) {
    const thickness_base = (mminfo.chemin.length + 1) * 3;
    const tmp_child = new category(mminfo, node.x, node.y, node.depth + 1,content);
    node.childrens.push(markRaw(tmp_child));
    if (isPreview){
        mminfo.previewnodes.push(markRaw(tmp_child));
        node.ispreview = true;
    } else {
        mminfo.nodes.push(markRaw(tmp_child));
    }
    if (createLink) {
        const linkage = new mm_Linkage(node, tmp_child, thickness_base * (1 / node.depth));
        if (isPreview) {
            mminfo.previewlinkages.push(linkage);
        } else {
            mminfo.linkages.push(linkage);
        }
    }
    set_children_pos(mminfo, node);
    return tmp_child;
}

/**
 * pos the children of a node in a circle
 * @param {mm_Mindmap} mminfo mm_Mindmap  
 * @param {mmch_CheminT} root the root node to witch the children has been added
 */
export function set_children_pos(mminfo, root) {
    // failsafe , si pas enfant
    if (!root.childrens.length) return;

    // est ce que c'est mm_Root ou pas 
    const isRoot = root.category == mmch_Root;
    const totalArc = isRoot ? 360 : 160; // Full circle for root, semicircle for others
    const nb_child = root.childrens.length;

    // Count children with and without content (mmch_obj)
    let childrenWithPreview = 0;
    let childrenWithContent = 0;
    let childrenWithoutContent = 0;

    for (let child of root.childrens) {
        if (child.category.mmch_hasMiniature()) {
            childrenWithPreview++;
        } else if (child.category.mmch_obj) {
            childrenWithContent++;
        } else {
            childrenWithoutContent++;
        }
    }

    // Calculate angle per child based on content
    // Children with content get 1.2x more angle space
    const effectiveChildren = childrenWithPreview * 1.4 + childrenWithContent * 1.2 + childrenWithoutContent;
    const angle_per_child = totalArc / effectiveChildren;

    // Check if all children already have origin_angle set with consistent spacing
    if (root.childrens.length > 1) {
        let allAnglesSet = true;
        
        for (let child of root.childrens) {
            if (child.origin_angle === null || child.origin_angle === undefined) {
                allAnglesSet = false;
                break;
            }
        }
        
        // If all angles are set, check spacing consistency
        if (allAnglesSet) {
            // Calculate expected spacing between consecutive children
            // We need to account for content weighting, so we check each pair
            let spacing_ok = false;
            let root_angle = root.childrens.origin_angle;
            if (root.childrens[1].category.mmch_hasMiniature()){
                if (root_angle - root.childrens[0].origin_angle - angle_per_child * 1.4 < 5){
                    spacing_ok = true;
                }
            } else if (root.childrens[1].category.mmch_obj){
                if (root_angle - root.childrens[0].origin_angle - angle_per_child * 1.2 < 5){
                    spacing_ok = true;
                }
            } else {
                if (root_angle - root.childrens[0].origin_angle - angle_per_child < 5){
                    spacing_ok = true;
                }
            }
            if (spacing_ok) return; // spacing consistent, no need to recalculate
        }
    } 
    // If we reach here, we need to recalculate positions
    
    // distance entre root et enfant ;
    // so the distance is inversly proportional to the number of angle_per_child
    const depthFactor = Math.max(0.7, 1 / root.depth); // Reduce distance as depth increases

    // New spreadFactor based on number of children AND children with content
    const spreadFactor = Math.max(1, (nb_child + childrenWithContent * 0.5) * 0.5);
    const distance = 250 * mminfo.scale * depthFactor * spreadFactor;

    // Calculate starting position - centered on origin_angle
    let start_angle = isRoot ? 0 : root.origin_angle - (totalArc / 2) + (angle_per_child / 2);
    const degree_to_rad = Math.PI / 180;

    let currentEffectiveIndex = 0;

    for (let index = 0; index < root.childrens.length; index++) {
        const child = root.childrens[index];
        const hasContent = child.category.mmch_obj;
        // Calculate current angle - adjust for content weighting
        const angleWeight = hasContent ? 1.2 : 1;
        const current_angle = start_angle + (angle_per_child * currentEffectiveIndex);
        currentEffectiveIndex += angleWeight;

        const angleRad = current_angle * degree_to_rad;

        child.x = root.x + Math.cos(angleRad) * distance;
        child.y = root.y + Math.sin(angleRad) * distance;
        child.origin_angle = current_angle;
        
        // Trigger animation for this child if at appropriate depth
        if (mminfo.chemin.length >= child.depth) {
            child.animateToTarget();
        }
    }
}