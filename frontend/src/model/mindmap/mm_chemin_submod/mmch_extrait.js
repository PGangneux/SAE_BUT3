import Extrait from "../../extrait.js";
import mmch_CheminT from "./mmch_chemin.js";

export class mmch_Extrait extends mmch_CheminT {
    static mmch_dbjsclass = Extrait;
    mmch_obj;

    constructor({inst = null} = {}) {
        this.mmch_obj = inst;
    }

    static async mmch_list(args = {}) {
        const finalArgs = { ...this.mmch_default_list_args, ...args };
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            new mmch_Artiste(null),
            new mmch_Tag(null),
            new mmch_Interview(null),
            new mmch_Question(null),
            ...items.map(item => new mmch_Extrait(item)),
        ];
    }

    static async mmch_search(args = {}) {
        const finalArgs = { ...this.mmch_default_search_args, ...args };
        const items = await Extrait.search(finalArgs);
        return [
            new mmch_Artiste(null),
            new mmch_Tag(null),
            new mmch_Interview(null),
            new mmch_Question(null),
            ...items.map(item => new mmch_Extrait(item)),
        ];
    }

    mmch_getStyle(){
        return "mmLegendColorMapExtrait";
    }

    async mmch_getDescription() {
        if (!!this.mmch_obj) throw new Error("mmch description extrait on empty obj");
        const description = [];
        const extrait = this.mmch_obj;
        try {
            const question = await extrait.question();
            if (question && question.texte) {
                description.push(`Question: ${question.texte.substring(0, 50)}...`);
            }
        } catch (error) { console.warn(error); }

        try {
            const artiste = await extrait.artiste();
            if (artiste && artiste.name) description.push(`Artiste: ${artiste.name}`);
        } catch (error) { console.warn(error); }


        if (extrait.uploaded_at) {
            description.push(`Ajouté le: ${new Date(extrait.uploaded_at).toLocaleDateString()}`);
        }

        if (extrait.duree) {
            const minutes = Math.floor(extrait.duree / 60);
            const seconds = extrait.duree % 60;
            description.push(`Durée: ${minutes}:${seconds.toString().padStart(2, '0')}`);
        }

        try {
            const tags = await extrait.tags({ limit: 3 });
            if (tags.length > 0) {
                const tagNames = tags.map(t => t.name).join(', ');
                description.push(`Tags: ${tagNames}`);
            }
        } catch (error) { console.warn(error); }

        return description.length > 0 ? description : ["no description extrait"];
    }

    mmch_hasPreview() {
        if (!!this.mmch_obj) return null;
        const extrait = this.mmch_obj;
        return !!(extrait.youtube_url || extrait.vimeo_url);
    }

    async mmch_getPreview() {
        if (!!this.mmch_obj) throw new Error("mmch mmch_getPreview Extrait on empty obj");
        const extrait = this.mmch_obj;
        if (extrait.youtube_url) {
            return extrait.url_miniature_yt;
        } else if (extrait.vimeo_url) {
            return await extrait.get_url_miniature_vimeo();
        } else {
            throw new Error("unreachable Extrait doesn't have url");
        }
    }
}