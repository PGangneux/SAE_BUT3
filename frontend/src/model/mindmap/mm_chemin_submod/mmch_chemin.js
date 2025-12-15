export class mmch_CheminT {
    static mmch_dbjsclass = null;
    static mmch_default_list_args = { limit: 5 };
    static mmch_default_search_args = { limit: 5 };
    mmch_obj;
    
    constructor(obj) {
        if (new.target === mmch_CheminT) {
            throw new Error("Cannot instantiate abstract class mmch_CheminT");
        }
    }
    
    static async mmch_list(args = {}) {
        throw new Error("mmch_list must be defined in child");
    }
    
    static async mmch_search(args = {}) {
        throw new Error("mmch_search must be defined in child");
    }
    
    async mmch_getTitle() {
        const obj = this.mmch_obj;
        if (obj.name) return obj.name;
        if (obj.titre) return obj.titre;
        if (obj.pseudo) return obj.pseudo;
        return "Sans titre";
    }
    
    async mmch_getDescription() {
        return ["no description"];
    }
    
    mmch_hasPreview() {
        return false;
    }
}