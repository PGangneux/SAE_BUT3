// tests/__mocks__/appMocks.js
import { vi } from "vitest";

vi.mock("../../src/model/model.js", () => ({
  default: class MockModel {}
}));

vi.mock("../../src/model/nation.js", () => ({
  default: class MockNation {}
}));

vi.mock("../../src/model/artiste.js", () => ({
  default: class MockArtiste {}
}));

vi.mock("../../src/model/utilisateur.js", () => ({
  default: class MockUtilisateur {}
}));

vi.mock("../../src/model/videoStore.js", () => ({
  videoStore: {
    uuid: "",
    url_yt: "",
    url_vimeo: "",
    url: "",
    lecteur: "YouTube",
    isPictureInPicture: false,
    currentTime: 0,
    isPlaying: true,
    intervalId: null,
    set_url: null,
    iframeComponent: null,
    chemin: []
  }
}));
