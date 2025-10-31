import CRUD from "./crud.js";
import Theme from "./theme.js";
import Extrait from "./extrait.js";

export default class Question extends CRUD {
    #texte
    #theme
    #extraits
    #theme_uuid

    constructor({ uuid, texte, theme, extraits }) {
        super(uuid);
        this.#texte = texte;
        this.#theme = theme;
        this.#extraits = extraits;
        this.#theme_uuid = null;
    }

    static get endpoint() { return "questions" }

    get texte() { return this.#texte }
    set texte(value) { this.#texte = this.validateString(value, "texte") }

    get theme() { return this.fetchDetail(this.#theme, Theme) }
    set theme(value) { this.#theme_uuid = this.validateString(value, "theme_uuid") }

    get extraits() { return this.fetchList(this.#extraits, Extrait) }

    toJSON() {
        return {
            uuid: this.uuid,
            texte: this.#texte,
            theme_uuid: this.#theme_uuid
        }
    }
}
