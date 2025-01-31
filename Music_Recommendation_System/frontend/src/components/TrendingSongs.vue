<template>
  <div class="bg-gray-800 p-4 rounded-md shadow-lg mt-4">
    <h2 class="text-xl font-semibold mb-4 text-red-500">Trending Songs</h2>
    <div v-if="isLoading" class="flex justify-center items-center space-x-2">
      <span class="text-white">Loading...</span>
      <svg
        class="animate-spin h-5 w-5 text-red-500"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <circle cx="12" cy="12" r="10" />
        <path d="M22 12a10 10 0 1 1-10 10" />
      </svg>
    </div>
    <ul v-else class="space-y-4 mt-4">
      <li
        v-for="song in trendingSongs"
        :key="song.id"
        class="flex items-center justify-between bg-gray-700 p-3 rounded-md shadow-md hover:bg-gray-600 transition-colors"
      >
        <div>
          <span class="text-white font-medium"
            >{{ song.name }} - {{ song.artist }}</span
          >
          <div v-if="song.genre" class="text-sm text-gray-400">
            {{ song.genre }}
          </div>
        </div>
        <div class="flex space-x-2">
          <button
            @click="playSong(song)"
            class="bg-red-500 text-white py-1 px-3 rounded-md hover:bg-red-600 transition-all"
          >
            Play
          </button>
          <button
            @click="showSongInfo(song)"
            class="bg-transparent text-white py-1 px-3 border border-white rounded-md hover:bg-gray-600 transition-all"
          >
            More Info
          </button>
        </div>
      </li>
    </ul>
    <div v-if="error" class="mt-4 text-red-500">
      <span>Error loading trending songs. Please try again later.</span>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      trendingSongs: [], // Holds the fetched trending songs
      isLoading: true, // Loading state
      error: false, // Error state
    };
  },
  methods: {
    async fetchTrendingSongs() {
      this.isLoading = true; // Start loading
      this.error = false; // Reset error

      try {
        const response = await fetch(
          "https://localhost:8000/recommend/trending?top_n=10",
        ); // Fetch trending songs from backend
        const data = await response.json();

        // Map the response to format the data
        this.trendingSongs = data.map((song, index) => ({
          id: index + 1, // Unique id for each song
          name: song.name,
          artist: song.artist,
          genre: song.genre || "Unknown", // Display genre if available
        }));
      } catch (error) {
        this.error = true; // Set error state if the fetch fails
        this.logError("Error fetching trending songs", error); // Log error to backend
      } finally {
        this.isLoading = false; // End loading
      }
    },

    playSong(song) {
      // Implement song play logic (e.g., send to audio player or service)
      alert(`Now playing: ${song.name} by ${song.artist}`);
    },

    showSongInfo(song) {
      // Display additional song info (could be a modal or another view)
      alert(`More info about: ${song.name} by ${song.artist}`);
    },

    logError(message, error) {
      // Log error details to backend (where Winston is set up)
      this.$axios
        .post("https://localhost:8000/log/error", {
          message: message,
          error: error.toString(),
          timestamp: new Date().toISOString(),
        })
        .catch((err) => {
          this.$logger.error("Failed to log error:", err);
        });
    },
  },
  mounted() {
    // Fetch trending songs when component is mounted
    this.fetchTrendingSongs();
  },
};
</script>

<style scoped>
/* Styling for neumorphism effect */
.bg-gray-800 {
  box-shadow:
    8px 8px 15px rgba(0, 0, 0, 0.2),
    -8px -8px 15px rgba(255, 255, 255, 0.1);
}

button:hover {
  transform: scale(1.05);
}

button:active {
  transform: scale(0.98);
}

ul li {
  transition: all 0.3s ease;
}

ul li:hover {
  box-shadow:
    0 4px 6px rgba(0, 0, 0, 0.3),
    0 2px 4px rgba(255, 255, 255, 0.1);
}

/* Styling for loading spinner */
svg {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
