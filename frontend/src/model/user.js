import BASE_URL from "../config.js";
export default class user_t {
    #uuid
    #pseudo
    #prenom
    #nom
    #email
    #admin
    #token

    constructor() {
    }

    authenticate(pseudo,password){
        return fetch(BASE_URL + "/API/utilisateurs/",{method : "GET"}).then( u => {
            this.uuid = u.uuid;
            this.pseudo = u.pseudo;
            this.prenom = u.prenom;
            this.nom = u.nom;
            this.email = u.email;
            this.token = u.uuid ;
        }
        ).catch(err => 0);
    }

    validateString(value, fieldName) {
        if (value === null || value === undefined) {
            throw new Error(`${fieldName} cannot be null or undefined`)
        }
        if (typeof value !== "string") {
            throw new Error(`${fieldName} must be a string, got ${typeof value}`)
        }
        return value
    }

    // Getters and Setters
    get uuid() { return this.#uuid }
    set uuid(value) { this.#uuid = this.validateString(value, "uuid") }

    get pseudo() { return this.#pseudo }
    set pseudo(value) { this.#pseudo = this.validateString(value, "pseudo") }

    get prenom() { return this.#prenom }
    set prenom(value) { this.#prenom = this.validateString(value, "prenom") }

    get nom() { return this.#nom }
    set nom(value) { this.#nom = this.validateString(value, "nom") }

    get email() { return this.#email }
    set email(value) { this.#email = this.validateString(value, "email") }
}