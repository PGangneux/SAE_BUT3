import CRUD from "./crud.js";

export default class theme_t extends CRUD {
    #name
    #description
    #questions

    validateString(value, fieldName) {
        if (value === null || value === undefined) {
            throw new Error(`${fieldName} cannot be null or undefined`)
        }
        if (typeof value !== "string") {
            throw new Error(`${fieldName} must be a string, got ${typeof value}`)
        }
        return value
    }

    constructor({uuid,name,description,questions}){
        super(uuid);
        this.#name = name;
        this.#description = description;
        this.#questions = questions;
    }

    get endpoint() { return "themes" }

    get name() { return this.#name }
    set name(value) { this.#name = this.validateString(value, "name") }

    get description() { return this.#description }
    set description(value) { this.#description = this.validateString(value, "description") }

    get questions() { return this.#questions }
    set questions(value) { 
        this.#questions = value; /// TODO : implement
    }

    toJSON() {
        return {
            uuid: this.uuid,
            name: this.#name,
            description: this.#description,
            questions: this.#questions
        }
    }
}