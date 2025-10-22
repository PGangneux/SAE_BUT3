import { BASE_URL, prefetcher } from "./prefetcher.js";
import CRUD from "./crud.js";

export default class user_t extends CRUD {
    #pseudo
    #prenom
    #nom
    #email
    #admin
    #token

    get endpoint() {
        return `utilisateurs`
    }
    constructor(pseudo, password) {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", BASE_URL + "/API/utilisateurs/", false);
        xhr.send();

        if (xhr.status !== 200) {
            throw new Error(`HTTP error! status: ${xhr.status}`);
        }

        const users = JSON.parse(xhr.responseText);
        const auth = users[0];

        /// console.log("pseudo : " + pseudo + " password : " + password);
        /// console.log(auth);

        if (pseudo !== auth.prenom) {
            throw new Error("mauvais mot de passe ou prenom");
        }
        super(auth.uuid);
        this.#pseudo = auth.pseudo;
        this.#prenom = auth.prenom;
        this.#nom = auth.nom;
        this.#email = auth.email;
        this.#token = auth.uuid;
        prefetcher.clearCache();
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

    get pseudo() { return this.#pseudo }
    set pseudo(value) { this.#pseudo = this.validateString(value, "pseudo") }

    get prenom() { return this.#prenom }
    set prenom(value) { this.#prenom = this.validateString(value, "prenom") }

    get nom() { return this.#nom }
    set nom(value) { this.#nom = this.validateString(value, "nom") }

    get email() { return this.#email }
    set email(value) { this.#email = this.validateString(value, "email") }

    get admin() { return true ; } // this.#admin }

    get token() { return this.#token }

    // no tojson
}