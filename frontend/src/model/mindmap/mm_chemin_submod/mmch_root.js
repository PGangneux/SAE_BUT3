import mmch_CheminT from "./mmch_chemin.js";
import mmch_Artiste from "./mm_chemin_submod/mmch_artiste.js";
import mmch_Extrait from "./mm_chemin_submod/mmch_extrait.js";
import mmch_Interview from "./mm_chemin_submod/mmch_interview.js";
import mmch_Nation from "./mm_chemin_submod/mmch_nation.js";
import mmch_Question from "./mm_chemin_submod/mmch_question.js";
import mmch_StyleMusical from "./mm_chemin_submod/mmch_style_musical.js";
import mmch_Theme from "./mm_chemin_submod/mmch_theme.js";

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

class mm_Root{
}

export class mmch_Root extends mmch_CheminT {
    static mmch_dbjsclass = mm_Root;
    
    constructor() {
        super(null);
    }
    
    static async mmch_list(args = {}) {
        const results = [];
        for (const Category of mm_CategorysDefault) {
            if (Category.mmch_list) {
                const items = await Category.mmch_list(args);
                results.push(...items);
            }
        }
        return results;
    }
    
    static async mmch_search(args = {}) {
        const allCategories = [...mm_CategorysDefault, ...mm_CategorysSearch];
        const results = [];
        
        for (const Category of allCategories) {
            if (Category.mmch_search) {
                const items = await Category.mmch_search(query, args);
                results.push(...items);
            }
        }
        return results;
    }
}