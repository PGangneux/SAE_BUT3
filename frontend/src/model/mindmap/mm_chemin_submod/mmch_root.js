import mmch_CheminT from "./mmch_chemin.js";
import mmch_Artiste from "./mmch_artiste.js";
import mmch_Extrait from "./mmch_extrait.js";
import mmch_Interview from "./mmch_interview.js";
import mmch_Nation from "./mmch_nation.js";
import mmch_Question from "./mmch_question.js";
import mmch_StyleMusical from "./mmch_style_musical.js";
import mmch_Theme from "./mmch_theme.js";

const mm_CategorysDefault = [
    mmch_Artiste,
    mmch_Nation,
    mmch_StyleMusical,
    mmch_Theme,
];

const mm_CategorysSearch = [
    mmch_Question,
    mmch_Extrait,
    mmch_Interview
];

class mm_Root {
}

export default class mmch_Root extends mmch_CheminT {
    static mmch_dbjsclass = mm_Root;

    static async mmch_listcat(args = {}) {
        return mm_CategorysDefault
    }

    static async mmch_searchcat(args = {}){
        return [...mm_CategorysDefault, ...mm_CategorysSearch];
    }

    static async mmch_previewcat(mminfo, parent, args = {}) {
        throw new Error("mmch_Root.mmch_previewcat doesn't have preview");
    }
}