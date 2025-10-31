import clientAPI from "./clientAPI.js";

export default class Model {
    #uuid

    constructor(uuid){
        this.#uuid = uuid;
    }

    get uuid() { return this.#uuid }

    fromJSON(json) {
        /** 
         * À surcharger dans les classes enfants avec les bonnes données
        */
        if (json && json.uuid !== undefined && json.uuid !== null) {
            this.#uuid = json.uuid;
        }
        return this;
    }

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
        if (elem) return new Class(await clientAPI.get(elem.url));
        else return null;
    }

    async fetchList(elem, Class) {
        return await clientAPI.get(elem.url).then(data => { return data.map(row => { return new Class(row) }) });
    }

    static async list(args=null) {
        return await clientAPI.get(await clientAPI.endpoints().then(res => { return res[this.endpoint] }), args)
        .then(data => { return data.map(row => { return new this(row) }) })
    }

    static async detail(uuid) {
        return await clientAPI.get(clientAPI.url_uuid(await clientAPI.endpoints().then(res => { return res[this.endpoint] }), uuid))
        .then(data => { return new this(data); })
    }

    async create() {
        if (this.#uuid) {
            throw new Error(`Cannot create ${this.constructor.name} that already has a UUID`);
        }
        return await clientAPI.post(
            clientAPI.endpoints().then(res => { return res[this.endpoint] }),
            JSON.stringify(this.toJSON())
        )
        .then(json => {
            // Charger les nouvelles données dans l'instance
            return this.fromJSON(json);
        });
    }

    async update() {
        if (!this.#uuid) {
            throw new Error(`Cannot update ${this.constructor.name} without a UUID`);
        }
        return await clientAPI.put(
            clientAPI.url_uuid(clientAPI.endpoints().then(res => { return res[this.endpoint] }), this.#uuid),
            JSON.stringify(this.toJSON())
        )
        .then(json => {
            // Charger les nouvelles données dans l'instance
            return this.fromJSON(json);
        });
    }

    async delete() {
        if (!this.#uuid) {
            throw new Error(`Cannot delete ${this.constructor.name} without a UUID`);
        }
        return await clientAPI.delete(
            clientAPI.url_uuid(clientAPI.endpoints().then(res => { return res[this.endpoint] }), this.#uuid),
        )
        .then(result => {
            // Charger les nouvelles données dans l'instance
            return true
        });
    }
}