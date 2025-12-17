import { mm_chemin_filter, mm_createChildNode, mm_clean_preview } from "./mm_subfunc.js"
import mm_Mindmap from "./mm_mindmap.js";
import mmch_CheminT from "./mm_chemin_submod/mmch_chemin.js";
import mmch_Root from "./mm_chemin_submod/mmch_root.js";

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
    let root = new mmch_Root(mminfo, 0, 0, 0,null);
    mminfo.nodes.push(root);
    mm_draw_onecat(mminfo, root);
}

/**
 * draw the categories of one node
 * @param {mm_Mindmap} mminfo mm_Mindmap  
 * @param {mmch_CheminT} node the root node to apply the new nodes to
*/
async function mm_draw_onecat(mminfo, node) {
    // 0. safe Guards
    // Video / preview-only nodes never expand
    console.log(node);
    if (node.ispreview) return;
    if (node.mmch_obj && node.mmch_hasMiniature()) return;
    const current_maxdepth = mminfo.chemin.length-1;
        node.loading = true;
    try {
        if (node.mmch_obj){
            // ─────────────────────────────
            // 2. CONTENT NODE → CATEGORIES
            // ─────────────────────────────
            
            // ─────────────────────────────
            // 3. CONTENT NODE → PREVIEW
            // ─────────────────────────────
    } else {
            // ─────────────────────────────
            // 1. CATEGORY NODE → CONTENT
            // ─────────────────────────────
            const getnodefunc = mminfo.searchval ? 
                () => node.constructor.mmch_searchcat() :
                () => node.constructor.mmch_listcat();
            getnodefunc().then(async catnodes => {
                console.log(catnodes);
                
                catnodes.forEach(catnode => {
                    console.log(catnode);
                    
                    mm_createChildNode(mminfo, node, catnode,null);
                });
            });
        } 
    } catch (err) {
        console.error("mm_draw_onecat error:", err);
            }
            node.loading = false;
}