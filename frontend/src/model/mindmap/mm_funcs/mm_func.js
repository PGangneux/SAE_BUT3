import { markRaw } from "vue";
import { mm_createChildNode, set_children_pos } from "./mm_func_node.js"
import { mm_find_compare } from "./mm_func_chemin.js";
import mm_Mindmap from "../mm_mindmap.js";
import mmch_CheminT from "../mm_chemin_submod/mmch_chemin.js";
import mmch_Root from "../mm_chemin_submod/mmch_root.js";

/**
 *  recreate the root node and reset everything
 * @param {mm_Mindmap} mminfo mm_Mindmap  
*/
function mm_reset_hard(mminfo) {
    // reset everything
    mminfo.nodes = [];
    mminfo.linkages = [];
    mminfo.previewnodes = [];
    mminfo.previewlinkages = [];
    // create root
    let root = markRaw(new mmch_Root(mminfo, 0, 0, 0, null));
    mminfo.nodes.push(root);
    mm_draw_onecat(mminfo, root, false);
}

/**
 * Soft reset of mindmap - clears previews and adjusts nodes based on search
 * @param {mm_Mindmap} mminfo mm_Mindmap  
 */
export async function mm_reset_soft(mminfo) {
    try {
        // Clear all preview elements and linkages
        mminfo.previewnodes = [];
        mminfo.previewlinkages = [];
        mminfo.linkages = []; // Root has no linkages anyway
        
        // Safeguard: Check if we have a valid root node
        if (!mminfo.nodes || mminfo.nodes.length === 0 || !mminfo.nodes[0]) {
            mm_reset_hard(mminfo);
            return;
        }

        const rootNode = mminfo.nodes[0];
        const list_cat = [];
        for await (const item of rootNode.constructor.mmch_listcat()) {
            list_cat.push(item);
        }
        
        let search_cat = [];
        let sameCount = 0; // How many nodes are the same between existing and search
        let nodesToCreate = 0; // How many new nodes to create

        // Only get search_cat if we have a search value
        if (mminfo.searchval && mminfo.searchval.trim() !== "") {
            for await (const item of rootNode.constructor.mmch_searchcat()) {
                search_cat.push(item);
            }
            
            // Compare each position to see how many nodes are the same
            for (let i = 0; i < Math.min(search_cat.length, mminfo.nodes.length - 1); i++) {
                const existingChild = mminfo.nodes[i + 1]; // +1 to skip root
                const searchResult = search_cat[i];
                
                if (searchResult && existingChild) {
                    // Compare
                    if (mm_find_compare(searchResult,existingChild)) {
                        sameCount = i + 1; // Update count of same nodes
                    } else {
                        break; // Stop at first difference
                    }
                } else {
                    break; // Stop if either is missing
                }
            }
            
            // Calculate how many nodes to create
            nodesToCreate = search_cat.length - sameCount;
        }
        // Handle nodes array
        if (search_cat.length > 0) {
            // Always slice to search count in search mode
            mminfo.nodes = mminfo.nodes.slice(0, search_cat.length + 1);
            // If we have nodes to create, create them
            if (nodesToCreate > 0) {
                // Create the nodes that are different/new
                for (let i = sameCount; i < search_cat.length; i++) {
                    const nodeData = search_cat[i];
                    await mm_createChildNode(mminfo, rootNode, nodeData, true, false);
                }
            }
        } else {
            // List mode: slice to list count
            mminfo.nodes = mminfo.nodes.slice(0, list_cat.length + 1);
        }
    } catch (error) {
        console.error("Error in mm_reset_soft:", error);
        mm_reset_hard(mminfo);
    }
}


/**
 * draw the categories of one node
 * @param {mm_Mindmap} mminfo mm_Mindmap  
 * @param {mmch_CheminT} node the root node to apply the new nodes to
 * @param {boolean?} createLink? = true do we draw the white line or not
 * @param {boolean?} isPreview? = false whether this is a preview node
*/
export async function mm_draw_onecat(mminfo, node, createLink = true, isPreview = false) {
    // 0. safe Guards
    // Video / preview-only nodes never expand
    console.log(node);
    if (node.mmch_obj && node.mmch_hasMiniature()) return;
    node.loading = true;
    try {
        if (node.ispreview) {
            if (node.mmch_obj) {
                // ─────────────────────────────
                // 3a. expand PREVIEW NODE with CONTENT
                // ─────────────────────────────
                // do nothing
                console.log("3a expand PREVIEW NODE with CONTENT",node);
                ;
            } else {
                // ─────────────────────────────
                // 3b. expand PREVIEW NODE without content
                // ─────────────────────────────
                console.log("3b expand PREVIEW NODE without content",node);
                
                // Handle async* generator
                for await (const catnode of node.mmch_previewinst(mminfo)) {
                    mm_createChildNode(mminfo, node, catnode, createLink, isPreview);
                }
                node.loading = false;
                for (const child of node.childrens) {
                    await mm_draw_onecat(mminfo, child, createLink, isPreview);
                }
            }
        }
        else if (node.mmch_obj) {
            // ─────────────────────────────
            // 1b. CONTENT NODE → CATEGORIES
            // ─────────────────────────────
            console.log("1b CONTENT NODE → CATEGORIES",node);
            // Handle async* generator for instance methods
            for await (const instnode of node.mmch_listinst()) {
                mm_createChildNode(mminfo, node, instnode, createLink, isPreview);
            }
            node.loading = false;
            for (const child of node.childrens) {
                await mm_draw_onecat(mminfo, child, createLink, isPreview);
            }
        } else {
            // ─────────────────────────────
            // 1a. CATEGORY NODE → CONTENT
            // ─────────────────────────────
            console.log("1a CATEGORY NODE → CONTENT",node);
            const getnodefunc = mminfo.searchval ?
                () => node.constructor.mmch_searchcat() :
                () => node.constructor.mmch_listcat();

            // Handle async* generator for static methods
            for await (const catnode of getnodefunc()) {
                mm_createChildNode(mminfo, node, catnode, createLink, isPreview);
            }
            node.loading = false;
            for (const child of node.childrens) {
                await mm_draw_onecat(mminfo, child, createLink, isPreview);
            }
        }
        if (node.depth > mminfo.chemin.length) {
            // ─────────────────────────────
            // 2. DRAW previews of subcategories
            // ─────────────────────────────
            // You might need to handle async generators here too
            // depending on what Promise.all() was doing
            // Promise.all();
            console.log("2 DRAW previews of subcategories",node);
        }
    } catch (err) {
        console.error("mm_draw_onecat error:", err);
    }
    node.loading = false;
}