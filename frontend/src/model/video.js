export default class extrait_t {
    #uuid
    #url
    #param_visible
    #pos_x_iframe
    #pos_y_iframe
    #lecteur

    validateString(value, fieldName) {
        if (value === null || value === undefined) {
            throw new Error(`${fieldName} cannot be null or undefined`)
        }
        if (typeof value !== "string") {
            throw new Error(`${fieldName} must be a string, got ${typeof value}`)
        }
        return value
    }

    validateBoolean(value, fieldName) {
        if (typeof value !== "boolean") {
            throw new Error(`${fieldName} must be a boolean, got ${typeof value}`)
        }
        return value
    }

    validateNumber(value, fieldName) {
        if (typeof value !== "number") {
            throw new Error(`${fieldName} must be a number, got ${typeof value}`)
        }
        return value
    }

    get uuid() { return this.#uuid }
    set uuid(value) { this.#uuid = this.validateString(value, "uuid") }

    get url() { return this.#url }
    set url(value) { this.#url = this.validateString(value, "url") }

    get param_visible() { return this.#param_visible }
    set param_visible(value) { this.#param_visible = this.validateBoolean(value, "param_visible") }

    get pos_x_iframe() { return this.#pos_x_iframe }
    set pos_x_iframe(value) { this.#pos_x_iframe = this.validateNumber(value, "pos_x_iframe") }

    get pos_y_iframe() { return this.#pos_y_iframe }
    set pos_y_iframe(value) { this.#pos_y_iframe = this.validateNumber(value, "pos_y_iframe") }

    get lecteur() { return this.#lecteur }
    set lecteur(value) { this.#lecteur = this.validateString(value, "lecteur") }

    constructor() {
        this.param_visible = false
        this.pos_x_iframe = 0
        this.pos_y_iframe = 0
        this.lecteur = 'Viméo'
        this.url = "https://player.vimeo.com/video/1128762950?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
    }
}