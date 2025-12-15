import { markRaw } from "vue";
import mm_mindmap from "./mm_mindmap.js";
import mm_node from "./mm_node.js";
import mmch_Root  from "./mm_chemin_submod/mmch_root.js";
import { mmchemin_filter } from "./mm_subfunc.js"

/**
    redraw everynode from root
 * @param {mm_mindmap} mminfo mm_mindmap  
*/
export async function mmdraw_root(mminfo) {
    mmreset(mminfo);
    let changevideo, changepath = mmchemin_filter(mminfo);
    if (changevideo) return;
    // console.log("mmdraw_root chemin path", mminfo.chemin);
    for (const cheminpath of mminfo.chemin) {
        await mmdraw_onecat(mminfo, cheminpath);
    }
}

/**
    redraw an update
 * @param {mm_mindmap} mminfo mm_mindmap  
*/
export async function mmdraw_update(mminfo) {
    if (mminfo.chemin.length <= 0) return mmdraw_root(mminfo);
    let changevideo, changepath = mmchemin_filter(mminfo);
    if (changevideo) return;
    if (changepath) return mmdraw_root(mminfo);
    console.log("mmdraw_update chemin path", mminfo.chemin);
    await mmdraw_onecat(mminfo, mminfo.chemin[mminfo.chemin.length - 1]);
}

/**
    recreate the root node and reset everything
 * @param {mm_mindmap} mminfo mm_mindmap  
*/
export function mmreset(mminfo) {
    // reset everything
    mminfo.nodes = [];
    mminfo.linkages = [];
    // create root
    let root = new mm_node(mminfo,0, 0, 1, mmch_Root, null);
    mminfo.nodes.push(root);
    mmdraw_onecat(root);
}

/**
    utils to create a child node
 * @param {mm_mindmap} mminfo mm_mindmap  
 * @param {mm_node} node the parent node  
 * @param {class} category the class of node  
 * @param {class} content the content instance of class category
 * @param {boolean} createLink = true do we draw the white line or not
 * @return {mm_node} the created child
*/
export function mmcreateChildNode(mminfo, node, category, content, createLink = true) {
    const thickness_base = (mminfo.chemin.length + 1) * 3;
    const tmp_child = new mm_node(mminfo,node.x, node.y, node.depth + 1, category, content);
    // console.table({"node":node, "category":category, "content":content, "createLink":createLink });
    // console.log("mmcreateChildNode",tmp_child);
    mminfo.nodes.push(markRaw(tmp_child));
    node.childrens.push(markRaw(tmp_child));
    // console.log("thicness",mminfo.chemin.length,root.depth,thickness_base,thickness_base * (1 / root.depth));
    if (createLink) {
        // TODO : change to have that in linkage constructor
        mminfo.linkages.push(new mmLinkage(node, tmp_child, thickness_base * (1 / node.depth)));
    }
    set_children_pos(mminfo, node);
    return tmp_child;
}

/**
 * pos the children of a node in a circle
 * @param {mm_mindmap} mminfo mm_mindmap  
 * @param {mm_node} root the root node to witch the children has been added
 */
export function set_children_pos(mminfo, root) {
    // failsafe , si pas enfant
    if (!root.childrens.length) return;

    // est ce que c'est mm_Root ou pas 
    const isRoot = root.category == mm_Root;
    const totalArc = isRoot ? 360 : 160; // Full circle for root, semicircle for others
    const nb_child = root.childrens.length;

    // Count children with and without content
    let childrenWithPreview = 0;
    let childrenWithContent = 0;
    let childrenWithoutContent = 0;

    for (let child of root.childrens) {
        if (child.hasPreview()) {
            childrenWithPreview++;
        } else if (child.content) {
            childrenWithContent++;
        }else {
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
        let spacingConsistent = true;
        
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
            if (root.childrens[1].hasPreview()){
                if (root_angle - )
            } else if (root.childrens[1].content){

            } else {
                
            }
        }
    } 
    // If we reach here, we need to recalculate positions
    
    // distance entre root et enfant ;
    // so the distance is inversly proportional to the number of angle_per_child
    const depthFactor = Math.max(0.7, 1 / root.depth); // Reduce distance as depth increases

    // New spreadFactor based on number of children AND children with content
    const spreadFactor = Math.max(1, (nb_child + childrenWithContent * 0.5) * 0.5);
    const distance = 200 * mminfo.scale * depthFactor * spreadFactor;

    // Calculate starting position - centered on origin_angle
    let start_angle = isRoot ? 0 : root.origin_angle - (totalArc / 2) + (angle_per_child / 2);
    const degree_to_rad = Math.PI / 180;

    let currentEffectiveIndex = 0;

    for (let index = 0; index < root.childrens.length; index++) {
        const child = root.childrens[index];
        const hasContent = child.content;
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

/**
    draw the categories of one node
 * @param {mm_mindmap} mminfo mm_mindmap  
 * @param {mm_node} node the root node to apply the new nodes to
*/
async function mmdraw_onecat(mminfo, node) {
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
            mmcreateChildNode(mminfo, node, cat, null);
        }
        
        // Add Extrait nodes based on search or list
        const searchFunc = mminfo.searchval ? 
            () => cheminHandler.search(mminfo.searchval, { limit: 5 }) : 
            () => cheminHandler.list({ limit: 5 });
            
        searchFunc().then(async extraits => {
            if (extraits && extraits.length > 0) {
                for (let index = 0; index < extraits.length && index < 5 && node.childrens.length < 8; index++) {
                    mmcreateChildNode(mminfo, node, node.category, extraits[index]);
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
                    mmcreateChildNode(mminfo, node, node.category, element);
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