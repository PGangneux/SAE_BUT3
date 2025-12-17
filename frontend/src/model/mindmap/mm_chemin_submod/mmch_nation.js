import Extrait from "../../extrait.js";
import Nation from "../../nation.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Artiste from "./mmch_artiste.js";

export default class mmch_Nation extends mmch_CheminT {
    static mmch_dbjsclass = Nation;
    /** @type {Nation} */
    mmch_obj;

    async mmch_listinst(args = {}) {
        const finalArgs = { ...this.mmch_default_listinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await Extrait.list(finalArgs);
        return [
            new mmch_Artiste(null),
            ...items.map(item => ({ cls: mmch_Extrait, content: item })),
        ];
    }

    async mmch_searchinst(args = {}) {
        const finalArgs = { ...this.mmch_default_searchinst_args, ...args };
        const items = await this.mmch_dbjsclass.search(finalArgs);
        return [
            new mmch_Artiste(null),
            ...items.map(item => ({ cls: mmch_Extrait, content: item })),
        ];
    }

    async mmch_previewinst(mminfo, parent, args = {}) {
        const finalArgs = { ...this.mmch_default_previewinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            ...items.map(item => ({ cls: mmch_Extrait, content: item })),
        ];
    }

    async mmch_getDescription() {
        if (!!this.mmch_obj) throw new Error("mmch description nation on empty obj");
        const description = [];
        const nation = this.mmch_obj;

        if (nation.name) description.push(`Pays: ${nation.name}`);

        try {
            const artistes = await nation.artistes({ limit: 3 });
            if (artistes.length > 0) {
                description.push(`${artistes.length} artiste(s) de ce pays`);
            }
        } catch (error) { console.warn(error); }

        return description.length > 0 ? description : ["no description nation"];
    }
}