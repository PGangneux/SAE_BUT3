import Model from "./model.js";
import Artiste from "./artiste.js";
import Question from "./question.js";
import Interview from "./interview.js";
import Tag from "./tag.js";
import ClientAPI from "./clientAPI.js";

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
  #duree;

  constructor({
    uuid,
    titre,
    description,
    youtube_url,
    vimeo_url,
    uploaded_at,
    artiste,
    question,
    interviews,
    tags,
    position,
    duree,
  }) {
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
    this.#duree = duree;
  }

  static get endpoint() {
    return "extraits";
  }

  get titre() {
    return this.#titre;
  }
  set titre(value) {
    this.#titre = this.constructor.validateString(value, "titre");
  }

  get description() {
    return this.#description;
  }
  set description(value) {
    this.#description = this.constructor.validateString(value, "description");
  }

  get youtube_url() {
    return this.#youtube_url;
  }
  set youtube_url(value) {
    this.#youtube_url = this.constructor.validateString(value, "youtube_url");
  }

  get vimeo_url() {
    return this.#vimeo_url;
  }
  set vimeo_url(value) {
    this.#vimeo_url = this.constructor.validateString(value, "vimeo_url");
  }

  get uploaded_at() {
    return this.#uploaded_at;
  }
  set uploaded_at(value) {
    this.#uploaded_at = value;
  }

  get artiste() {
    return  this.fetchDetail(this.#artiste, Artiste);
  }
  set artiste(value) {
    this.#artiste_uuid = this.constructor.validateString(value, "artiste_uuid");
  }

  get question() {
    return  this.fetchDetail(this.#question, Question);
  }
  set question(value) {
    this.#question_uuid = this.constructor.validateString(
      value,
      "question_uuid"
    );
  }

  get duree() {
    return this.#duree;
  }
  set duree(value) {
    this.#duree = value;
  }

  async interviews(args) {
    return await this.fetchList(this.#interviews, Interview, args);
  }

  async tags(args) {
    return await this.fetchList(this.#tags, Tag, args);
  }

  get position() {
    return this.#position;
  }

  get url_miniature_yt() {
    return `https://img.youtube.com/vi/${this.youtube_url}/maxresdefault.jpg`;
  }

  async get_url_miniature_vimeo() {
    const response = await fetch(
      `https://vimeo.com/api/oembed.json?url=https://vimeo.com/${
        this.#vimeo_url
      }`
    );
    const data = await response.json();
    return data.thumbnail_url;
  }

  /**
   * Connecte un extrait à un tag
   * @param {Tag} tag
   */
  async connect_tag(tag) {
    await this.connect(this.#tags, { uuid: tag.uuid });
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
   * @param {number} position
   */
  async connect_interview(interview, position) {
    // await this.connect(this.#interviews, {'uuid': interview.uuid, 'position': position});
    await this.connect(this.#interviews, {
      uuid: interview.uuid,
      position: Model.validateNumber(position, "position"),
    });
  }

  /**
   * Modifie la position d'un extrait dans une interview
   * @param {Interview} interview
   * @param {number} position
   */
  async update_position(interview, position) {
    try {
      return await ClientAPI.put(
        ClientAPI.url_uuid(this.#interviews, interview.uuid),
        JSON.stringify({ position: position })
      );
    } catch (error) {
      console.error(`Erreur HTTP ${error.message}`);
      return null;
    }
  }

  /**
   * Déconnecte un extrait d'une interview
   * @param {Interview} interview
   */
  async disconnect_interview(interview) {
    await this.disconnect(this.#interviews, interview);
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
    this.#duree = json.duree;
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
      question_uuid: this.#question_uuid,
      duree: this.#duree,
    };
  }
}
