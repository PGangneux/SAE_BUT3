import Extrait from "../../extrait.js";
import StyleMusical from "../../style_musical.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Artiste from "./mmch_artiste.js";

export default class mmch_StyleMusical extends mmch_CheminT {
    static mmch_dbjsclass = StyleMusical;
    /** @type {StyleMusical} */
    mmch_obj;

    async mmch_listinst(args = {}) {
        const finalArgs = { ...this.mmch_default_listinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await Extrait.list(finalArgs);
        return [
            new mmch_Artiste(null),
            ...items.map(item => (infos) => new mmch_StyleMusical(item)),
        ];
    }

    async mmch_searchinst(args = {}) {
        const finalArgs = { ...this.mmch_default_searchinst_args, ...args };
        const items = await this.mmch_dbjsclass.search(finalArgs);
        return [
            new mmch_Artiste(null),
            ...items.map(item => (infos) => new mmch_StyleMusical(item)),
        ];
    }

    async mmch_previewinst(mminfo, parent, args = {}) {
        const finalArgs = { ...this.mmch_default_previewinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            ...items.map(item => (infos) => new mmch_StyleMusical(item)),
        ];
    }

    async mmch_getDescription() {
        if (!!this.mmch_obj) throw new Error("mmch mmch_getTitle style musical on empty obj");
        return "";
    }
}