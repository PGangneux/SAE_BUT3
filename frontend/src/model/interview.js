export default class interview_t {
    #uuid
    #titre
    #date
    #occasion
    #description
    #lieu
    #artiste
    #extraits

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

    get titre() { return this.#titre }
    set titre(value) { this.#titre = this.validateString(value, "titre") }

    get date() { return this.#date }
    set date(value) { this.#date = this.validateString(value, "date") }

    get occasion() { return this.#occasion }
    set occasion(value) { this.#occasion = this.validateString(value, "occasion") }

    get description() { return this.#description }
    set description(value) { this.#description = this.validateString(value, "description") }

    get lieu() { return this.#lieu }
    set lieu(value) { this.#lieu = this.validateString(value, "lieu") }

    get artiste() { return this.#artiste }
    set artiste(value) { 
        this.#artiste = value ; /// TODO : implement 
    }

    get extraits() { return this.#extraits }
    set extraits(value) { 
        this.#extraits = value ; /// TODO : implement 
    }

    create() {
        // todo : todo
    }
    update() {
        // todo : todo
    }
    delete() {
        // todo : todo
    }
}