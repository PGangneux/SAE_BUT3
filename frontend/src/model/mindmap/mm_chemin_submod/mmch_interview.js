import Interview from "../../interview.js";
import mmch_CheminT from "./mmch_chemin.js";

export default class mmch_Interview extends mmch_CheminT {
    static mmch_dbjsclass = Interview;
    mmch_obj;
    #_previewurl;

    constructor({ inst = null } = {}) {
        this.mmch_obj = inst;
        this._previewurl = null;
    }

    static async mmch_list(args = {}) {
        const finalArgs = { ...this.mmch_default_list_args, ...args };
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            new mmch_Extrait(null),
            new mmch_Tag(null),
            ...items.map(item => new mmch_Interview(item)),
        ];
    }

    static async mmch_search(args = {}) {
        const finalArgs = { ...this.mmch_default_search_args, ...args };
        const items = await Interview.search(finalArgs);
        return [
            new mmch_Extrait(null),
            new mmch_Tag(null),
            ...items.map(item => new mmch_Interview(item)),
        ];
    }

    static async mmch_Preview(mminfo,parent,args = {}){
        const finalArgs = { ...this.mmch_default_preview_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            ...items.map(item => new mmch_Interview(item)),
        ];
    }

    mmch_getStyle(){
        return "mmLegendColorMapInterview";
    }

    async mmch_getDescription() {
        if (!!this.mmch_obj) throw new Error("mmch description interview on empty obj");
        const description = [];
        const interview = this.mmch_obj;

        if (interview.date) description.push(`Date: ${new Date(interview.date).toLocaleDateString()}`);
        if (interview.lieu) description.push(`Lieu: ${interview.lieu}`);
        if (interview.occasion) description.push(`Occasion: ${interview.occasion}`);

        try {
            const tags = await interview.tags({ limit: 3 });
            if (tags.length > 0) {
                const tagNames = tags.map(t => t.name).join(', ');
                description.push(`Tags: ${tagNames}`);
            }
        } catch (error) { console.warn(error); }

        return description.length > 0 ? description : ["no description interview"];
    }

    async #get_url(){
        if (!!this.mmch_obj) return null;
        if (this.#_previewurl) return this.#_previewurl;
        const interview = this.mmch_obj;

        const extraits = await interview.extraits();
        if (!extraits || extraits.length === 0) {
            console.warn(`Aucun extrait trouvé pour l'interview ${interview}`);
            return null;
        }

        const extrait = extraits[0];
        if (!extrait) {
            console.warn(`Extrait null pour l'interview ${interview}`);
            return null;
        }

        if (extrait.youtube_url) {
            this.#_previewurl = extrait.url_miniature_yt;
        } else if (extrait.vimeo_url) {
            this.#_previewurl = await extrait.get_url_miniature_vimeo();
        } else {
            throw new Error("unreachable Extrait doesn't have url");
        }
        return this.#_previewurl;
    }

    async mmch_hasMiniature() {
        if (!!this.mmch_obj) return null;
        return await this.#get_url() != null;
    }

    async mmch_getMiniature() {
        if (!!this.mmch_obj) throw new Error("mmch mmch_Preview interview on empty obj");
        return await this.#get_url();
    }
}