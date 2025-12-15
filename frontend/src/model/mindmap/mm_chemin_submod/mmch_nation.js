import Nation from "../../nation.js";
import mmch_CheminT from "./mmch_chemin.js";

export default class mmch_Nation extends mmch_CheminT {
    static mmch_dbjsclass = Nation;
    mmch_obj;

    constructor({inst = null} = {}) {
        this.mmch_obj = inst;
    }

    static async mmch_list(args = {}) {
        const finalArgs = { ...this.mmch_default_list_args, ...args };
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            new mmch_Artiste(null),
            ...items.map(item => new mmch_Nation(item)),
        ];
    }

    static async mmch_search(args = {}) {
        const finalArgs = { ...this.mmch_default_search_args, ...args };
        const items = await Nation.search(finalArgs);
        return [
            new mmch_Artiste(null),
            ...items.map(item => new mmch_Nation(item)),
        ];
    }

    mmch_getStyle(){
        return "mmLegendColorMapNation";
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