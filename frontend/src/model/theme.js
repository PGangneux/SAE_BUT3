import Model from "./model.js";
import Question from "./question.js";

export default class Theme extends Model {
    #name;
    #description;
    #questions;

    constructor({ uuid, name, description, questions }) {
        super(uuid);
        this.#name = name;
        this.#description = description;
        this.#questions = questions;
    }

    static get endpoint() { return "themes"; }

    get name() { return this.#name; }
    set name(value) { this.#name = this.validateString(value, "name"); }

    get description() { return this.#description; }
    set description(value) { this.#description = this.validateString(value, "description"); }

    async questions(args) { return await this.fetchList(this.#questions, Question, args); }

    fromJSON(json) {
        super.fromJSON(json);
        this.#name = json.name;
        this.#description = json.description;
        this.#questions = json.questions;
        return this;
    }

    toJSON(json = {}) {
        json = super.toJSON(json)
        if (this.name) json['name'] = this.name;
        if (this.description) json['description'] = this.description;
        return json;
    }
}
