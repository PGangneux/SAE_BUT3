import mm_Mindmap from "./mm_mindmap.js";
import mmch_Root from "./mm_chemin_submod/mmch_root.js";
import mmch_Extrait from "./mm_chemin_submod/mmch_extrait.js";
import mmch_Interview from "./mm_chemin_submod/mmch_interview.js";
import router from "../../router.js";

/**
    check video
 * @param {mm_Mindmap} mminfo mm_mindmap  
 * @return {boolean} if there is a goto video or not
*/
export function mm_checkvideo(mminfo) {
    if (mminfo.chemin.length == 0) return false;
    let last = mminfo.chemin[mminfo.chemin.length - 1];
    if (!!last) return false;
    if (last.category == mmch_Extrait && last.category.mmch_obj) {
        mminfo.extrait_current.set(last.category);
        router.push({
            path: "/lecteur_video/"
        });
        return true;
    } else if (last.category == mmch_Interview && last.category.mmch_obj) {
        mminfo.interview_current.set(last.category);
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
    mminfo.chemin = mminfo.chemin.filter(item => item.category !== mmch_Root);
    return false, didchange;
}