import { videoStore } from "../../videoStore.js";
import mm_Mindmap from "../mm_mindmap.js";
import mmch_CheminT from "../mm_chemin_submod/mmch_chemin.js";
import { mm_reset_soft , mm_draw_onecat } from "./mm_func.js";
import { mm_chemin_filter } from "./mm_func_chemin.js"

/**
 *  redraw everynode from root
 * @param {mm_Mindmap} mminfo mm_Mindmap 
 * @returns {Promise<Boolean>} if it's a video or not 
*/
export async function mm_draw_root(mminfo) {
    await mm_reset_soft(mminfo); // weither we needed to recreate everything or not
    let changevideo, changepath = mm_chemin_filter(mminfo); // we can ignore change path here because it's drawing from the root
    if (changevideo) return true;
    console.log("mm_draw_root reset_hard:",reset_hard,"changepath:",changepath);
    for (const cheminpath of mminfo.chemin) {
        await mm_draw_onecat(mminfo, cheminpath);
    }
    return false;
}

/**
 *  redraw an update
 * @param {mm_Mindmap} mminfo mm_Mindmap  
 * @returns {Promise<Boolean>} if it's a video or not 
*/
export async function mm_draw_update(mminfo) {
    if (mminfo.chemin.length <= 0) return mm_draw_root(mminfo);
    let changevideo, changepath = mm_chemin_filter(mminfo);
    if (changevideo) return true;
    if (changepath) return mm_draw_root(mminfo);
    await mm_draw_onecat(mminfo, mminfo.chemin[mminfo.chemin.length - 1]);
    return false;
}

const doesblock = false;

/**
 * the main entry interface for Mind Map shenanigans 
 * @param {mm_Mindmap} mminfo mm_Mindmap
 * @param {mmch_CheminT<T>} node mm_Node clicked
*/
export async function mm_interface_handleclick(mminfo,node){
    if (doesblock) {
        console.log("spam blocked");
        return;
    }
    console.log("running mm algo");
    doesblock = true;
    console.log("mm hanldeclick",mminfo.chemin,node.mmch_key,node);
    mminfo.chemin.push(node.mmch_key); // TODO : verify
    let isvideo = await mm_draw_update(mminfo);
    if (isvideo){
        console.log("video store path before",videoStore.chemin);
        console.log("video store set",mminfo.chemin,mminfo);
        videoStore.chemin = mminfo.chemin;
    }
    console.log("mm hanldeclick end");
    
    doesblock = false;
}