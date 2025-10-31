import CRUD from "./crud.js";
import Artiste from "./artiste.js";

export default class Nation extends CRUD {
    #name
    #artistes

    constructor({uuid, name, artistes}) {
        super(uuid);
        this.#name = name;
        this.#artistes = artistes;
    }

    static get endpoint() { return "nations" }

    get name() { return this.#name }
    set name(value) { this.#name = this.validateString(value, "name") }

    get artistes() { return this.fetchList(this.#artistes, Artiste) }

    toJSON() {
        return {
            uuid: this.uuid,
            name: this.#name,
        }
    }
}
