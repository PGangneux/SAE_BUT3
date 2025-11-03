import Model from "./model.js";
import Extrait from "./extrait.js";
import Tag from "./tag.js";

export default class Interview extends Model {
    #titre;
    #date;
    #occasion;
    #description;
    #lieu;
    #extraits;
    #tags;

    constructor({ uuid, titre, date, occasion, description, lieu, extraits, tags }) {
        super(uuid);
        this.#titre = titre;
        this.#date = date;
        this.#occasion = occasion;
        this.#description = description;
        this.#lieu = lieu;
        this.#extraits = extraits;
        this.#tags = tags;
    }

    static get endpoint() { return "interviews"; }

    get titre() { return this.#titre; }
    set titre(value) { this.#titre = this.validateString(value, "titre"); }

    get date() { return this.#date; }
    set date(value) { this.#date = value; }

    get occasion() { return this.#occasion; }
    set occasion(value) { this.#occasion = this.validateString(value, "occasion"); }

    get description() { return this.#description; }
    set description(value) { this.#description = this.validateString(value, "description"); }

    get lieu() { return this.#lieu; }
    set lieu(value) { this.#lieu = this.validateString(value, "lieu"); }

    get extraits() { return this.fetchList(this.#extraits, Extrait); }

    get tags() { return this.fetchList(this.#tags, Tag); }

    /**
     * Connecte une interview à un tag
     * @param {Tag} tag 
     */
    async connect_tag(tag) {
        await this.connect(this.#tags, {'uuid': tag.uuid});
    }

    /**
     * Déconnecte une interview d'un tag
     * @param {Tag} tag 
     */
    async disconnect_tag(tag) {
        await this.disconnect(this.#tags, tag);
    }

    fromJSON(json) {
        super.fromJSON(json);
        this.#titre = json.titre;
        this.#date = json.date;
        this.#occasion = json.occasion;
        this.#description = json.description;
        this.#lieu = json.lieu;
        this.#extraits = json.extraits;
        this.#tags = json.tags;
        return this;
    }

    toJSON() {
        return {
            uuid: this.uuid,
            titre: this.#titre,
            date: this.#date,
            occasion: this.#occasion,
            description: this.#description,
            lieu: this.#lieu,
        };
    }
}
