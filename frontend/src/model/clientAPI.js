/**
 * Classe client faisant le lien avec l'API
 */
export default class clientAPI {
    static BASE_URL = 'http://localhost:8000/';
    static #endpoints = null;

    /**
     * Récupère le dictionnaire des endpoints de l'API
     * Si nom de endpoint renseigner, renvoie url du endpoint
     * @param {string} endpoint 
     * @returns {Record<string, string>|string}
     */
    static async endpoints(endpoint) {
        if (!this.#endpoints) {
            this.#endpoints = await this.get(`${this.BASE_URL}API/`);
        }
        return endpoint ? this.#endpoints[endpoint] : this.#endpoints;
    }

    /**
     * Construction de l'url detail
     * @param {string} url 
     * @param {string} uuid 
     * @returns {string}
     */
    static url_uuid(url, uuid) {
        return uuid ? `${url}${uuid}/` : url;
    }

    /**
     * Construction de l'url avec paramètres
     * @param {string} url 
     * @param {Record<string, string|string[]>} args
     * @returns {string}
     */
    static url_query(url, args) {
        return args ? url + `?${new URLSearchParams(args)}` : url;
    }

    /**
     * Récupère le header, ajoute le token si connecter (non implémenter)
     * @param {boolean} admin
     * @returns {Record<string, string>}
     */
    static get_headers(admin=false) {
        let headers = {};
        headers['Content-Type'] = 'application/json';
        if (admin) {
            this.get_token()
        }
        return headers;
    }

    /**
     * Récupère le token d'authentification de l'utilisateur connecté (non implémenter)
     * @returns {string}
     */
    static get_token() {
        return null;
    }

    /**
     * 
     * @param {string} methode (GET, POST, PATCH, DELETE)
     * @param {string} url 
     * @param {Record<string, string|string[]>} args 
     * @param {Object} data 
     * @param {boolean} admin Si besoin d'être administrateur (non implémenter)
     * @returns {Promise}
     */
    static async fetch(methode, url, args=null, data=null, admin=false) {
        if (args) url = this.url_query(url, args);

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

    /**
     * Fetch GET
     * @param {string} url
     * @param {Record<string, string|string[]>} args
     * @param {boolean} admin
     * @returns {Promise}
     */
    static async get(url, args=null, admin=false) {
        return await this.fetch("GET", url, args, null, admin);
    }

    /**
     * Fetch POST
     * @param {string} url
     * @param {Object} data
     * @param {boolean} admin
     * @returns {Promise}
     */
    static async post(url, data, admin=true) {
        return await this.fetch("POST", url, null, data, admin);
    }

    /**
     * Fetch PATCH
     * @param {string} url
     * @param {Object} data
     * @param {boolean} admin
     * @returns {Promise}
     */
    static async put(url, data, admin=true) {
        return await this.fetch("PATCH", url, null, data, admin);
    }

    /**
     * Fetch DELETE
     * @param {string} url
     * @param {boolean} admin
     * @returns {Promise}
     */
    static async delete(url, admin=true) {
        return await this.fetch("DELETE", url, null, null, admin);
    }
}
