import { videoStore } from "../../videoStore.js";
import mm_Mindmap from "../mm_mindmap.js";
import { mm_chemin_filter } from "./mm_func_chemin.js"
import { mm_reset_soft , mm_draw_onecat } from "./mm_func.js";

/**
 *  redraw everynode from root
 * @param {mm_Mindmap} mminfo mm_Mindmap  
*/
export async function mm_draw_root(mminfo) {
    let reset_hard = await mm_reset_soft(mminfo);
    let changevideo, changepath = mm_chemin_filter(mminfo);
    if (changevideo) return;
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
}

/**
 *  redraw an update
 * @param {mm_Mindmap} mminfo mm_Mindmap  
*/
export async function mm_draw_update(mminfo) {
    if (mminfo.chemin.length <= 0) return mm_draw_root(mminfo);
    let changevideo, changepath = mm_chemin_filter(mminfo);
    if (changevideo) return;
    if (changepath) return mm_draw_root(mminfo);
    await mm_draw_onecat(mminfo, mminfo.chemin[mminfo.chemin.length - 1]);
}

export async function mm_interface_handleclick(mminfo,node){
    mminfo.chemin.push(node);
    videoStore.chemin = mminfo.chemin;
    console.log("mm hanldeclick",mminfo.chemin);
    await mm_draw_update(mminfo);
}