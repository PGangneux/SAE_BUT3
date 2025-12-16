import StyleMusical from "../../style_musical.js";
import mmch_CheminT from "./mmch_chemin.js";

export default class mmch_StyleMusical extends mmch_CheminT {
    static mmch_dbjsclass = StyleMusical;
    mmch_obj;

    constructor({inst = null} = {}) {
        this.mmch_obj = inst;
    }

    static async mmch_list(args = {}) {
        const finalArgs = { ...this.mmch_default_list_args, ...args };
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            new mmch_Artiste(null),
            ...items.map(item => new mmch_StyleMusical(item)),
        ];
    }

    static async mmch_search(args = {}) {
        const finalArgs = { ...this.mmch_default_search_args, ...args };
        const items = await StyleMusical.search(finalArgs);
        return [
            new mmch_Artiste(null),
            ...items.map(item => new mmch_StyleMusical(item)),
        ];
    }

    static async mmch_preview(mminfo,parent,args = {}){
        const finalArgs = { ...this.mmch_default_preview_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            ...items.map(item => new mmch_StyleMusical(item)),
        ];
    }

    async mmch_getDescription() {
        if (!!this.mmch_obj) throw new Error("mmch mmch_getTitle style musical on empty obj");
        return "";
    }
}