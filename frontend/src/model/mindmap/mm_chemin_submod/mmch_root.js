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

    constructor() {
        throw new Error("mmch_Root is an abstract class and cannot be instantiated directly.");
    }

    static async mmch_listcat(args = {}) {
        const results = [];
        for (const Category of mm_CategorysDefault) {
            const items = await Category.mmch_listcat(args);
            results.push(...items);
        }
        return results;
    }

    static async mmch_searchcat(args = {}) {
        const allCategories = [...mm_CategorysDefault, ...mm_CategorysSearch];
        const results = [];

        for (const Category of allCategories) {
            const items = await Category.mmch_searchcat(args);
            results.push(...items);
        }
        return results;
    }

    static async mmch_previewcat(mminfo, parent, args = {}) {
        throw new Error("mmch_Root.mmch_previewcat doesn't have preview");
    }
}