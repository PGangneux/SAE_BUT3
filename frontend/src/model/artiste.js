import CRUD from "./crud.js";
import Nation from "./nation.js";
import StyleMusical from "./style_musical.js";
import Extrait from "./extrait.js";

export default class Artiste extends CRUD {
    #name
    #info
    #nation
    #styles
    #extraits
    #nation_uuid

    constructor({uuid,name,info, nation, styles, extraits}){
        super(uuid);
        this.#name = name;
        this.#info = info;
        this.#nation = nation;
        this.#styles = styles;
        this.#extraits = extraits;
        this.#nation_uuid = null;
    }

    get endpoint() { return "artistes" }

    get name() { return this.#name }
    set name(value) { this.#name = this.validateString(value, "name") }

    get info() { return this.#info }
    set info(value) { this.#info = this.validateString(value, "info") }

    get nation() { return this.fetchDetail(this.#nation, Nation); }
    set nation(value) { this.#nation_uuid = this.validateString(value, "nation_uuid") }

    get styles() { return this.fetchList(this.#styles, StyleMusical) }

    get extraits() { return this.fetchList(this.#extraits, Extrait) }

    toJSON() {
        return {
            uuid: this.uuid,
            name: this.#name,
            info: this.#info,
            nation_uuid: this.#nation_uuid,
        }
    }
}