export default class clientAPI {
    static BASE_URL = 'http://localhost:8000/';
    static #endpoints = null;

    static async endpoints() {
        /** 
         * Récupère les endpoints de l'API
        */
        if (!this.#endpoints) {
            this.#endpoints = await this.get(`${this.BASE_URL}API/`);
        }
        return this.#endpoints;
    }

    static url_uuid(url, uuid) {
        /** 
         * Construction de l'url detail
         * url: url list
         * uuid: uuid de l'élément visé
        */
        return uuid ? `${url}${uuid}/` : url;
    }

    static url_query(url, args) {
        /**
         * Construction de l'url complète
         * url: endpoint visé
         * args: paramètres d'url, {champ: [valeur1, valeur2]}
        */
        return args ? url + `?${new URLSearchParams(args)}` : url;
    }

    static get_headers(admin=false) {
        /**
         * Récupère le header, ajoute le token si connecter (non implémenter)
        */
        let headers = {};
        headers['Content-Type'] = 'application/json';
        if (admin) {

        }
        return headers;
    }

    static get_token() {
        /**
         * Récupère le token d'authentification (non implémenter)
        */
        return null;
    }

    static async fetch(methode, url, args=null, data=null, admin=false) {
        /** 
         * Fetch par défaut 
         * methode: Méthode de la requête (GET, POST, PATCH, DELETE)
         * url: endpoint visé
         * args: paramètres d'url, {champ: [valeur1, valeur2]}
         * data: données à envoyer, json
         * admin: Si besoin d'être connecter (non implémenter)
        */
        if (args) url = this.url_query(url, args)

        const opts = {
            method: methode.toUpperCase(),
            headers: this.get_headers(admin),
        };
        if (data) opts["body"] = data;

        return await fetch(url, opts)
        .then(response => {
            if (!response.ok) throw new Error(response.status);
            return response.json();
        });
    }

    static async get(url, args=null, admin=false) {
        /** 
         * Fetch GET
        */
        return await this.fetch("GET", url, args, null, admin);
    }

    static async post(url, data, admin=true) {
        /** 
         * Fetch POST
        */
        return await this.fetch("POST", url, null, data, admin);
    }

    static async put(url, data, admin=true) {
        /** 
         * Fetch PATCH
        */
        return await this.fetch("PATCH", url, null, data, admin);
    }

    static async delete(url, admin=true) {
        /** 
         * Fetch DELETE
        */
        return await this.fetch("DELETE", url, null, null, admin);
    }
}
