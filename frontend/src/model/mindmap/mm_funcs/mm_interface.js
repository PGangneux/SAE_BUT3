import { videoStore } from "../../videoStore.js";
import mm_Mindmap from "../mm_mindmap.js";
import { mm_chemin_filter } from "./mm_func_chemin.js"
import { mm_reset_soft , mm_draw_onecat } from "./mm_func.js";

/**
 *  redraw everynode from root
 * @param {mm_Mindmap} mminfo mm_Mindmap 
 * @returns {Promise<Boolean>} if it's a video or not 
*/
export async function mm_draw_root(mminfo) {
    let reset_hard = await mm_reset_soft(mminfo);
    let changevideo, changepath = mm_chemin_filter(mminfo);
    if (changevideo) return true;
    /// console.log("mm_draw_root reset_hard:",reset_hard,"changepath:",changepath);
    if (!reset_hard) {
        for (const child of mminfo.nodes[0].childrens) {
            child.childrens = [];
            await mm_draw_onecat(mminfo, child);
        }
    }
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

/**
 * the main entry interface for Mind Map shenanigans 
*/
export async function mm_interface_handleclick(mminfo,node){
    mminfo.chemin.push(node);
    console.log("mm hanldeclick",mminfo.chemin);
    let isvideo = await mm_draw_update(mminfo);
    if (isvideo){
        console.log("video store path before",videoStore.chemin);
        console.log("video store set",mminfo.chemin,mminfo);
        videoStore.chemin = mminfo.chemin;
    }
}