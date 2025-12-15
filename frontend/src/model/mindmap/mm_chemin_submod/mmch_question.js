import Question from "../../question.js";
import mmch_CheminT from "./mmch_chemin.js";

export class mmch_Question extends mmch_CheminT {
    static mmch_dbjsclass = Question;
    mmch_obj;

    constructor(question) {
        this.mmch_obj = question;
    }
    
    static async mmch_list(args = {}) {
        const finalArgs = { ...this.mmch_default_list_args, ...args };
        const items = await this.mmch_dbjsclass.list(finalArgs);
        return items.map(item => new mmch_Question(item));
    }

    static async mmch_search(query, args = {}) {
        const finalArgs = { ...this.mmch_default_search_args, ...args };
        const questions = await Question.search(query, finalArgs);
        return questions.map(q => new mmch_Question(q));
    }
    
    async mmch_getTitle(){
        const question = this.mmch_obj;
        return question.texte.substring(0, 50);
    }

    async mmch_getDescription() {
        const description = [];
        const question = this.mmch_obj;
        try {
            const theme = await question.theme();
            if (theme && theme.name) description.push(`Thème: ${theme.name}`);
        } catch (error) {console.warn(error);}
        
        return description.length > 0 ? description : ["no description question"];
    }
}