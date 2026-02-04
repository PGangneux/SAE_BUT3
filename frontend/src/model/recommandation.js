import { markRaw } from 'vue';
import Extrait from '@model/extrait.js';
import Interview from '@model/interview.js';
import ClientAPI from '@model/clientAPI.js';

/**
 * Génère un dictionnaire de poids selon le chemin d'entrée de l'utilisateur.
 * les poids sont plus lourd au debut du chemin.
 *
 * @param {Array} chemin - liste représentant le chemin d'entrée de l'utilisateur
 * @return {Dict} Dictionnaire des poids pour les recommandations
*/
function get_reco_weights(chemin) {
    const weights = {};
    chemin.forEach((value, index, array) => {
        weights[value.constructor.mmch_dbjsclass.name] = array.length - index;
    });
    return weights;
}


/* Récupère les vidéos recommandées en fonction de l'extrait ou de l'interview actuelle.
   Utilise un algorithme de recommandation basé sur des poids prédéfinis.
*/
export default async function fetchRecommendations({ video = null, chemin = null, filters = null, page = 0, size = 10 }) {

    // TODO Nécessite d'enregistrer et modifier les poids à chaque fois
    let weights;
    if (false) {
        weights = localStorage.getItem('weights')
            .then((weights) => weights ? JSON.parse(weights) : get_reco_weights(chemin));
        localStorage.setItem('weights', JSON.stringify(weights));
    }
    else {
        weights = get_reco_weights(chemin);
    }

    // Récupération des poids
    const payload = {
        'weights': weights
    };

    // Construction des filtres (optionnelle)
    if (filters) {
        payload['filters'] = filters;
    };

    const result = await ClientAPI.post(
        `${ClientAPI.BASE_URL}api/recommandations`,
        JSON.stringify(payload),
        !!ClientAPI.current_user,
        video ? { video, size: size, page: page } : null
    );

    return markRaw(
        result.map(v =>
            v.type === 'Extrait'
                ? markRaw(new Extrait(v.value))
                : markRaw(new Interview(v.value))
        )
    );
}
