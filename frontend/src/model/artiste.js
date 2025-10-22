export default class artiste_t {
    #uuid
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

    // Getters and Setters
    get uuid() { return this.#uuid }
    set uuid(value) { this.#uuid = this.validateString(value, "uuid") }

    get name() { return this.#name }
    set name(value) { this.#name = this.validateString(value, "name") }

    get info() { return this.#info }
    set info(value) { this.#info = this.validateString(value, "info") }
}