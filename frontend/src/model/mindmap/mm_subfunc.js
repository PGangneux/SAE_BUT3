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
    if (last instanceof  mmch_Extrait && last.mmch_obj) {
        mminfo.extrait_current.set(last.mmch_obj);
        router.push({
            path: "/lecteur_video/"
        });
        return true;
    } else if (last instanceof mmch_Interview && last.mmch_obj) {
        mminfo.interview_current.set(last.mmch_obj);
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
    mminfo.chemin = mminfo.chemin.filter(item => !(item instanceof mmch_Root));
    return false, didchange;
}

/**
 * clear the preview nodes and linkages
 * @param {mm_Mindmap} mminfo mm_mindmap  
*/
export function mm_clean_preview(mminfo){
    mminfo.previewlinkages = [];
    if (mminfo.chemin.length < 2) return;
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
 * @param {boolean?} createLink? = true do we draw the white line or not
 * @param {boolean?} isPreview? = false whether this is a preview node
 * @return {mmch_CheminT} the created child
*/
export function mm_createChildNode(mminfo, node, category, createLink = true, isPreview = false) {
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
    const tmp_child = new Cls(mminfo, node.x, node.y, node.depth, content);
    // Add to parent's children
    node.childrens.push(markRaw(tmp_child));
    // add to mminfo nodes or previewnodes
    if (isPreview) {
        node.ispreview = true;
        mminfo.previewnodes.push(markRaw(tmp_child));
    } else {
        mminfo.nodes.push(markRaw(tmp_child));
    }
    // create linkage
    if (createLink) {
        const linkage = new mm_Linkage(node, tmp_child, thickness_base * (1 / node.depth));
        if (isPreview) {
            mminfo.previewlinkages.push(markRaw(linkage));
        } else {
            mminfo.linkages.push(markRaw(linkage));
        }
    }
    set_children_pos(mminfo, node);
    return tmp_child;
}

/**
 * Compare two nodes for equality
 * Compares by: 1) reference, 2) class type, 3) object content (UUID), 4) position for non-content nodes
 * @param {mmch_CheminT} one - First node to compare
 * @param {mmch_CheminT} other - Second node to compare
 * @returns {boolean} - True if nodes are considered equal
 */
export function mm_find_compare(one, other) {
    if (!one || !other) return false;
    if (one === other) return true;
    if (one.constructor !== other.constructor) return false;
    
    if (one.mmch_obj && other.mmch_obj) {
        if (one.mmch_obj.uuid && other.mmch_obj.uuid) {
            return one.mmch_obj.uuid === other.mmch_obj.uuid;
        }
        return one.mmch_obj === other.mmch_obj;
    }
    
    if (!one.mmch_obj && !other.mmch_obj) {
        return one.x === other.x && one.y === other.y && one.depth === other.depth;
    }
    
    return false;
}

/**
 * Find a node in the mindmap using multiple search strategies
 * First searches in the current path (chemin), then searches from root
 * @param {mm_Mindmap} mminfo - The mindmap instance
 * @param {mmch_CheminT} searched - The node to search for
 * @returns {Array<mmch_CheminT>|null} - Path to found node or null if not found
 */
export function mm_find_node(mminfo, searched) {
    return mm_find_top(mminfo, searched) || mm_find_fromroot(mminfo, searched);
}

/**
 * Search for a node starting from the current navigation path (chemin)
 * Checks nodes in the chemin, then searches recursively through children
 * @param {mm_Mindmap} mminfo - The mindmap instance
 * @param {mmch_CheminT} searched - The node to search for
 * @returns {Array<mmch_CheminT>|null} - Path to found node or null if not found
 */
function mm_find_top(mminfo, searched) {
    if (!searched || mminfo.chemin.length === 0) return null;
    
    // Check chemin nodes
    for (let i = 0; i < mminfo.chemin.length; i++) {
        if (mm_find_compare(mminfo.chemin[i], searched)) {
            return mminfo.chemin.slice(0, i + 1);
        }
    }
    
    // Use DFS to search through children of last chemin node
    const lastNode = mminfo.chemin[mminfo.chemin.length - 1];
    return dfs_search_stack(lastNode, searched, mminfo.chemin);
}

/**
 * Search for a node starting from the root node (full depth-first search)
 * @param {mm_Mindmap} mminfo - The mindmap instance
 * @param {mmch_CheminT} searched - The node to search for
 * @returns {Array<mmch_CheminT>|null} - Path from root to found node or null if not found
 */
function mm_find_fromroot(mminfo, searched) {
    if (!searched || mminfo.nodes.length === 0) return null;
    return dfs_search_stack(mminfo.nodes[0], searched, [mminfo.nodes[0]]);
}

/**
 * Generic Depth-First Search function using a stack
 * @param {mmch_CheminT} startNode - Node to start search from
 * @param {mmch_CheminT} searched - Node to search for
 * @param {Array<mmch_CheminT>} initialPath - Initial path to startNode
 * @returns {Array<mmch_CheminT>|null} - Complete path if found, null otherwise
 */
function dfs_search_stack(startNode, searched, initialPath) {
    const stack = [{ node: startNode, path: initialPath }];
    
    while (stack.length > 0) {
        const { node, path } = stack.pop();        
        if (mm_find_compare(node, searched)) {
            return [...path, node];
        }
        // Push children to stack (in reverse order for DFS)
        for (let i = node.childrens.length - 1; i >= 0; i--) {
            const child = node.childrens[i];
            stack.push({ node: child, path: [...path, child] });
        }
    }
    return null;
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
    const totalArc = isRoot ? 360 : 160; // Full circle for root, semicircle for others
    const nb_child = root.childrens.length;

    // Count children with and without content (mmch_obj)
    let childrenWithPreview = 0;
    let childrenWithContent = 0;
    let childrenWithoutContent = 0;

    for (let child of root.childrens) {
        if (child.mmch_hasMiniature()) {
            childrenWithPreview++;
        } else if (child.mmch_obj) {
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
            // TODO : REDO
            if (root.childrens[1].mmch_hasMiniature()){
                if (root_angle - root.childrens[0].origin_angle - angle_per_child * 1.4 < 5){
                    spacing_ok = true;
                }
            } else if (root.childrens[1].mmch_obj){
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
        const hasContent = child.mmch_obj;
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