export default class mmch_CheminT {
    static mmch_dbjsclass = null;
    
    static mmch_default_listcat_args = { limit: 5 };
    static mmch_default_listinst_args = { limit: 5 };
    
    static mmch_default_searchcat_args = { limit: 5 };
    static mmch_default_searchinst_args = { limit: 5 };
    
    static mmch_default_previewcat_args = { limit: 1 };
    static mmch_default_previewinst_args = { limit: 1 };
    mmch_obj;

    constructor({obj} = {}) {
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

    static async mmch_Preview(mminfo,parent,args = {}){
        throw new Error("mmch_Preview must be defined in child");
    }

    toJSON() {
        return {
            mmch_dbjsclass: this.mmch_dbjsclass,
            mmch_obj: this.mmch_obj,
        };
    }

    mmch_getStyle(){
        return `mmLegendColorMap${this.mmch_dbjsclass.name}`;
    }

    async mmch_getTitle() {
        if (!!this.mmch_obj) throw new Error("mmch mmch_getTitle generic on empty obj");
        const obj = this.mmch_obj;
        if (obj.name) return obj.name;
        if (obj.titre) return obj.titre;
        if (obj.pseudo) return obj.pseudo;
        return "Sans titre";
    }

    async mmch_getDescription() {
        console.warn("mmch_getDescription generic");
        return ["no description"];
    }

    async mmch_hasMiniature() {
        return false;
    }

    async mmch_getMiniature() {
        throw new Error("mmch_getMiniature must be defined in child");
    }
}