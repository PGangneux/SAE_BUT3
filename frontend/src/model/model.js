import clientAPI from "./clientAPI.js";

/** 
 * Classe par parent du Model
 */
export default class Model {
    #uuid;

    constructor(uuid){
        this.#uuid = uuid;
    }

    /** 
     * getter et setter de la classe
     */

    get uuid() { return this.#uuid; }

    /**
     * 
     * Utiliser pour surcharger les données de l'instance
     * À surcharger dans les classes enfants avec les bonnes données
     * @param {Object} json
     * @returns {Promise<Model>}
     */
    fromJSON(json) {
        if (json && json.uuid !== undefined && json.uuid !== null) {
            this.#uuid = json.uuid;
        }
        return this;
    }

    /**
     * Utiliser pour récupérer les données de l'instance
     * À surcharger dans les classes enfants avec les bonnes données
     * @returns {Object}
     */
    toJSON() {
        throw new Error('toJSON must be implemented by child class');
    }

    /** 
     * Utiliser pour récupérer le nom de l'endpoint correspondant à la classe
     * À surcharger dans les classes enfants avec les bonnes données
     * @returns {string}
     */
    get endpoint() {
        throw new Error('endpoint must be implemented by child class');
    }

    // Peut-être avoir un validateDate ?

    /**
     * Vérifie que le type de la variable est le bon
     * @param {*} value
     * @param {string} fieldName
     * @param {string} type
     * @returns {*}
     */
    static validateType(value, fieldName, type) {
        if (value === null || value === undefined) {
            throw new Error(`${fieldName} cannot be null or undefined`);
        }
        if (typeof value !== type) {
            throw new Error(`${fieldName} must be a ${type}, got ${typeof value}`);
        }
        return value;
    }

    /**
     * Valide si la valeur est un String
     * @param {*} value 
     * @param {string} fieldName 
     * @returns {string}
     */
    static validateString(value, fieldName) {
        return this.validateType(value, fieldName, "string");
    }

    /**
     * Valide si la valeur est un Int
     * @param {*} value 
     * @param {string} fieldName 
     * @returns {int}
     */
    static validateInt(value, fieldName) {
        return this.validateType(value, fieldName, "int");
    }

    /**
     * Récupère l'instance de Class 
     * @param {*} elem 
     * @param {Class} Class 
     * @returns {Promise<Model>}
     */
    async fetchDetail(elem, Class) {
        if (elem) return new Class(await clientAPI.get(elem.url));
        else return null;
    }

    /**
     * Récupère la liste d'instances de Class 
     * @param {*} elem 
     * @param {Class} Class 
     * @returns {Promise<Model>}
     */
    async fetchList(elem, Class) {
        return await clientAPI.get(elem.url)
        .then(data => { return data.map(row => { return new Class(row); }); });
    }

    /**
     * Récupère la liste des éléments de this
     * @param {Record<string, string|string[]>} args
     * @returns {Promise<Model>}
     */
    static async list(args=null) {
        return await clientAPI.get(await clientAPI.endpoints(this.endpoint), args)
        .then(data => { return data.map(row => { return new this(row); }); });
    }

    /**
     * Récupère l'élément de this appartir de son uuid
     * @param {string} uuid 
     * @returns {Promise<Model>}
     */
    static async detail(uuid) {
        return await clientAPI.get(clientAPI.url_uuid(await clientAPI.endpoints(this.endpoint), uuid))
        .then(data => { return new this(data); });
    }

    /**
     * Créé une instance de classe this
     * @returns {Promise<Model>}
     */
    async create() {
        if (this.#uuid) {
            throw new Error(`Cannot create ${this.constructor.name} that already has a UUID`);
        }
        return await clientAPI.post(
            clientAPI.endpoints(this.endpoint),
            JSON.stringify(this.toJSON())
        )
        // Charger les nouvelles données dans l'instance
        .then(json => { return this.fromJSON(json); });
    }

    /**
     * Modifie une instance de classe this
     * @returns {Promise<Model>}
     */
    async update() {
        if (!this.#uuid) {
            throw new Error(`Cannot update ${this.constructor.name} without a UUID`);
        }
        return await clientAPI.put(
            clientAPI.url_uuid(clientAPI.endpoints(this.endpoint), this.#uuid),
            JSON.stringify(this.toJSON())
        )
        // Charger les nouvelles données dans l'instance
        .then(json => { return this.fromJSON(json); });
    }

    /**
     * Supprime une instance de classe this
     * @returns {boolean}
     */
    async delete() {
        if (!this.#uuid) {
            throw new Error(`Cannot delete ${this.constructor.name} without a UUID`);
        }
        return await clientAPI.delete(
            clientAPI.url_uuid(clientAPI.endpoints(this.endpoint), this.#uuid),
        )
        // Charger les nouvelles données dans l'instance
        .then(result => { return true; });
    }
}