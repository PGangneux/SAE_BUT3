export default class extrait_t {
    #uuid
    #titre
    #description
    #youtube_url
    #vimeo_url
    #uploaded_at
    #interview
    #question
    #tags

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

    get description() { return this.#description }
    set description(value) { this.#description = this.validateString(value, "description") }

    get youtube_url() { return this.#youtube_url }
    set youtube_url(value) { this.#youtube_url = this.validateString(value, "youtube_url") }

    get vimeo_url() { return this.#vimeo_url }
    set vimeo_url(value) { this.#vimeo_url = this.validateString(value, "vimeo_url") }

    get uploaded_at() { return this.#uploaded_at }
    set uploaded_at(value) { this.#uploaded_at = this.validateString(value, "uploaded_at") }

    get interview() { return this.#interview }
    set interview(value) { 
        this.#interview = value ; /// TODO : implement 
    }

    get question() { return this.#question }
    set question(value) { 
        this.#question = value ; /// TODO : implement 
    }

    get tags() { return this.#tags }
    set tags(value) { 
        this.#tags = value ; /// TODO : implement 
    }
}