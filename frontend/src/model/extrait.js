import Model from "./model.js";
import Artiste from "./artiste.js";
import Question from "./question.js";
import Interview from "./interview.js";
import Tag from "./tag.js";

export default class Extrait extends Model {
    #titre;
    #description;
    #youtube_url;
    #vimeo_url;
    #uploaded_at;
    #artiste;
    #question;
    #interviews;
    #tags;
    #position;
    #artiste_uuid;
    #question_uuid;

    constructor({ uuid, titre, description, youtube_url, vimeo_url, uploaded_at, artiste, question, interviews, tags, position }) {
        super(uuid);
        this.#titre = titre;
        this.#description = description;
        this.#youtube_url = youtube_url;
        this.#vimeo_url = vimeo_url;
        this.#uploaded_at = uploaded_at;
        this.#artiste = artiste;
        this.#question = question;
        this.#interviews = interviews;
        this.#tags = tags;
        this.#position = position;
        this.#artiste_uuid = null;
        this.#question_uuid = null;
    }

    static get endpoint() { return "extraits"; }

    get titre() { return this.#titre; }
    set titre(value) { this.#titre = this.validateString(value, "titre"); }

    get description() { return this.#description; }
    set description(value) { this.#description = this.validateString(value, "description"); }

    get youtube_url() { return this.#youtube_url; }
    set youtube_url(value) { this.#youtube_url = this.validateString(value, "youtube_url"); }

    get vimeo_url() { return this.#vimeo_url; }
    set vimeo_url(value) { this.#vimeo_url = this.validateString(value, "vimeo_url"); }

    get uploaded_at() { return this.#uploaded_at; }
    set uploaded_at(value) { this.#uploaded_at = value; }

    get artiste() { return this.fetchDetail(this.#artiste, Artiste); }
    set artiste(value) { this.#artiste_uuid = this.validateString(value, "artiste_uuid"); }

    get question() { return this.fetchDetail(this.#question, Question); }
    set question(value) { this.#question_uuid = this.validateString(value, "question_uuid"); }

    get interviews() { return this.fetchList(this.#interviews, Interview); }

    get tags() { return this.fetchList(this.#tags, Tag); }

    get position() { return this.#position; }

    get url_miniature_yt(){
        return `https://img.youtube.com/vi/${this.youtube_url}/maxresdefault.jpg`;
    }

    /**
     * Connecte un extrait à un tag
     * @param {Tag} tag 
     */
    async connect_tag(tag) {
        await this.connect(this.#tags, {'uuid': tag.uuid});
    }

    /**
     * Déconnecte un extrait d'un tag
     * @param {Tag} tag 
     */
    async disconnect_tag(tag) {
        await this.disconnect(this.#tags, tag);
    }

    /**
     * Connecte un extrait à une interview
     * @param {Interview} interview 
     * @param {int} position 
     */
    async connect_interview(interview, position) {
        await this.connect(this.#interviews, {'uuid': interview.uuid, 'position': this.validateInt(position)});
    }

    /**
     * Déconnecte un extrait d'une interview
     * @param {Interview} interview 
     */
    async disconnect_interview(interview) {
        await this.disconnect(this.#interviews, interview)
    }

    fromJSON(json) {
        super.fromJSON(json);
        this.#titre = json.titre;
        this.#description = json.description;
        this.#youtube_url = json.youtube_url;
        this.#vimeo_url = json.vimeo_url;
        this.#uploaded_at = json.uploaded_at;
        this.#artiste = json.artiste;
        this.#question = json.question;
        this.#interviews = json.interviews;
        this.#tags = json.tags;
        this.#position = json.position;
        return this;
    }

    toJSON() {
        return {
            uuid: this.uuid,
            titre: this.#titre,
            description: this.#description,
            youtube_url: this.#youtube_url,
            vimeo_url: this.#vimeo_url,
            uploaded_at: this.#uploaded_at,
            artiste_uuid: this.#artiste_uuid,
            question_uuid: this.#question_uuid
        };
    }
}
