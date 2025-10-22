const BASE_URL = 'http://localhost:8000/';

export default class Prefetcher {
    constructor() {
        this.cache = new Map();
    }

    // Clear cache (call this when user connects)
    clearCache() {
        this.cache.clear();
    }

    // Generic fetch method with cache
    _fetch(url) {
        if (this.cache.has(url)) {
            return Promise.resolve(this.cache.get(url));
        }

        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                this.cache.set(url, data);
                return data;
            });
    }

    // Individual fetch methods
    fetch_theme(id) {
        return this._fetch(`${BASE_URL}API/themes/${id}/`);
    }

    fetch_themes() {
        return this._fetch(`${BASE_URL}API/themes/`);
    }

    fetch_question(id) {
        return this._fetch(`${BASE_URL}API/questions/${id}/`);
    }

    fetch_questions() {
        return this._fetch(`${BASE_URL}API/questions/`);
    }

    fetch_extrait(id) {
        return this._fetch(`${BASE_URL}API/extraits/${id}/`);
    }

    fetch_extraits() {
        return this._fetch(`${BASE_URL}API/extraits/`);
    }

    fetch_interview(id) {
        return this._fetch(`${BASE_URL}API/interviews/${id}/`);
    }

    fetch_interviews() {
        return this._fetch(`${BASE_URL}API/interviews/`);
    }

    fetch_artiste(id) {
        return this._fetch(`${BASE_URL}API/artistes/${id}/`);
    }

    fetch_artistes() {
        return this._fetch(`${BASE_URL}API/artistes/`);
    }

    fetch_utilisateur(id) {
        return this._fetch(`${BASE_URL}API/utilisateurs/${id}/`);
    }

    fetch_utilisateurs() {
        return this._fetch(`${BASE_URL}API/utilisateurs/`);
    }
}