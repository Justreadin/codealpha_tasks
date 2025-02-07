<template>
  <div
    class="bg-gradient-to-r from-blue-500 via-teal-500 to-green-500 p-6 rounded-3xl shadow-2xl w-full max-w-lg mx-auto"
  >
    <h2 class="text-2xl font-extrabold mb-6 text-yellow-400 text-center">
      Recommended For You
    </h2>

    <!-- Display Personalized Recommendations, New Releases, and Similar Songs -->
    <div v-if="recommendations.length">
      <h3 class="text-xl font-semibold text-white mb-4">
        Personalized & Spotify Recommendations
      </h3>
      <ul class="space-y-6">
        <li
          v-for="item in recommendations.personalizedAndSpotify"
          :key="item.id"
          class="flex items-center justify-between bg-gray-800 p-4 rounded-lg shadow-lg transform hover:scale-105 transition-all"
        >
          <div>
            <p class="text-lg text-white font-medium">{{ item.title }}</p>
            <p class="text-sm text-gray-400">{{ item.artist }}</p>
          </div>
          <button
            class="bg-yellow-500 text-black py-2 px-4 rounded-md hover:bg-yellow-600 transition-colors"
            @click="playSong(item)"
          >
            Play
          </button>
        </li>
      </ul>
    </div>

    <!-- Display New Releases -->
    <div v-if="newReleases.length" class="mt-8">
      <h3 class="text-xl font-semibold text-white mb-4">New Releases</h3>
      <ul class="space-y-6">
        <li
          v-for="item in newReleases"
          :key="item.id"
          class="flex items-center justify-between bg-gray-800 p-4 rounded-lg shadow-lg transform hover:scale-105 transition-all"
        >
          <div>
            <p class="text-lg text-white font-medium">{{ item.title }}</p>
            <p class="text-sm text-gray-400">{{ item.artist }}</p>
          </div>
          <a
            :href="item.url"
            class="bg-yellow-500 text-black py-2 px-4 rounded-md hover:bg-yellow-600 transition-colors"
            target="_blank"
          >
            Listen on Spotify
          </a>
        </li>
      </ul>
    </div>

    <!-- Display Similar Songs -->
    <div v-if="similarSongs.length" class="mt-8">
      <h3 class="text-xl font-semibold text-white mb-4">Similar Songs</h3>
      <ul class="space-y-6">
        <li
          v-for="item in similarSongs"
          :key="item.id"
          class="flex items-center justify-between bg-gray-800 p-4 rounded-lg shadow-lg transform hover:scale-105 transition-all"
        >
          <div>
            <p class="text-lg text-white font-medium">{{ item.title }}</p>
            <p class="text-sm text-gray-400">{{ item.artist }}</p>
          </div>
          <button
            class="bg-yellow-500 text-black py-2 px-4 rounded-md hover:bg-yellow-600 transition-colors"
            @click="playSong(item)"
          >
            Play
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import logger from "@/utils/logger";

export default {
  data() {
    return {
      recommendations: { personalizedAndSpotify: [] }, // Combined personalized + Spotify recommendations
      newReleases: [], // New releases fetched from the API
      similarSongs: [], // Similar songs fetched from the API
      platform: null, // Platform to fetch recommendations for
    };
  },
  created() {
    this.platform = localStorage.getItem("platform"); // Retrieve platform from localStorage
    this.fetchRecommendations();
    this.fetchNewReleases();
    this.fetchSimilarSongs();
  },
  methods: {
    // Fetch personalized + Spotify recommendations from the API
    async fetchRecommendations() {
      try {
        if (!this.platform) {
          logger.error("Platform not found in localStorage.");
          return;
        }

        const response = await this.$axios.get(
          `http://localhost:8000/recommend/combined/${this.platform}`,
        );

        const recommendations = this.transformRecommendations(response.data);
        this.recommendations.personalizedAndSpotify = recommendations;

        logger.info(
          "Fetched personalized and Spotify recommendations successfully.",
        );
      } catch (error) {
        logger.error("Error fetching recommendations:", error);
      }
    },

    // Fetch new releases from the API
    async fetchNewReleases() {
      try {
        const response = await this.$axios.get(
          `http://localhost:8000/recommend/new_releases/`,
        );

        this.newReleases = response.data.recommendations.map((item, index) => ({
          id: index,
          title: item.name,
          artist: item.artist,
          url: item.url,
        }));

        logger.info("Fetched new releases successfully.");
      } catch (error) {
        logger.error("Error fetching new releases:", error);
      }
    },

    // Fetch similar songs from the API
    async fetchSimilarSongs() {
      try {
        const songName = "example_song"; // Replace with dynamic song name if available
        const response = await this.$axios.get(
          `http://localhost:8000/recommend/similar_songs/${songName}`,
        );

        this.similarSongs = response.data.map((item, index) => ({
          id: index,
          title: item.song,
          artist: "Similar Artist", // Placeholder, adjust as needed
        }));

        logger.info("Fetched similar songs successfully.");
      } catch (error) {
        logger.error("Error fetching similar songs:", error);
      }
    },

    // Transform the combined response to match the frontend structure
    transformRecommendations(data) {
      const personalizedRecommendations = data.personalized_recommendations.map(
        (song, index) => ({
          id: index,
          title: song,
          artist: "Personalized", // Placeholder for artist
        }),
      );

      const spotifyRecommendations = data.spotify_recommendations.map(
        (item, index) => ({
          id: `spotify-${index}`,
          title: item.name,
          artist: item.artist,
        }),
      );

      return [...personalizedRecommendations, ...spotifyRecommendations];
    },

    // Handle song playback (extend as necessary)
    playSong(item) {
      logger.info(`Playing: ${item.title} by ${item.artist}`);
      // Logic for triggering song playback can go here
    },
  },
};
</script>
<style scoped>
/* Container hover effect with smooth transition */
::v-deep(.bg-gray-800) {
  box-shadow:
    8px 8px 15px rgba(0, 0, 0, 0.3),
    -8px -8px 15px rgba(255, 255, 255, 0.2);
}

/* Add smooth hover and transition effects */
::v-deep(button:hover) {
  transform: scale(1.05);
}

::v-deep(ul) {
  transition: all 0.3s ease;
}

::v-deep(ul li:hover) {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Animate play button */
::v-deep(button) {
  transition: all 0.3s ease;
}

::v-deep(button:hover) {
  background-color: #fbbf24;
  transform: scale(1.05);
}
</style>
