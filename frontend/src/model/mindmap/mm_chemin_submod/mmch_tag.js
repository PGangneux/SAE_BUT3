import Tag from "../../tag.js";
import mmch_CheminT from "./mmch_chemin.js";

export default class mmch_Tag extends mmch_CheminT {
    static mmch_dbjsclass = Tag;
    mmch_obj;

    constructor({inst = null} = {}) {
        this.mmch_obj = inst;
    }

    static async mmch_list(args = {}) {
        const finalArgs = { ...this.mmch_default_list_args, ...args };
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            new mmch_Extrait(null),
            new mmch_Interview(null),
            ...items.map(item => new mmch_Tag(item)),
        ];
    }

    static async mmch_search(args = {}) {
        const finalArgs = { ...this.mmch_default_search_args, ...args };
        const items = await Tag.search(finalArgs);
        return [
            new mmch_Extrait(null),
            new mmch_Interview(null),
            ...items.map(item => new mmch_Tag(item)),
        ];
    }

    static async mmch_preview(mminfo,parent,args = {}){
        const finalArgs = { ...this.mmch_default_preview_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            ...items.map(item => new mmch_Tag(item)),
        ];
    }

    async mmch_getDescription() {
        if (!!this.mmch_obj) throw new Error("mmch mmch_getTitle tag on empty obj");
        return "";
    }
}