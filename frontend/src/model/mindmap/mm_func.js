import { mm_chemin_filter, mm_createChildNode, mm_clean_preview } from "./mm_subfunc.js"
import mm_Mindmap from "./mm_mindmap.js";
import mmch_CheminT from "./mm_chemin_submod/mmch_chemin.js";
import mmch_Root from "./mm_chemin_submod/mmch_root.js";
import { markRaw } from "vue";

/**
    redraw everynode from root
 * @param {mm_Mindmap} mminfo mm_Mindmap  
*/
export async function mm_draw_root(mminfo) {
    mm_reset(mminfo);
    let changevideo, changepath = mm_chemin_filter(mminfo);
    if (changevideo) return;
    for (const cheminpath of mminfo.chemin) {
        await mm_draw_onecat(mminfo, cheminpath);
    }
}

/**
    redraw an update
 * @param {mm_Mindmap} mminfo mm_Mindmap  
*/
export async function mm_draw_update(mminfo) {
    if (mminfo.chemin.length <= 0) return mm_draw_root(mminfo);
    let changevideo, changepath = mm_chemin_filter(mminfo);
    if (changevideo) return;
    if (changepath) return mm_draw_root(mminfo);
    mm_clean_preview(mminfo);
    await mm_draw_onecat(mminfo, mminfo.chemin[mminfo.chemin.length - 1]);
}

/**
    recreate the root node and reset everything
 * @param {mm_Mindmap} mminfo mm_Mindmap  
*/
function mm_reset(mminfo) {
    // reset everything
    mminfo.nodes = [];
    mminfo.linkages = [];
    mminfo.previewnodes = [];
    // create root
    let root = markRaw(new mmch_Root(mminfo, 0, 0, 0, null));
    mminfo.nodes.push(root);
    mm_draw_onecat(mminfo, root,false);
}

/**
 * draw the categories of one node
 * @param {mm_Mindmap} mminfo mm_Mindmap  
 * @param {mmch_CheminT} node the root node to apply the new nodes to
 * @param {boolean?} createLink? = true do we draw the white line or not
 * @param {boolean?} isPreview? = false whether this is a preview node
*/
async function mm_draw_onecat(mminfo, node, createLink = true, isPreview = false) {
    // 0. safe Guards
    // Video / preview-only nodes never expand
    console.log(node);
    if (node.ispreview) return;
    if (node.mmch_obj && node.mmch_hasMiniature()) return;
    node.loading = true;
    try {
        if (node.ispreview){
            if (node.mmch_obj) {
                // ─────────────────────────────
                // 3a. expand PREVIEW NODE with CONTENT
                // ─────────────────────────────
                // do nothing
                ;
            } else {
                // ─────────────────────────────
                // 3b. expand PREVIEW NODE without content
                // ─────────────────────────────
                // Handle async* generator
                for await (const catnode of node.mmch_previewinst(mminfo)) {
                    mm_createChildNode(mminfo, node, catnode, createLink, isPreview);
                }
            }
        }
        else if (node.mmch_obj) {
            // ─────────────────────────────
            // 1b. CONTENT NODE → CATEGORIES
            // ─────────────────────────────
            // Handle async* generator for instance methods
            for await (const instnode of node.mmch_listinst()) {
                mm_createChildNode(mminfo, node, instnode, createLink, isPreview);
            }
        } else {
            // ─────────────────────────────
            // 1a. CATEGORY NODE → CONTENT
            // ─────────────────────────────
            const getnodefunc = mminfo.searchval ?
                () => node.constructor.mmch_searchcat() :
                () => node.constructor.mmch_listcat();
            
            // Handle async* generator for static methods
            for await (const catnode of getnodefunc()) {
                mm_createChildNode(mminfo, node, catnode, createLink, isPreview);
            }
        }
        if (node.depth < mminfo.chemin.length-1) {
            // ─────────────────────────────
            // 2. DRAW previews of subcategories
            // ─────────────────────────────
            // You might need to handle async generators here too
            // depending on what Promise.all() was doing
            // Promise.all();
        }
    } catch (err) {
        console.error("mm_draw_onecat error:", err);
    }
    node.loading = false;    
}