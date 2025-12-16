import Artiste from "../../artiste.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Extrait from "./mmch_extrait.js";
import mmch_Nation from "./mmch_nation.js";
import mmch_StyleMusical from "./mmch_style_musical.js";

export default class mmch_Artiste extends mmch_CheminT {
    static mmch_dbjsclass = Artiste;
    /** @type {Artiste} */
    mmch_obj;

    constructor({ inst = null } = {}) {
        this.mmch_obj = inst;
    }

    static async mmch_list(args = {}) {
        const finalArgs = { ...this.mmch_default_list_args, ...args };
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            new mmch_Extrait(null),
            new mmch_Nation(null),
            new mmch_StyleMusical(null),
            ...items.map(item => new mmch_Artiste(item)),
        ];
    }

    static async mmch_search(args = {}) {
        const finalArgs = { ...this.mmch_default_search_args, ...args };
        const items = await Artiste.search(finalArgs);
        return [
            new mmch_Extrait(null),
            new mmch_Nation(null),
            new mmch_StyleMusical(null),
            ...items.map(item => new mmch_Artiste(item)),
        ];
    }

    static async mmch_Preview(mminfo,parent,args = {}){
        const finalArgs = { ...this.mmch_default_preview_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            ...items.map(item => new mmch_Artiste(item)),
        ];
    }

    async mmch_getDescription() {
        if (!!this.mmch_obj) throw new Error("mmch description artiste on empty obj");
        const description = [];

        try {
            const nation = await artiste.nation();
            if (nation && nation.name) description.push(`Pays: ${nation.name}`);
        } catch (error) { console.warn(error); }

        try {
            const styles = await artiste.styles({ limit: 3 });
            if (styles.length > 0) {
                const styleNames = styles.map(s => s.name).join(', ');
                description.push(`Styles: ${styleNames}`);
            }
        } catch (error) { console.warn(error); }

        try {
            const extraits = await artiste.extraits({ limit: 3 });
            if (extraits.length > 0) {
                description.push(`${extraits.length} extrait(s) disponible(s)`);
            }
        } catch (error) { console.warn(error); }

        return description.length > 0 ? description : ["no description artiste"];
    }
}