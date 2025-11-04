import Utilisateur from "./utilisateur";

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
     * @returns {Promise<Record<string, string>|string>}
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
     * @param {boolean} withAuth
     * @returns {Promise<Record<string, string>>}
     */
    static get_headers(withAuth=false) {
        let headers = {};
        headers['Content-Type'] = 'application/json';
        if (withAuth) {
            const token = this.get_token();
            if (token) headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    }

    /**
     * Récupère le token d'authentification de l'utilisateur connecté (access)
     * @returns {string|null}
     */
    static get_token() {
        return localStorage.getItem('access');
    }

    /**
     * Récupère le refresh token
     * @returns {string|null}
     */
    static get_refresh_token() {
        return localStorage.getItem('refresh');
    }

    /**
     * Stocke access/refresh dans localStorage
     * @param {string|null} access 
     * @param {string|null} refresh 
     */
    static save_tokens(access, refresh=null) {
        if (access) localStorage.setItem('access', access);
        if (refresh) localStorage.setItem('refresh', refresh);
    }

    /**
     * Supprime tokens
     */
    static clear_tokens() {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
    }

    /**
     * Tente de refresh l'access token à partir du refresh token.
     * Retourne true si succès, false sinon.
     * IMPORTANT: endpoint utilisé: /API/token/refresh/
     * @returns {Promise<boolean>}
     */
    static async tryRefresh() {
        const refresh = this.get_refresh_token();
        if (!refresh) return false;
        try {
            const res = await fetch(`${this.BASE_URL}API/login/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify({ refresh: refresh })
            });
            if (!res.ok) {
                this.clear_tokens();
                return false;
            }
            const data = await res.json();
            // SimpleJWT renvoie { access: "..." }
            if (data.access) {
                this.save_tokens(data.access, refresh); // conserve le refresh existant
                return true;
            } else {
                this.clear_tokens();
                return false;
            }
        } catch (e) {
            console.error("Erreur lors du refresh token :", e);
            this.clear_tokens();
            return false;
        }
    }

    /**
     * 
     * @param {string} methode (GET, POST, PATCH, DELETE)
     * @param {string} url 
     * @param {Record<string, string|string[]>} args 
     * @param {Object} data 
     * @param {boolean} withAuth 
     * @returns {Promise<Object>}
     */
    static async fetch(methode, url, args=null, data=null, withAuth=false) {
        if (args) url = this.url_query(url, args);

        const opts = {
            method: methode.toUpperCase(),
            headers: await this.get_headers(withAuth),
        };
        if (data) opts["body"] = data;

        let response = await fetch(url, opts);

        if (response.status === 401 && withAuth) {
            const refreshed = await this.tryRefresh();
            if (refreshed) {
                opts.headers = this.get_headers(true);
                response = await fetch(url, opts);
            } else {
                this.clear_tokens();
                throw new Error('401 : Unauthorized (token expired or invalid)');
            }
        }

        if (!response.ok) {
            // essaie de donner des messages utiles
            let texte;
            try {
                texte = await response.text();
                // si c'est du JSON, parse pour message plus propre
                try {
                    const j = JSON.parse(texte);
                    texte = JSON.stringify(j);
                } catch {}
            } catch {
                texte = response.statusText;
            }
            throw new Error(`${response.status} : ${texte}`);
        }

        // Si pas de contenu (204), retourne null
        if (response.status === 204) return null;

        // parse JSON response
        return await response.json();
    }

    /**
     * Fetch GET
     * @param {string} url
     * @param {Record<string, string|string[]>} args
     * @param {boolean} withAuth
     * @returns {Promise<Object>}
     */
    static async get(url, args=null, withAuth=false) {
        return await this.fetch("GET", url, args, null, withAuth);
    }

    /**
     * Fetch POST
     * @param {string} url
     * @param {Object} data
     * @param {boolean} withAuth
     * @returns {Promise<Object>}
     */
    static async post(url, data, withAuth=true) {
        return await this.fetch("POST", url, null, data, withAuth);
    }

    /**
     * Fetch PATCH
     * @param {string} url
     * @param {Object} data
     * @param {boolean} withAuth
     * @returns {Promise<Object>}
     */
    static async put(url, data, withAuth=true) {
        return await this.fetch("PATCH", url, null, data, withAuth);
    }

    /**
     * Fetch DELETE
     * @param {string} url
     * @param {boolean} withAuth
     * @returns {Promise<Object>}
     */
    static async delete(url, withAuth=true) {
        return await this.fetch("DELETE", url, null, null, withAuth);
    }

    /**
     * Connecte un utilisateur à l'API
     * @param {string} pseudo_email 
     * @param {string} password 
     * @returns {Promise<Utilisateur>}
     */
    static async connectAPI(pseudo_email, password) {
        try {
            const res = await this.post(
                `${this.BASE_URL}API/login/`,
                JSON.stringify(
                    {'identifiant': pseudo_email, 'password': password}
                )
            );
            this.save_tokens(res.access, res.refresh)
            return new Utilisateur(await this.get(res.utilisateur));
        } catch (error) {
            console.error(`Erreur HTTP ${error.message}`);
            return null;
        }
    }

    static disconnectAPI() {
        const refresh = this.get_refresh_token();
        if (refresh) { this.clear_tokens(); }
        return null;
    }
}
