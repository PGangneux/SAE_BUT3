import Tag from "../../tag.js";
import mmch_CheminT from "./mmch_chemin.js";

export class mmch_Tag extends mmch_CheminT {
    static mmch_dbjsclass = Tag;
    mmch_obj;

    constructor(tag) {
        this.mmch_obj = tag;
    }
    
    static async mmch_list(args = {}) {
        const finalArgs = { ...this.mmch_default_list_args, ...args };
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return items.map(item => new mmch_Tag(item));
    }

    static async mmch_search(query, args = {}) {
        const finalArgs = { ...this.mmch_default_search_args, ...args };
        const tags = await Tag.search(query, finalArgs);
        return tags.map(t => new mmch_Tag(t));
    }
    
    async mmch_getDescription() {
        return "";
        const description = [];
        const tag = this.mmch_obj;
        
        return description.length > 0 ? description : ["no description tag"];
    }
}