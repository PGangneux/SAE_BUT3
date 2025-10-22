import CRUD from "./crud.js";

export default class artiste_t extends CRUD {
    #name
    #info

    validateString(value, fieldName) {
        if (value === null || value === undefined) {
            throw new Error(`${fieldName} cannot be null or undefined`)
        }
        if (typeof value !== "string") {
            throw new Error(`${fieldName} must be a string, got ${typeof value}`)
        }
        return value
    }

    constructor({uuid,name,info}){
        super(uuid);
        this.#name = name;
        this.#info = info;
    }

    get endpoint() { return "artistes" }

    get name() { return this.#name }
    set name(value) { this.#name = this.validateString(value, "name") }

    get info() { return this.#info }
    set info(value) { this.#info = this.validateString(value, "info") }

    toJSON() {
        return {
            uuid: this.uuid,
            name: this.#name,
            info: this.#info
        }
    }
}