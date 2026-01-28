import { markRaw } from "vue";
import mm_Mindmap from "../mm_mindmap.js";
import mm_Linkage from "../mm_linkage.js";
import mmch_CheminT from "../mm_chemin_submod/mmch_chemin.js";
import mmch_Root from "../mm_chemin_submod/mmch_root.js";

/**
 *  utils to create a child node
 * @param {mm_Mindmap} mminfo mm_Mindmap  
 * @param {mmch_CheminT} parent the parent node  
 * @param {mmch_CheminT} category the class of node  
 * @param {boolean?} createLink? = true do we draw the white line or not
 * @param {boolean?} isPreview? = false whether this is a preview node
 * @return {mmch_CheminT} the created child
*/
export function mm_createChildNode(mminfo, parent, category, createLink = true, isPreview = false) {
    const thickness_base = (mminfo.chemin.length + 1) * 3;
    let Cls, content;
    // Determine if category is a simple class or a config object
    if (category && typeof category.cls === 'function') {
        // It's a config object { cls: mmch_Extrait, content: item }
        Cls = category.cls;
        content = category.content;
    } else if (typeof category === 'function' && category.prototype) {
        // It's a class constructor (like mmch_Extrait)
        Cls = category;
        content = null;
    } else {
        console.error("Invalid category passed to mm_createChildNode:", category);
        return null;
    }    
    // Create the instance
    
    const tmp_child = new Cls(mminfo, parent.x, parent.y, parent.depth, content);
    console.log(mminfo);
    
    // Add to parent's children
    parent.childrens.push(markRaw(tmp_child));
    // add to mminfo nodes or previewnodes    
    if (isPreview) {
        tmp_child.ispreview = true;
        mminfo.previewnodes.push(markRaw(tmp_child));
    } else {
        mminfo.nodes.push(markRaw(tmp_child));
    }
    // create linkage
    if (createLink) {
        const linkage = new mm_Linkage(parent, tmp_child, thickness_base * (1 / tmp_child.depth));
        if (isPreview) {
            mminfo.previewlinkages.push(markRaw(linkage));
        } else {
            mminfo.linkages.push(markRaw(linkage));
        }
    }
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
    const isRoot = root instanceof mmch_Root;
    const totalArc = isRoot ? 360 : 170; // Full circle for root, semicircle for others
    // Count children with and without content (mmch_obj)
    let childrenWithPreview = 0;
    let childrenWithContent = 0;
    let childrenEmpty = 0;

    for (let child of root.childrens) {
        if (child.mmch_hasMiniature()) {
            childrenWithPreview++;
        } else if (child.mmch_obj) {
            childrenWithContent++;
        } else {
            childrenEmpty++;
        }
    }
    // Calculate angle per child based on content
    // Children with content get 1.2x more angle space
    const childrenPreviewWeight = 10.0;
    const childrenContentWeight = 1.4;
    const childrenEmptyWeight = 1.0;
    const effectiveChildren = childrenWithPreview * childrenPreviewWeight
                            + childrenWithContent * childrenContentWeight
                            + childrenEmpty * childrenEmptyWeight;
    const angle_per_child = totalArc / effectiveChildren;

    console.log("prev",childrenWithPreview,childrenWithPreview * childrenPreviewWeight, "content",
                             childrenWithContent,childrenWithContent * childrenContentWeight
                            ,"empty",childrenEmpty, childrenEmpty * childrenEmptyWeight);
    

    // distance entre root et enfant ;
    // so the distance is inversly proportional to the number of angle_per_child
    const depthFactor = Math.min(0.9, Math.max(2.0, root.depth/10)); // Reduce distance as depth increases

    // spreadFactor based on number of children AND children with content
    const spreadFactor = Math.max(1, effectiveChildren);
    const distance = 150 + 10 * mminfo.scale * depthFactor * spreadFactor;

    // Calculate starting position - centered on origin_angle
    let start_angle = isRoot ? 0 : root.origin_angle;
    const degree_to_rad = Math.PI / 180;
    let currentEffectiveIndex = 0;

    console.log("commence");
    
    for (let index = 0; index < root.childrens.length; index++) {
        const child = root.childrens[index];
        // Calculate current angle - adjust for content weighting
        let angleWeight;
        if (child.mmch_hasMiniature()) {
            angleWeight = childrenPreviewWeight;
        } else if (child.mmch_obj) {
            angleWeight = childrenContentWeight;
        } else {
            angleWeight = childrenEmptyWeight;
        }
        console.log(angleWeight);
        
        const current_angle = start_angle + (angle_per_child * currentEffectiveIndex);
        
        const angleRad = current_angle * degree_to_rad;
        
        child.targetX = root.x + Math.cos(angleRad) * distance;
        child.targetY = root.y + Math.sin(angleRad) * distance;
        child.origin_angle = current_angle;
        console.log("origin_angle",root.origin_angle,"start_angle",start_angle,"effectiveChildren",effectiveChildren,"currentEffectiveIndex",currentEffectiveIndex,"angle_per_child",angle_per_child,"i",index,"current_angle",current_angle,child);
        
        currentEffectiveIndex += angleWeight;
        console.log("currentEffectiveIndex",currentEffectiveIndex);
        
        
        // Trigger animation for this child if at appropriate depth
        // console.log(root,child,mminfo.chemin.length, ">=", child.depth);
        
        if (mminfo.chemin.length >= child.depth) {
            child.animateToTarget();
        } else {
            child.x = child.targetX;
            child.y = child.targetY;
        }
    }
    // console.log("fini");
}