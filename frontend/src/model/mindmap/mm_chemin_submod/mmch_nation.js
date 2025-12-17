import Extrait from "../../extrait.js";
import Nation from "../../nation.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Extrait from "./mmch_extrait.js";
import mmch_Artiste from "./mmch_artiste.js";

export default class mmch_Nation extends mmch_CheminT {
    static mmch_dbjsclass = Nation;
    /** @type {Nation} */
    mmch_obj;
    /** @type {Array[String]} */
    #description = null;

    async* mmch_listinst(args = {}) {
        const finalArgs = { ...this.mmch_default_listinst_args, ...args };
        yield mmch_Artiste;
        // TODO : put recomendation algorithm here
        const recommend = await Extrait.list(finalArgs);
        for (const item of recommend) {
            yield { cls: mmch_Extrait, content: item };
        }
    }

    async* mmch_searchinst(args = {}) {
        const finalArgs = { ...this.mmch_default_searchinst_args, ...args };
        yield mmch_Artiste;
        // TODO : put recomendation algorithm here
        const recommend = await Extrait.list(finalArgs);
        for (const item of recommend) {
            yield { cls: mmch_Extrait, content: item };
        }
    }

    async* mmch_previewinst(mminfo, args = {}) {
        const finalArgs = { ...this.mmch_default_previewinst_args, ...args };
        // TODO : put recomendation algorithm here
        const recommend = await Extrait.list(finalArgs);
        for (const item of recommend) {
            yield { cls: mmch_Extrait, content: item };
        }
    }

    async mmch_getDescription() {
        if (!this.mmch_obj) throw new Error("mmch description nation on empty obj");
        if (this.#description) return this.#description;
        const description = [];
        const nation = this.mmch_obj;

        if (nation.name) description.push(`Pays: ${nation.name}`);

        try {
            const artistes = await nation.artistes({ limit: 3 });
            if (artistes.length > 0) {
                description.push(`${artistes.length} artiste(s) de ce pays`);
            }
        } catch (error) { console.warn(error); }

        this.#description = description.length > 0 ? description : ["no description nation"];
        return this.#description;
    }
}