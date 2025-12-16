import mm_Mindmap from "./mm_mindmap.js";
import mm_Node from "./mm_node.js";
import mmch_Root from "./mm_chemin_submod/mmch_root.js";
import { mm_chemin_filter, mm_createChildNode, mm_clean_preview } from "./mm_subfunc.js"

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
    let root = new mm_Node(mminfo, 0, 0, 1, mmch_Root);
    mminfo.nodes.push(root);
    mm_draw_onecat(mminfo, root);
}

/* 
    draw the categories of one node
 * @param {mm_Mindmap} mminfo mm_Mindmap  
 * @param {mm_Node} node the root node to apply the new nodes to
*/
async function mm_draw_onecat(mminfo, node) {
    // TODO : FIX CHEMIN mmch
    // console.log("mmdraw_onecat", node);

    // failsafe videonode
    // normally we should have goto video before
    if (node.content && (node.category.name === 'Extrait' || node.category.name === 'Interview')) return;
    
    // Get the chemin handler for this node's category
    const cheminHandler = mm_CheminMap[node.category.name];
    if (!cheminHandler) {
        console.error(`No chemin handler found for category: ${node.category.name}`);
        return;
    }

    // Get categories that are NOT in the current path
    const currentPathCategories = mminfo.chemin.map(item => item.category.name);
    const availableCategories = mm_CategorysDefault.filter(cat =>
        !currentPathCategories.includes(cat.name)
    );

    if (node.content) {
        // Current node has content - add CATEGORY nodes
        console.log("Adding category nodes to content node");
        node.loading = true;
        
        // Add available category nodes
        for (const cat of availableCategories) {
            mm_createChildNode(mminfo, node, cat, null);
        }
        
        // Add Extrait nodes based on search or list
        const searchFunc = mminfo.searchval ? 
            () => cheminHandler.search(mminfo.searchval, { limit: 5 }) : 
            () => cheminHandler.list({ limit: 5 });
            
        searchFunc().then(async extraits => {
            if (extraits && extraits.length > 0) {
                for (let index = 0; index < extraits.length && index < 5 && node.childrens.length < 8; index++) {
                    mm_createChildNode(mminfo, node, node.category, extraits[index]);
                }
            }
            node.loading = false;
        }).catch(error => {
            console.error("Error loading category list:", error);
            set_children_pos(mminfo, node);
            node.loading = false;
        });
    } else {
        // Current node is a category - add content nodes using chemin handler
        node.loading = true;

        const searchFunc = mminfo.searchval ?
            () => cheminHandler.search(mminfo.searchval, { limit: 5 }) :
            () => cheminHandler.list({ limit: 5 });

        searchFunc().then(async contentList => {
            // console.log("getting detail from category", node.category, contentList);
            if (contentList && contentList.length > 0) {
                for (const element of contentList.slice(0, 5)) {
                    mm_createChildNode(mminfo, node, node.category, element);
                }
            }
            node.loading = false;
        }).catch(error => {
            console.error("Error loading category list:", error);
            set_children_pos(mminfo, node);
            node.loading = false;
        });
    }
}