<template>
  <div>
    <h1 class="text-2xl font-bold mb-4 text-red-500">Your Recommendations</h1>
    <Recommendations />
  </div>
</template>

<script>
import Recommendations from "../components/SongRecommendations.vue";

export default {
  components: {
    Recommendations,
  },
};
</script>
