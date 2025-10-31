import prefetcher from "./prefetcher";

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

    validateString(value, fieldName) {
        if (value === null || value === undefined) {
            throw new Error(`${fieldName} cannot be null or undefined`)
        }
        if (typeof value !== "string") {
            throw new Error(`${fieldName} must be a string, got ${typeof value}`)
        }
        return value
    }

    validateInt(value, fieldName) {
        if (value === null || value === undefined) {
            throw new Error(`${fieldName} cannot be null or undefined`)
        }
        if (typeof value !== "int") {
            throw new Error(`${fieldName} must be an int, got ${typeof value}`)
        }
        return value
    }

    async fetchDetail(elem, Class) {
        if (elem) return new Class(await prefetcher.get(elem.url));
        else return null;
    }

    async fetchList(elem, Class) {
        return await prefetcher.get(elem.url).then(data => { return data.map(row => { return new Class(row) }) });
    }

    static async list() {
        return await prefetcher.get(await prefetcher.endpoints().then(res => { return res[this.endpoint] }))
        .then(data => { return data.map(row => { return new this(row) }) })
    }

    static async detail(uuid) {
        return await prefetcher.get(prefetcher.url_uuid(await prefetcher.endpoints().then(res => { return res[this.endpoint] }), uuid))
        .then(data => { return new this(data); })
    }

    async create() {
        if (this.#uuid) {
            throw new Error(`Cannot create ${this.constructor.name} that already has a UUID`);
        }
        return await prefetcher.post(
            prefetcher.endpoints().then(res => { return res[this.endpoint] }),
            JSON.stringify(this.toJSON())
        )
        .then(result => {
            // Charger les nouvelles données dans l'instance
            this.constructor(result);
        });
    }

    async update() {
        if (!this.#uuid) {
            throw new Error(`Cannot update ${this.constructor.name} without a UUID`);
        }
        return await prefetcher.put(
            prefetcher.url_uuid(prefetcher.endpoints().then(res => { return res[this.endpoint] }), this.#uuid),
            JSON.stringify(this.toJSON())
        )
        .then(result => {
            // Charger les nouvelles données dans l'instance
            this.constructor(result);
        });
    }

    async delete() {
        if (!this.#uuid) {
            throw new Error(`Cannot delete ${this.constructor.name} without a UUID`);
        }
        return await prefetcher.delete(
            prefetcher.url_uuid(prefetcher.endpoints().then(res => { return res[this.endpoint] }), this.#uuid),
        )
        .then(result => {
            // Charger les nouvelles données dans l'instance
            return true
        });
    }
}