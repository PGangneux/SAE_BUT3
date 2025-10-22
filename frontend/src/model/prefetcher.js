const BASE_URL = 'http://localhost:8000/';

import artiste_t from "./artiste.js";
import extrait_t from "./extrait.js";
import interview_t from "./interview.js";
import question_t from "./question.js";
import theme_t from "./theme.js";

class prefetcher {
    // Class-level cache (shared across all instances)
    static #cache = new Map();

    // Clear cache (call this when user connects)
    static clearCache() {
        prefetcher.#cache.clear();
    }

    // Generic fetch method with cache and object building
    static fetch(Class, url, returnsList = false) {
        if (prefetcher.#cache.has(url)) {
            return prefetcher.#cache.get(url);
        }

        const xhr = new XMLHttpRequest();
        xhr.open("GET", url, false);
        xhr.send();

        if (xhr.status !== 200) {
            throw new Error(`HTTP error! status: ${xhr.status}`);
        }

        const data = JSON.parse(xhr.responseText);

        // Build objects using the class constructor
        let result;
        /// console.log("prefetcher data return");
        /// console.log(data);
        if (returnsList) {
            result = data.map(item => new Class(item));
        } else {
            result = new Class(data);
        }

        prefetcher.#cache.set(url, result);
        return result;
    }

    static theme(id) {
        return prefetcher.fetch(theme_t, `${BASE_URL}API/themes/${id}/`, false);
    }

    static theme_all() {
        return prefetcher.fetch(theme_t, `${BASE_URL}API/themes/`, true);
    }

    static question(id) {
        return prefetcher.fetch(question_t, `${BASE_URL}API/questions/${id}/`, false);
    }

    static question_all() {
        return prefetcher.fetch(question_t, `${BASE_URL}API/questions/`, true);
    }

    static extrait(id) {
        return prefetcher.fetch(extrait_t, `${BASE_URL}API/extraits/${id}/`, false);
    }

    static extrait_all() {
        return prefetcher.fetch(extrait_t, `${BASE_URL}API/extraits/`, true);
    }

    static interview(id) {
        return prefetcher.fetch(interview_t, `${BASE_URL}API/interviews/${id}/`, false);
    }

    static interview_all() {
        return prefetcher.fetch(interview_t, `${BASE_URL}API/interviews/`, true);
    }

    static artiste(id) {
        return prefetcher.fetch(artiste_t, `${BASE_URL}API/artistes/${id}/`, false);
    }

    static artiste_all() {
        return prefetcher.fetch(artiste_t, `${BASE_URL}API/artistes/`, true);
    }
}

export { BASE_URL, prefetcher };
export default prefetcher;