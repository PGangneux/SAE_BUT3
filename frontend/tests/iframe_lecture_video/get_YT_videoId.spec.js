// ne fonctionne pas

// tests/get_YT_videoId.spec.js
import "./../__mocks__/appMocks.js";
import { mount } from "@vue/test-utils";
import { vi, describe, it, expect } from "vitest";
import lecteur from "../../src/components/lecteur_video/lecteur_video.vue";



// Mock du store réel
vi.mock("../../src/model/videoStore", () => ({
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
    chemin: [],
  }
}));

describe("get_YT_videoId", () => {
  it("extrait l'ID depuis différentes URLs YouTube", async () => {
    const wrapper = mount(lecteur);
    const fn = wrapper.vm.get_YT_videoId;

    expect(fn("https://youtu.be/abcd1234")).toBe("abcd1234");
    expect(fn("https://www.youtube.com/watch?v=ZZ99YY")).toBe("ZZ99YY");
    expect(fn("https://youtube.com/embed/HELLO_WORLD")).toBe("HELLO_WORLD");
    expect(fn("https://youtube.com/watch?x=1")).toBe(null);
    expect(fn("not a url")).toBe(null);
  });
});
