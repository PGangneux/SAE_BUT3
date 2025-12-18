import Papa from 'papaparse';
import Interview from './interview.js';
import Extrait from './extrait.js';
import Artiste from './artiste.js';
import Question from './question.js';
import Tag from './tag.js';
import Theme from './theme.js';

export function get_YT_videoId(url) {
  try {
    const u = new URL(url);
    if (u.hostname === "youtu.be") return u.pathname.slice(1);
    if (u.hostname.includes("youtube.com")) {
      if (u.pathname.startsWith("/embed/")) return u.pathname.split("/")[2];
      if (u.searchParams.has("v")) return u.searchParams.get("v");
    }
  } catch {
    console.warn("URL YouTube invalide :", url);
  }
  return null;
}

/**
 * Parse un fichier CSV contenant des extraits d'interviews d'artistes
 * et crée les instances des Models correspondants
 * @param {File|string} file - Le fichier CSV ou son contenu
 * @returns {Promise<Object>} Objet contenant les données parsées
 */
export async function parse(file) {
  try {
    // Si c'est un objet File, lire son contenu
    let csvContent;
    if (file instanceof File) {
      csvContent = await file.text();
    } else {
      csvContent = file;
    }

    // Parser le CSV avec Papaparse
    const result = Papa.parse(csvContent, {
      header: true,
      skipEmptyLines: true,
      dynamicTyping: false,
      transformHeader: (header) => header.trim(),
      delimitersToGuess: [',', ';', '\t']
    });

    if (result.errors.length > 0) {
      console.warn('Avertissements de parsing:', result.errors);
    }

    // Créer les données brutes des extraits
    const extraitsData = result.data
      .filter(row => row.ARTISTE?.trim())
      .map((row, index) => ({
        id: `extrait_${index + 1}`,
        artiste: row.ARTISTE?.trim() || '',
        theme: row.Theme?.trim() || '',
        question: row.Question?.trim() || '',
        audio: row.Audio?.trim() || '',
        tags: row.Tags ? row.Tags.split(';').map(t => t.trim()).filter(Boolean) : [],
        date: row.Date?.trim() || '',
        ville: row.Ville?.trim() || '',
        youtube: get_YT_videoId(row.Youtube?.trim()) || null,
        vimeo:  null,
        evenement: row.Evénement?.trim() || row['Événement']?.trim() || '',
        duree: parseInt(row.Duree) || 0
      }));

    // Grouper les extraits par interview (artiste + événement)
    const interviewsMap = new Map();
    
    extraitsData.forEach(extrait => {
      const key = `${extrait.artiste}|${extrait.evenement}`;
      
      if (!interviewsMap.has(key)) {
        interviewsMap.set(key, {
          id: `interview_${interviewsMap.size + 1}`,
          artiste: extrait.artiste,
          evenement: extrait.evenement,
          ville: extrait.ville,
          date: extrait.date,
          extraits: []
        });
      }
      
      interviewsMap.get(key).extraits.push(extrait);
    });

    const interviewsData = Array.from(interviewsMap.values());

    // Statistiques
    const artistesUniques = new Set(extraitsData.map(e => e.artiste));
    const evenementsUniques = new Set(extraitsData.map(e => e.evenement).filter(Boolean));
    const villesUniques = new Set(extraitsData.map(e => e.ville).filter(Boolean));
    const tagsUniques = new Set(extraitsData.flatMap(e => e.tags));

    return {
      success: true,
      extraits: extraitsData,
      interviews: interviewsData,
      stats: {
        totalExtraits: extraitsData.length,
        totalInterviews: interviewsData.length,
        artistes: artistesUniques.size,
        evenements: evenementsUniques.size,
        villes: villesUniques.size,
        tags: tagsUniques.size,
        avecYoutube: extraitsData.filter(e => e.youtube).length,
        avecVimeo: extraitsData.filter(e => e.vimeo).length
      }
    };

  } catch (error) {
    console.error('Erreur lors du parsing du fichier:', error);
    return {
      success: false,
      error: error.message,
      extraits: [],
      interviews: []
    };
  }
}

/**
 * Crée les instances Interview et Extrait à partir des données parsées
 * Gère les artistes, questions et tags existants ou nouveaux
 * @param {Object} parsedData - Données retournées par parse()
 * @returns {Promise<Object>} Résultat de l'import avec les instances créées
 */
export async function importToDatabase(parsedData) {
  const results = {
    success: true,
    created: {
      interviews: [],
      extraits: [],
      artistes: [],
      questions: [],
      tags: [],
      themes: []
    },
    errors: []
  };

  try {
    // 1. Récupérer ou créer les artistes
    const artistesMap = new Map();
    for (const artisteName of new Set(parsedData.extraits.map(e => e.artiste))) {
      try {
        // Chercher l'artiste existant
        const artistes = await Artiste.search(artisteName);
        let artiste = artistes.find(a => a.nom?.toLowerCase() === artisteName.toLowerCase());
        
        if (!artiste) {
          // Créer un nouvel artiste
          artiste = new Artiste({ 'name': artisteName });
          await artiste.create();
          results.created.artistes.push(artiste);
        }
        
        artistesMap.set(artisteName, artiste);
      } catch (error) {
        results.errors.push(`Erreur artiste ${artisteName}: ${error.message}`);
      }
    }

    // Récupérer ou créer les thèmes
    const themesMap = new Map();
    for (const themeText of new Set(parsedData.extraits.map(e => e.theme).filter(Boolean))) {
      try {
        const themes = await theme.search(themeText);
        let theme = themes.find(q => q.texte?.toLowerCase() === themeText.toLowerCase());
        
        if (!theme) {
          theme = new Theme({ 'name': themeText });
          await Theme.create();
          results.created.themes.push(theme);
        }
        
        themesMap.set(themeText, theme);
      } catch (error) {
        results.errors.push(`Erreur theme: ${error.message}`);
      }
    }

    // 2. Récupérer ou créer les questions
    const questionsMap = new Map();
    for (const questionText of new Set(parsedData.extraits.map(e => e.question).filter(Boolean))) {
      try {
        const questions = await Question.search(questionText);
        let question = questions.find(q => q.texte?.toLowerCase() === questionText.toLowerCase());
        
        if (!question) {
          question = new Question({ texte: questionText });
          await question.create();
          results.created.questions.push(question);
        }
        
        questionsMap.set(questionText, question);
      } catch (error) {
        results.errors.push(`Erreur question: ${error.message}`);
      }
    }

    // 3. Récupérer ou créer les tags
    const tagsMap = new Map();
    const allTags = new Set(parsedData.extraits.flatMap(e => e.tags));
    for (const tagName of allTags) {
      try {
        const tags = await Tag.search(tagName);
        let tag = tags.find(t => t.nom?.toLowerCase() === tagName.toLowerCase());
        
        if (!tag) {
          tag = new Tag({ 'name': tagName });
          await tag.create();
          results.created.tags.push(tag);
        }
        
        tagsMap.set(tagName, tag);
      } catch (error) {
        results.errors.push(`Erreur tag ${tagName}: ${error.message}`);
      }
    }

    // 4. Créer les interviews
    const interviewsCreated = new Map();

    
    
    for (const interviewData of parsedData.interviews) {
      try {
        // Vérifie si la date est présente et valide
        let formattedDate = null;
        if (interviewData.date && interviewData.date.trim() !== "") {
            const d = new Date(interviewData.date);
            if (!isNaN(d)) {
                formattedDate = d.toISOString().slice(0, 10); // format YYYY-MM-DD
            }
        }


        const interview = new Interview({
          titre: `${interviewData.artiste} - ${interviewData.evenement}`,
          date: formattedDate,
          occasion: interviewData.evenement,
          description: '',
          lieu: interviewData.ville
        });
        
        await interview.create();
        results.created.interviews.push(interview);
        interviewsCreated.set(interviewData.id, interview);
      } catch (error) {
        results.errors.push(`Erreur interview ${interviewData.id}: ${error.message}`);
      }
    }

    // 5. Créer les extraits et les lier
    let i = 0  
    for (const interviewData of parsedData.interviews) {
      const interview = interviewsCreated.get(interviewData.id);
      if (!interview) continue;

      const extraitsToConnect = [];
      for (const extraitData of interviewData.extraits) {
        try {
            i++;
                  // Vérifie si la date est présente et valide
            let formattedDate = null;
            if (extraitData.date && extraitData.date.trim() !== "") {
                const d = new Date(extraitData.date);
                if (!isNaN(d)) {
                    formattedDate = d.toISOString().slice(0, 10); // format YYYY-MM-DD
                }
            }  
            const artiste = artistesMap.get(extraitData.artiste);
            const questionKey = `${extraitData.question}|${extraitData.theme}`;
            const question = questionsMap.get(questionKey);

            if (!artiste) {
                results.errors.push(`Artiste introuvable: ${extraitData.artiste}`);
                continue;
            }

            const extrait = new Extrait({
                titre: extraitData.theme || extraitData.question || `Èxtrait_${i}`,
                description: extraitData.question || '',
                youtube_url: extraitData.youtube,
                vimeo_url: extraitData.vimeo,
                uploaded_at: formattedDate,
                duree: 48
            });

            // Lier l'artiste et la question
            extrait.artiste = artiste.uuid;
            if (question) {
                extrait.question = question.uuid;
            }
            await extrait.create();
            results.created.extraits.push(extrait);

            // Lier les tags
            for (const tagName of extraitData.tags) {
                const tag = tagsMap.get(tagName);
                if (tag) {
                await extrait.connect_tag(tag);
                }
            }

            extraitsToConnect.push(extrait);
        } catch (error) {
            results.errors.push(`Erreur extrait: ${error.message}`);
        }
      }

      // Lier tous les extraits à l'interview avec leur position
      if (extraitsToConnect.length > 0) {
        await interview.setExtraits(extraitsToConnect);
      }
    }

    return results;
  } catch (error) {
    return {
      success: false,
      error: error.message,
      created: results.created,
      errors: results.errors
    };
  }
}

/**
 * Fonction helper pour importer un fichier CSV complet
 * @param {File} file - Le fichier CSV
 * @returns {Promise<Object>} Résultat complet de l'import
 */
export async function parseAndImport(file) {
  const parsed = await parse(file);
  
  if (!parsed.success) {
    return parsed;
  }

  console.log('Données parsées:', parsed.stats);
  
  const imported = await importToDatabase(parsed);
  
  return {
    ...imported,
    stats: parsed.stats
  };
}