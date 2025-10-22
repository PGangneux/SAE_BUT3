import CRUD from "./crud.js";

export default class interview_t extends CRUD {
    #titre
    #date
    #occasion
    #description
    #lieu
    #artiste
    #extraits

    validateString(value, fieldName) {
        if (value === null || value === undefined) {
            throw new Error(`${fieldName} cannot be null or undefined`)
        }
        if (typeof value !== "string") {
            throw new Error(`${fieldName} must be a string, got ${typeof value}`)
        }
        return value
    }

    constructor({uuid,
    titre,
    date,
    occasion,
    description,
    lieu,
    artiste,
    extraits,}
    ){
        super(uuid);
    this.#titre = titre;
    this.#date = date;
    this.#occasion = occasion;
    this.#description = description;
    this.#lieu = lieu;
    this.#artiste = artiste;
    this.#extraits = extraits;
    }

    get endpoint() { return "interviews" }

    get titre() { return this.#titre }
    set titre(value) { this.#titre = this.validateString(value, "titre") }

    get date() { return this.#date }
    set date(value) { this.#date = this.validateString(value, "date") }

    get occasion() { return this.#occasion }
    set occasion(value) { this.#occasion = this.validateString(value, "occasion") }

    get description() { return this.#description }
    set description(value) { this.#description = this.validateString(value, "description") }

    get lieu() { return this.#lieu }
    set lieu(value) { this.#lieu = this.validateString(value, "lieu") }

    get artiste() { return this.#artiste }
    set artiste(value) { 
        this.#artiste = value; /// TODO : implement 
    }

    get extraits() { return this.#extraits }
    set extraits(value) { 
        this.#extraits = value; /// TODO : implement 
    }

    toJSON() {
        return {
            uuid: this.uuid,
            titre: this.#titre,
            date: this.#date,
            occasion: this.#occasion,
            description: this.#description,
            lieu: this.#lieu,
            artiste: this.#artiste,
            extraits: this.#extraits
        }
    }
}