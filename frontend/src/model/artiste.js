import Model from "./model.js";
import Extrait from "./extrait.js";

export default class Artiste extends Model {
    #name;
    #info;
    #extraits;

    constructor({ uuid, name, info, extraits }) {
        super(uuid);
        this.#name = name;
        this.#info = info;
        this.#extraits = extraits;
    }

    static get endpoint() { return "artistes"; }

    get name() { return this.#name; }
    set name(value) { this.#name = this.validateString(value, "name"); }

    get info() { return this.#info; }
    set info(value) { this.#info = this.validateString(value, "info"); }

    async extraits(args) { return await this.fetchList(this.#extraits, Extrait, args); }

    fromJSON(json) {
        super.fromJSON(json);
        this.#name = json.name;
        this.#info = json.info;
        this.#extraits = json.extraits;
        return this;
    }

    toJSON() {
        return {
            uuid: this.uuid,
            name: this.#name,
            info: this.#info,
        };
    }
}