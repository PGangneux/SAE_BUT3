import Model from "./model.js";
import Interview from "./interview.js";
import Extrait from "./extrait.js";

export default class Tag extends Model {
    #name
    #interviews
    #extraits

    constructor({ uuid, name, interviews, extraits }) {
        super(uuid);
        this.#name = name;
        this.#interviews = interviews;
        this.#extraits = extraits;
    }

    static get endpoint() { return "tags" }

    get name() { return this.#name }
    set name(value) { this.#name = this.validateString(value, "name") }

    get interviews() { return this.fetchList(this.#interviews, Interview) }

    get extraits() { return this.fetchList(this.#extraits, Extrait) }

    fromJSON(json) {
        super.fromJSON(json);
        this.#name = json.name;
        this.#interviews = json.interviews;
        this.#extraits = json.extraits;
        return this
    }

    toJSON() {
        return {
            uuid: this.uuid,
            name: this.#name,
        }
    }
}
