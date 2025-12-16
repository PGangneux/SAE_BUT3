import Extrait from "../../extrait.js";
import mmch_CheminT from "./mmch_chemin.js";
import mmch_Artiste from "./mmch_artiste.js";
import mmch_Tag from "./mmch_tag.js";
import mmch_Interview from "./mmch_interview.js";
import mmch_Question from "./mmch_question.js";

export default class mmch_Extrait extends mmch_CheminT {
    static mmch_dbjsclass = Extrait;
    /** @type {Extrait} */
    mmch_obj;
    #_previewurl = null;

    async mmch_listinst(args = {}) {
        const finalArgs = { ...this.mmch_default_listinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await Extrait.list(finalArgs);
        return [
            new mmch_Artiste(null),
            new mmch_Tag(null),
            new mmch_Interview(null),
            new mmch_Question(null),
            ...items.map(item => new mmch_Extrait(item)),
        ];
    }

    async mmch_searchinst(args = {}) {
        const finalArgs = { ...this.mmch_default_searchinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await Extrait.list(finalArgs);
        return [
            new mmch_Artiste(null),
            new mmch_Tag(null),
            new mmch_Interview(null),
            new mmch_Question(null),
            ...items.map(item => new mmch_Extrait(item)),
        ];
    }

    async mmch_previewinst(mminfo, parent, args = {}) {
        const finalArgs = { ...this.mmch_default_previewinst_args, ...args };
        // TODO : put recomendation algorithm here
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return [
            ...items.map(item => new mmch_Extrait(item)),
        ];
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

    async #get_url() {
        if (!!this.mmch_obj) return null;
        if (this.#_previewurl) return this.#_previewurl;
        const extrait = this.mmch_obj;
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
        if (!!this.mmch_obj) throw new Error("mmch mmch_getMiniature Extrait on empty obj");
        return await this.#get_url();
    }
}