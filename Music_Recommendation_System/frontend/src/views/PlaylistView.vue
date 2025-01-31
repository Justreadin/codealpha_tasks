<template>
  <div>
    <h1 class="text-2xl font-bold mb-4 text-red-500">Your Playlists</h1>
    <SongPlaylist />
  </div>
</template>

<script>
import SongPlaylist from "../components/SongPlaylist.vue";

export default {
  components: {
    SongPlaylist,
  },
};
</script>
