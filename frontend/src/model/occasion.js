import Model from "./model.js";
import Interview from "./interview.js";

export default class Occasion extends Model {
    #name;
    #interviews;

    constructor({ uuid, name, artistes }) {
        super(uuid);
        this.#name = name;
        this.#interviews = artistes;
    }

    static get endpoint() { return "occasions"; }

    get name() { return this.#name; }
    set name(value) { this.#name = this.validateString(value, "name"); }

    async interviews(args) { return await this.fetchList(this.#interviews, Interview, args); }

    fromJSON(json) {
        super.fromJSON(json);
        this.#name = json.name;
        this.#interviews = json.interviews;
        return this;
    }

    toJSON(json = {}) {
        json = super.toJSON(json)
        if (this.name) json['name'] = this.name;
        return json;
    }
}
