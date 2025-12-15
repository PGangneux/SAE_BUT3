import StyleMusical from "../../style_musical.js";
import mmch_CheminT from "./mmch_chemin.js";

export class mmch_StyleMusical extends mmch_CheminT {
    static mmch_dbjsclass = StyleMusical;
    mmch_obj;

    constructor(style) {
        this.mmch_obj = style;
    }
    
    static async mmch_list(args = {}) {
        const finalArgs = { ...this.mmch_default_list_args, ...args };
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return items.map(item => new mmch_StyleMusical(item));
    }

    static async mmch_search(query, args = {}) {
        const finalArgs = { ...this.mmch_default_search_args, ...args };
        const styles = await StyleMusical.search(query, finalArgs);
        return styles.map(s => new mmch_StyleMusical(s));
    }
    
    async mmch_getDescription() {
        return "";
        const description = [];
        const style = this.mmch_obj;
        
        return description.length > 0 ? description : ["no description style musical"];
    }
}