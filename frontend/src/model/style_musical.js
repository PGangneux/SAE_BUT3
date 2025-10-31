import Model from "./model.js";
import Artiste from "./artiste.js";

export default class StyleMusical extends Model {
    #name
    #artistes

    constructor({uuid, name, artistes}) {
        super(uuid);
        this.#name = name;
        this.#artistes = artistes;
    }

    static get endpoint() { return "styles-musicaux" }

    get name() { return this.#name }
    set name(value) { this.#name = this.validateString(value, "name") }

    get artistes() { return this.fetchList(this.#artistes, Artiste) }

    fromJSON(json) {
        super.fromJSON(json);
        this.#name = json.name;
        this.#artistes = json.artistes;
        return this
    }

    toJSON() {
        return {
            uuid: this.uuid,
            name: this.#name,
        }
    }
}
