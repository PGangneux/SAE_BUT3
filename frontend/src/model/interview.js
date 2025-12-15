import Model from "./model.js";
import Extrait from "./extrait.js";
import Tag from "./tag.js";

export default class Interview extends Model {
    #titre;
    #date;
    #occasion;
    #description;
    #lieu;
    #extraits;
    #tags;
    #duree;
    #dureePromise;

    constructor({ uuid, titre, date, occasion, description, lieu, extraits, tags }) {
        super(uuid);
        this.#titre = titre;
        this.#date = date;
        this.#occasion = occasion;
        this.#description = description;
        this.#lieu = lieu;
        this.#extraits = extraits;
        this.#tags = tags;
        this.#duree = 0;
    }

    static get endpoint() { return "interviews"; }

    get titre() { return this.#titre; }
    set titre(value) { this.#titre = Model.validateString(value, "titre"); }

    get date() { return this.#date; }
    set date(value) { this.#date = value; }

    get occasion() { return this.#occasion; }
    set occasion(value) { this.#occasion = Model.validateString(value, "occasion"); }

    get description() { return this.#description; }
    set description(value) { this.#description = Model.validateString(value, "description"); }

    get lieu() { return this.#lieu; }
    set lieu(value) { this.#lieu = Model.validateString(value, "lieu"); }

    async extraits(args) { return await this.fetchList(this.#extraits, Extrait, args); }

    /**
     * Redéfinie la liste des extraits de this
     * @param {Array<Extrait>} extraits Les nouveaux extrait de this.
     */
    async setExtraits(extraits) {
        // Extraits actuellement liés
        const current = await this.extraits();

        const currentUUIDs = new Set(current.map(extrait => extrait.uuid));
        const newUUIDs = new Set(extraits.map(extrait => extrait.uuid));

        // Supprimer ceux qui ne sont plus là
        for (const extrait of current) {
            if (!newUUIDs.has(extrait.uuid)) {
                await extrait.disconnect_interview(this);
            }
        }

        // Ajouter les nouveaux
        // Connexion avec POSITION
        for (let index = 0; index < extraits.length; index++) {
            const extrait = extraits[index];

            if (!currentUUIDs.has(extrait.uuid)) {
                // add new Extrait
                await extrait.connect_interview(this, index)
            }
            else{
                // update posiiton
                await extrait.update_position(this, index)
            }
        }

        // Reset durée
        this.#dureePromise = null;
    }



    async tags(args) { return await this.fetchList(this.#tags, Tag, args); }

    get duree() {
        if (!this.#dureePromise) {
            this.#dureePromise = (async () => {
                const extraits = await this.extraits();
                let total = 0;
                for (const extrait of extraits) {
                    total += extrait.duree;
                }
                this.#duree = total;
                return total;
            })();
        }
        return this.#dureePromise;
    }


    /**
     * Connecte une interview à un tag
     * @param {Tag} tag 
     */
    async connect_tag(tag) {
        await this.connect(this.#tags, {'uuid': tag.uuid});
    }

    /**
     * Déconnecte une interview d'un tag
     * @param {Tag} tag 
     */
    async disconnect_tag(tag) {
        await this.disconnect(this.#tags, tag);
    }

    fromJSON(json) {
        super.fromJSON(json);
        this.#titre = json.titre;
        this.#date = json.date;
        this.#occasion = json.occasion;
        this.#description = json.description;
        this.#lieu = json.lieu;
        this.#extraits = json.extraits;
        this.#tags = json.tags;
        return this;
    }

    toJSON() {
        return {
            uuid: this.uuid,
            titre: this.#titre,
            date: this.#date,
            occasion: this.#occasion,
            description: this.#description,
            lieu: this.#lieu,
        };
    }
}
