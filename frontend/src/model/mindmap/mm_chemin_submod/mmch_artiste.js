import Extrait from "../../extrait.js";
import Artiste from "../../artiste.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Extrait from "./mmch_extrait.js";
import mmch_Nation from "./mmch_nation.js";
import mmch_StyleMusical from "./mmch_style_musical.js";

export default class mmch_Artiste extends mmch_CheminT {
    static mmch_dbjsclass = Artiste;
    /** @type {Artiste} */
    mmch_obj;

    async mmch_listinst(args = {}) {
        const finalArgs = { ...this.mmch_default_listinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await this.mmch_obj.extraits();
        return [
            mmch_Extrait,
            mmch_Nation,
            mmch_StyleMusical,
            ...items.map(item => {
                console.log("to be created mmch_Artist listcat", item);
                return (infos) => {
                    console.log("creating mmch_Artist listcat", infos);
                    return new mmch_Extrait(...infos, content = item);
                }
            }),
        ];
    }
    async mmch_searchinst(args = {}) {
        const finalArgs = { ...this.mmch_default_searchinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await Artiste.search(finalArgs);
        return [
            new mmch_Extrait(null),
            new mmch_Nation(null),
            new mmch_StyleMusical(null),
            ...items.map(item => (infos) => new mmch_Artiste(item)),
        ];
    }

    async mmch_previewinst(mminfo, parent, args = {}) {
        const finalArgs = { ...this.mmch_default_previewinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            ...items.map(item => (infos) => new mmch_Artiste(item)),
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