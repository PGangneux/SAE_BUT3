import Model from "./model.js";
import StyleMusical from "./style_musical.js";
import Extrait from "./extrait.js";
import ClientAPI from "./clientAPI.js";

export default class Artiste extends Model {
    #name;
    #info;
    #styles;
    #extraits;

    constructor({uuid,name,info, styles, extraits}){
        super(uuid);
        this.#name = name;
        this.#info = info;
        this.#styles = styles;
        this.#extraits = extraits;
    }

    static get endpoint() { return "artistes"; }

    get name() { return this.#name; }
    set name(value) { this.#name = this.validateString(value, "name"); }

    get info() { return this.#info; }
    set info(value) { this.#info = this.validateString(value, "info"); }

    async styles(args) { return await this.fetchList(this.#styles, StyleMusical, args); }

    async extraits(args) { return await this.fetchList(this.#extraits, Extrait, args); }

    /**
     * Connecte un artiste à un style musical
     * @param {StyleMusical} style_musical 
     */
    async connect_styles(style_musical) {
        await this.connect(this.#styles, {'uuid': style_musical.uuid});
    }

    /**
     * Déconnecte un artiste d'un style musical
     * @param {StyleMusical} style_musical 
     */
    async disconnect_styles(style_musical) {
        await this.disconnect(this.#styles, style_musical.uuid);
    }

    fromJSON(json) {
        super.fromJSON(json);
        this.#name = json.name;
        this.#info = json.info;
        this.#styles = json.styles;
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