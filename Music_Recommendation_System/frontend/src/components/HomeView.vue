<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- AppHeader -->
    <AppHeader />

    <!-- Main Content Area -->
    <div class="flex flex-1">
      <!-- Icon Bar -->
      <div class="hidden lg:block w-16 bg-gray-200">
        <IconBar />
      </div>

      <!-- Main Content -->
      <div class="flex-1 px-4 py-6 space-y-6">
        <!-- Recommendations Section -->
        <SongRecommendations />

        <!-- Device-Specific Recommendations -->
        <DeviceSpecific />

        <!-- Trending Songs Section -->
        <TrendingSongs />

        <Visual3D />
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from "../components/AppHeader.vue";
import IconBar from "../components/IconBar.vue";
import SongRecommendations from "./SongRecommendations.vue";
import DeviceSpecific from "../components/DeviceSpecific.vue";
import TrendingSongs from "./TrendingSongs.vue";
import Visual3D from "../components/Visual3D.vue";

export default {
  components: {
    AppHeader,
    IconBar,
    SongRecommendations,
    DeviceSpecific,
    TrendingSongs,
    Visual3D,
  },
};
</script>

<style scoped>
/* Add specific styles here if needed */
</style>
