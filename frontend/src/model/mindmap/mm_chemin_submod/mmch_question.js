import Extrait from "../../extrait.js";
import Question from "../../question.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Extrait from "./mmch_extrait.js";
import mmch_Theme from "./mmch_theme.js";

export default class mmch_Question extends mmch_CheminT {
    static mmch_dbjsclass = Question;
    /** @type {Question} */
    mmch_obj;

    async mmch_listinst(args = {}) {
        const finalArgs = { ...this.mmch_default_listinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await Extrait.list(finalArgs);
        return [
            new mmch_Extrait(null),
            new mmch_Theme(null),
            ...items.map(item => (infos) => new mmch_Question(item)),
        ];
    }

    async mmch_searchinst(args = {}) {
        const finalArgs = { ...this.mmch_default_searchinst_args, ...args };
        const items = await this.mmch_dbjsclass.search(finalArgs);
        return [
            new mmch_Extrait(null),
            new mmch_Theme(null),
            ...items.map(item => (infos) => new mmch_Question(item)),
        ];
    }

    async mmch_previewinst(mminfo, parent, args = {}) {
        const finalArgs = { ...this.mmch_default_previewinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            ...items.map(item => (infos) => new mmch_Question(item)),
        ];
    }

    async mmch_getTitle() {
        if (!!this.mmch_obj) throw new Error("mmch mmch_getTitle question on empty obj");
        const question = this.mmch_obj;
        return question.texte.substring(0, 50);
    }

    async mmch_getDescription() {
        if (!!this.mmch_obj) throw new Error("mmch description question on empty obj");
        const description = [];
        const question = this.mmch_obj;
        try {
            const theme = await question.theme();
            if (theme && theme.name) description.push(`Thème: ${theme.name}`);
        } catch (error) { console.warn(error); }

        return description.length > 0 ? description : ["no description question"];
    }
}