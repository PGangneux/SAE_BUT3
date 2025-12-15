import Interview from "../../interview.js";
import mmch_CheminT from "./mmch_chemin.js";

export class mmch_Interview extends mmch_CheminT {
    static mmch_dbjsclass = Interview;
    mmch_obj;

    constructor(interview) {
        this.mmch_obj = interview;
    }
    
    static async mmch_list(args = {}) {
        const finalArgs = { ...this.mmch_default_list_args, ...args };
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return items.map(item => new mmch_Interview(item));
    }

    static async mmch_search(query, args = {}) {
        const finalArgs = { ...this.mmch_default_search_args, ...args };
        const interviews = await Interview.search(query, finalArgs);
        return interviews.map(i => new mmch_Interview(i));
    }
    
    async mmch_getDescription() {
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
        } catch (error) {console.warn(error);}
        
        return description.length > 0 ? description : ["no description interview"];
    }
}