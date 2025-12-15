import Question from "../../question.js";
import mmch_CheminT from "./mmch_chemin.js";

export default class mmch_Question extends mmch_CheminT {
    static mmch_dbjsclass = Question;
    mmch_obj;

    constructor({inst = null} = {}) {
        this.mmch_obj = inst;
    }

    static async mmch_list(args = {}) {
        const finalArgs = { ...this.mmch_default_list_args, ...args };
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            new mmch_Extrait(null),
            new mmch_Theme(null),
            ...items.map(item => new mmch_Question(item)),
        ];
    }

    static async mmch_search(args = {}) {
        const finalArgs = { ...this.mmch_default_search_args, ...args };
        const items = await Question.search(finalArgs);
        return [
            new mmch_Extrait(null),
            new mmch_Theme(null),
            ...items.map(item => new mmch_Question(item)),
        ];
    }

    mmch_getStyle(){
        return "mmLegendColorMapQuestion";
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