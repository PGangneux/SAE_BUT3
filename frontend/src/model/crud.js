import { BASE_URL } from "./prefetcher";

export default class CRUD {
    #uuid

    constructor(uuid){
        this.#uuid = uuid;
    }

    get uuid() { return this.#uuid }

    toJSON() {
        throw new Error('toJSON must be implemented by child class');
    }

    get endpoint() {
        throw new Error('endpoint must be implemented by child class');
    }

    create() {
        if (this.#uuid) {
            throw new Error(`Cannot create ${this.constructor.name} that already has a UUID`);
        }

        return fetch(`${BASE_URL}API/${this.endpoint}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.toJSON())
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(result => {
            this.#uuid = result.uuid;
            return this;
        });
    }

    update() {
        if (!this.#uuid) {
            throw new Error(`Cannot update ${this.constructor.name} without a UUID`);
        }

        return fetch(`${BASE_URL}API/${this.endpoint}/${this.#uuid}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.toJSON())
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(result => this);
    }

    delete() {
        if (!this.#uuid) {
            throw new Error(`Cannot delete ${this.constructor.name} without a UUID`);
        }

        return fetch(`${BASE_URL}API/${this.endpoint}/${this.#uuid}/`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            this.#uuid = null;
            return true;
        });
    }
}