import CRUD from "./crud.js";

export default class question_t extends CRUD {
    #texte
    #theme

    validateString(value, fieldName) {
        if (value === null || value === undefined) {
            throw new Error(`${fieldName} cannot be null or undefined`)
        }
        if (typeof value !== "string") {
            throw new Error(`${fieldName} must be a string, got ${typeof value}`)
        }
        return value
    }

    constructor({uuid,texte,theme}){
        super(uuid);
        this.#texte = texte;
        this.#theme = theme;
    }

    get endpoint() { return "questions" }

    get texte() { return this.#texte }
    set texte(value) { this.#texte = this.validateString(value, "texte") }

    get theme() { return this.#theme }
    set theme(value) { 
        this.#theme = value; /// TODO : implement 
    }

    toJSON() {
        return {
            uuid: this.uuid,
            texte: this.#texte,
            theme: this.#theme
        }
    }
}