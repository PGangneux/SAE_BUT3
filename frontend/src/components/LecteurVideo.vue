<script>
import IframeLectureVideo from './IframeLectureVideo.vue';
import ParametresVideo from "./ParametresVideo.vue";
import PictureInPicture from "./PictureInPicture.vue";
import BarListeVideo from "./BarListeVideo.vue";

export default {
  components: {
    IframeLectureVideo,
    ParametresVideo,
    PictureInPicture,
    BarListeVideo
  }
};

</script>

<template>
  <main>
    <IframeLectureVideo url="https://www.youtube.com/embed/10MZrDXjby8" />
    <div>
      <h2>Title</h2>
      <ParametresVideo />
      <PictureInPicture />
      <div>
        <p>Video description</p>
      </div>
    </div>
  </main>
  <aside>
    <BarListeVideo />
  </aside>
</template>
