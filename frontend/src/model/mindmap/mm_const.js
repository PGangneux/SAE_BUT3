import Artiste from "../artiste.js";
import Extrait from "../extrait.js";
import Interview from "../interview.js";
import Nation from "../nation.js";
import Question from "../question.js";
import StyleMusical from "../style_musical.js";
import Tag from "../tag.js";
import Theme from "../theme.js";

export class mm_Root {
}

export const mm_LegendClassMap = {
    "Artiste": "Artiste",
    "Extrait": "Extrait",
    "Interview": "Interview",
    "Nation": "Pays",
    "Question": "Question",
    "StyleMusical": "Style Musical",
    "Tag": "Tag",
    "Theme": "Thème",
}

export const mm_CategorysDefault = [
    Artiste,
    Nation,
    StyleMusical,
    Theme,
]

export const mm_CategorysSearch = [
    Question,
    Extrait,
    Interview
]

export const mm_CheminMap = {
    Artiste: [],
    Extrait: [],
    Interview: [],
    Nation: [],
    Question: [],
    StyleMusical: [],
    Tag: [],
    Theme: [],
}