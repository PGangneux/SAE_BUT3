import Artiste from "./artiste.js";
import Extrait from "./extrait.js";
import Interview from "./interview.js";
import Model from "./model.js";
import Question from "./question.js";

export default class Utilisateur extends Model {
    #pseudo;
    #prenom;
    #nom;
    #email;
    #password;
    #is_admin;
    #recherches_artistes;
    #regarder_interviews;
    #regarder_extraits;
    #recherches_questions;

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

    static get endpoint() { return "utilisateurs"; }

    get pseudo() { return this.#pseudo; }
    set pseudo(value) { this.#pseudo = this.validateString(value, "pseudo"); }

    get prenom() { return this.#prenom; }
    set prenom(value) { this.#prenom = this.validateString(value, "prenom"); }

    get nom() { return this.#nom; }
    set nom(value) { this.#nom = this.validateString(value, "nom"); }

    get email() { return this.#email; }
    set email(value) { this.#email = this.validateString(value, "email"); }

    get password() { return this.#password; }
    set password(value) { this.#password = this.validateString(value, "password"); } // hash à gérer côté backend

    get is_admin() { return this.#is_admin; }
    set is_admin(value) { this.#is_admin = !!value; }

    get recherches_artistes() { return this.fetchList(this.#recherches_artistes, Artiste); }

    get regarder_interviews() { return this.fetchList(this.#regarder_interviews, Interview); }

    get regarder_extraits() { return this.fetchList(this.#regarder_extraits, Extrait); }

    get recherches_questions() { return this.fetchList(this.#recherches_questions, Question); }

    fromJSON(json) {
        super.fromJSON(json);
        this.#pseudo = json.pseudo;
        this.#prenom = json.prenom;
        this.#nom = json.nom;
        this.#email = json.email;
        this.#password = json.password;
        this.#is_admin = json.is_admin;
        this.#recherches_artistes = json.recherches_artistes;
        this.#regarder_interviews = json.regarder_interviews;
        this.#regarder_extraits = json.regarder_extraits;
        this.#recherches_questions = json.recherches_questions;
        return this;
    }

    toJSON() {
        return {
            uuid: this.uuid,
            pseudo: this.#pseudo,
            prenom: this.#prenom,
            nom: this.#nom,
            email: this.#email,
            password: this.#password,
            is_admin: this.#is_admin
        };
    }

    static connectAPI(pseudo_email, password) {
        /** 
         * Connecte un utilisateur avec son pseudo ou son e-mail et son password
         * (non implémenté)
        */
        let data = {}; // Résultat de la connexion à l'API
        // Au lieu de simplement le return, pourquoi pas avoir un attribut static current_user ?
        return new this(data);
    }
}