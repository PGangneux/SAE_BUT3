import Model from "./model.js";
import Question from "./question.js";

export default class Theme extends Model {
    #name
    #description
    #questions

    constructor({ uuid, name, description, questions }) {
        super(uuid);
        this.#name = name;
        this.#description = description;
        this.#questions = questions;
    }

    static get endpoint() { return "themes" }

    get name() { return this.#name }
    set name(value) { this.#name = this.validateString(value, "name") }

    get description() { return this.#description }
    set description(value) { this.#description = this.validateString(value, "description") }

    get questions() { return this.fetchList(this.#questions, Question) }

    toJSON() {
        return {
            uuid: this.uuid,
            name: this.#name,
            description: this.#description
        }
    }
}
