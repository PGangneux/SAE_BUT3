import router from "../../router.js";
import mm_Mindmap from "./mm_mindmap.js";
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