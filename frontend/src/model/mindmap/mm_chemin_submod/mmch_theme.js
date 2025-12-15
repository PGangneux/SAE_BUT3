import Theme from "../../theme.js";
import mmch_CheminT from "./mmch_chemin.js";

export class mmch_Theme extends mmch_CheminT {
    static mmch_dbjsclass = Theme;
    mmch_obj;

    constructor({inst = null} = {}) {
        this.mmch_obj = inst;
    }

    static async mmch_list(args = {}) {
        const finalArgs = { ...this.mmch_default_list_args, ...args };
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            new mmch_Question(),
            ...items.map(item => new mmch_Theme(item)),
        ];
    }

    static async mmch_search(args = {}) {
        const finalArgs = { ...this.mmch_default_search_args, ...args };
        const items = await Theme.search(finalArgs);
        return [
            new mmch_Question(),
            ...items.map(item => new mmch_Theme(item)),
        ];
    }

    mmch_getStyle(){
        return "mmLegendColorMapTheme";
    }

    async mmch_getDescription() {
        if (!!this.mmch_obj) throw new Error("mmch description theme on empty obj");
        const description = [];
        const theme = this.mmch_obj;
        if (theme.description) description.push(theme.description.substring(0, 100) + "...");

        return description.length > 0 ? description : ["no description theme"];
    }
}