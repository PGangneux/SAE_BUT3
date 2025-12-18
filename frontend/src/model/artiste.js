import Model from "./model.js";
import Nation from "./nation.js";
import Extrait from "./extrait.js";

export default class Artiste extends Model {
    #name;
    #info;
    #nation;
    #extraits;
    #nation_uuid;

    constructor({ uuid, name, info, nation, extraits }) {
        super(uuid);
        this.#name = name;
        this.#info = info;
        this.#nation = nation;
        this.#extraits = extraits;
        this.#nation_uuid = null;
    }

    static get endpoint() { return "artistes"; }

    get name() { return this.#name; }
    set name(value) { this.#name = this.validateString(value, "name"); }

    get info() { return this.#info; }
    set info(value) { this.#info = this.validateString(value, "info"); }

    get nation() { return this.fetchDetail(this.#nation, Nation); }
    set nation(value) { this.#nation_uuid = this.validateString(value, "nation_uuid"); }

    async extraits(args) { return await this.fetchList(this.#extraits, Extrait, args); }

    fromJSON(json) {
        super.fromJSON(json);
        this.#name = json.name;
        this.#info = json.info;
        this.#nation = json.nation;
        this.#extraits = json.extraits;
        return this;
    }

    toJSON() {
        return {
            uuid: this.uuid,
            name: this.#name,
            info: this.#info,
            nation_uuid: this.#nation_uuid,
        };
    }
}