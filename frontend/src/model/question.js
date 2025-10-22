export default class question_t {
    #uuid
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

    // Getters and Setters
    get uuid() { return this.#uuid }
    set uuid(value) { this.#uuid = this.validateString(value, "uuid") }

    get texte() { return this.#texte }
    set texte(value) { this.#texte = this.validateString(value, "texte") }

    get theme() { return this.#theme }
    set theme(value) { 
        this.#theme = value ; /// TODO : implement 
    }
}