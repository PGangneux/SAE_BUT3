import Model from "./model.js";

export default class Utilisateur extends Model {
    #pseudo
    #prenom
    #nom
    #email
    #password
    #is_admin
    #recherches_artistes
    #regarder_interviews
    #regarder_extraits
    #recherches_questions

    constructor({ uuid, pseudo, prenom, nom, email, password, is_admin, recherches_artistes, regarder_interviews, regarder_extraits, recherches_questions }) {
        super(uuid);
        this.#pseudo = pseudo;
        this.#prenom = prenom;
        this.#nom = nom;
        this.#email = email;
        this.#password = password;
        this.#is_admin = is_admin;
        this.#recherches_artistes = recherches_artistes;
        this.#regarder_interviews = regarder_interviews;
        this.#regarder_extraits = regarder_extraits;
        this.#recherches_questions = recherches_questions;
    }

    static get endpoint() { return "utilisateurs" }

    get pseudo() { return this.#pseudo }
    set pseudo(value) { this.#pseudo = this.validateString(value, "pseudo") }

    get prenom() { return this.#prenom }
    set prenom(value) { this.#prenom = this.validateString(value, "prenom") }

    get nom() { return this.#nom }
    set nom(value) { this.#nom = this.validateString(value, "nom") }

    get email() { return this.#email }
    set email(value) { this.#email = this.validateString(value, "email") }

    get password() { return this.#password }
    set password(value) { this.#password = this.validateString(value, "password") } // hash à gérer côté backend

    get is_admin() { return this.#is_admin }
    set is_admin(value) { this.#is_admin = !!value }

    get recherches_artistes() { return this.fetchList(this.#recherches_artistes, null) }

    get regarder_interviews() { return this.fetchList(this.#regarder_interviews, null) }

    get regarder_extraits() { return this.fetchList(this.#regarder_extraits, null) }

    get recherches_questions() { return this.fetchList(this.#recherches_questions, null) }

    toJSON() {
        return {
            uuid: this.uuid,
            pseudo: this.#pseudo,
            prenom: this.#prenom,
            nom: this.#nom,
            email: this.#email,
            password: this.#password,
            is_admin: this.#is_admin
        }
    }
}

// import prefetcher from "./prefetcher.js";
// import CRUD from "./crud.js";

// export default class user_t extends CRUD {
//     #pseudo
//     #prenom
//     #nom
//     #email
//     #admin
//     #token

//     get endpoint() {
//         return `utilisateurs`
//     }
//     constructor(pseudo, password) {
//         const xhr = new XMLHttpRequest();
//         xhr.open("GET", BASE_URL + "/API/utilisateurs/", false);
//         xhr.send();

//         if (xhr.status !== 200) {
//             throw new Error(`HTTP error! status: ${xhr.status}`);
//         }

//         const users = JSON.parse(xhr.responseText);
//         const auth = users[0];

//         /// console.log("pseudo : " + pseudo + " password : " + password);
//         /// console.log(auth);

//         if (pseudo !== auth.prenom) {
//             throw new Error("mauvais mot de passe ou prenom");
//         }
//         super(auth.uuid);
//         this.#pseudo = auth.pseudo;
//         this.#prenom = auth.prenom;
//         this.#nom = auth.nom;
//         this.#email = auth.email;
//         this.#token = auth.uuid;
//         prefetcher.clearCache();
//     }

//     validateString(value, fieldName) {
//         if (value === null || value === undefined) {
//             throw new Error(`${fieldName} cannot be null or undefined`)
//         }
//         if (typeof value !== "string") {
//             throw new Error(`${fieldName} must be a string, got ${typeof value}`)
//         }
//         return value
//     }

//     get pseudo() { return this.#pseudo }
//     set pseudo(value) { this.#pseudo = this.validateString(value, "pseudo") }

//     get prenom() { return this.#prenom }
//     set prenom(value) { this.#prenom = this.validateString(value, "prenom") }

//     get nom() { return this.#nom }
//     set nom(value) { this.#nom = this.validateString(value, "nom") }

//     get email() { return this.#email }
//     set email(value) { this.#email = this.validateString(value, "email") }

//     get admin() { return true ; } // this.#admin }

//     get token() { return this.#token }

//     // no tojson
// }