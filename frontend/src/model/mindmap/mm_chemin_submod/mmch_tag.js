import Extrait from "../../extrait.js";
import Tag from "../../tag.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Extrait from "./mmch_extrait.js";
import mmch_Interview from "./mmch_interview.js";

export default class mmch_Tag extends mmch_CheminT {
    static mmch_dbjsclass = Tag;
    /** @type {Tag} */
    mmch_obj;

    async mmch_listinst(args = {}) {
        const finalArgs = { ...this.mmch_default_listinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await Extrait.list(finalArgs);
        return [
            new mmch_Extrait(null),
            new mmch_Interview(null),
            ...items.map(item => ({ cls: mmch_Extrait, content: item })),
        ];
    }

    async mmch_searchinst(args = {}) {
        const finalArgs = { ...this.mmch_default_searchinst_args, ...args };
        const items = await this.mmch_dbjsclass.search(finalArgs);
        return [
            new mmch_Extrait(null),
            new mmch_Interview(null),
            ...items.map(item => ({ cls: mmch_Extrait, content: item })),
        ];
    }

    async mmch_previewinst(mminfo, args = {}) {
        const finalArgs = { ...this.mmch_default_previewinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            ...items.map(item => ({ cls: mmch_Extrait, content: item })),
        ];
    }

    async mmch_getDescription() {
        if (!!this.mmch_obj) throw new Error("mmch mmch_getTitle tag on empty obj");
        return "";
    }
}