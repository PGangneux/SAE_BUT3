import ClientAPI from "./clientAPI.js";

/**
 * Parse un fichier CSV contenant des extraits d'interviews d'artistes
 * et crée les instances des Models correspondants
 * @param {File|string} file - Le fichier CSV ou son contenu
 * @returns {Promise<Object>} Objet contenant les données parsées
 */
export async function parse(file) {
  console.log("Parsing CSV...");
  console.log(file);
  console.log("import")
  ClientAPI.sendFile(ClientAPI.BASE_URL + "api/csv_import/", file  );

}


