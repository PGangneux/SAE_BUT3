import Theme from "../../theme.js";
import mmch_CheminT from "./mmch_chemin.js";

export default class mmch_Theme extends mmch_CheminT {
    static mmch_dbjsclass = Theme;
    /** @type {Theme} */
    mmch_obj;

    async mmch_listinst(args = {}) {
        const finalArgs = { ...this.mmch_default_listinst_args, ...args };
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            new mmch_Question(),
            ...items.map(item => ({ cls: mmch_Extrait, content: item })),
        ];
    }

    async mmch_searchinst(args = {}) {
        const finalArgs = { ...this.mmch_default_search_args, ...args };
        const items = await Theme.search(finalArgs);
        return [
            new mmch_Question(),
            ...items.map(item => ({ cls: mmch_Extrait, content: item })),
        ];
    }

    async mmch_previewinst(mminfo,parent,args = {}){
        const finalArgs = { ...this.mmch_default_preview_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            ...items.map(item => ({ cls: mmch_Extrait, content: item })),
        ];
    }

    async mmch_getDescription() {
        if (!!this.mmch_obj) throw new Error("mmch description theme on empty obj");
        const description = [];
        const theme = this.mmch_obj;
        if (theme.description) description.push(theme.description.substring(0, 100) + "...");

        return description.length > 0 ? description : ["no description theme"];
    }
}