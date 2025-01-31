<template>
  <div
    class="search-section py-6 px-4 bg-gray-900 rounded-lg shadow-lg relative"
  >
    <h2 class="text-3xl font-bold mb-6 text-yellow-500 text-center">
      Search for Music
    </h2>

    <!-- Search Input with Animation -->
    <div class="relative flex items-center justify-center">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search for songs, playlists, or artists..."
        class="w-80 px-4 py-3 bg-black text-white border-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        @input="fetchSuggestions"
        @focus="showHistory = true"
        @blur="hideHistory"
      />

      <!-- Suggestions Dropdown -->
      <ul
        v-if="suggestions.length && searchQuery"
        class="absolute z-10 bg-black text-white shadow-lg w-full mt-1 rounded-lg overflow-hidden border border-yellow-500"
      >
        <li
          v-for="(suggestion, index) in suggestions"
          :key="index"
          class="px-4 py-2 hover:bg-yellow-500 cursor-pointer"
          @click="selectSuggestion(suggestion)"
        >
          {{ suggestion }}
        </li>
      </ul>

      <!-- Search History -->
      <ul
        v-if="showHistory && !searchQuery && searchHistory.length"
        class="absolute z-10 bg-black text-white shadow-lg w-full mt-1 rounded-lg overflow-hidden border border-yellow-500"
      >
        <li
          v-for="(history, index) in searchHistory"
          :key="index"
          class="px-4 py-2 hover:bg-yellow-500 cursor-pointer"
          @click="selectSuggestion(history)"
        >
          {{ history }}
        </li>
      </ul>
    </div>

    <!-- 3D Visual -->
    <div ref="canvasContainer" class="absolute top-0 left-0 w-full h-full">
      <canvas id="search-canvas"></canvas>
    </div>
  </div>
</template>

<script>
import * as THREE from "three";
import mitt from "mitt";
import logger from "@/utils/logger"; // Import the logger

const emitter = mitt();

export default {
  name: "SearchSection",
  data() {
    return {
      searchQuery: "",
      suggestions: [],
      searchHistory: ["Top 100 Songs", "Classical Hits", "Lo-fi Beats"],
      showHistory: false,
    };
  },
  methods: {
    fetchSuggestions() {
      if (this.searchQuery.trim() === "") {
        this.suggestions = [];
        return;
      }

      // Emit an event to fetch search results
      emitter.emit("search", this.searchQuery);
      logger.info(`Fetching suggestions for query: ${this.searchQuery}`); // Log the query
    },
    selectSuggestion(suggestion) {
      this.searchQuery = suggestion;
      this.suggestions = [];
      this.showHistory = false;
      logger.info(`Selected suggestion: ${suggestion}`); // Log the selected suggestion
    },
    hideHistory() {
      setTimeout(() => (this.showHistory = false), 200);
    },
  },
  mounted() {
    // Listen for search events using mitt
    emitter.on("search", (query) => {
      logger.info(`Search initiated for query: ${query}`); // Log the search query
      this.$axios
        .get(`http://localhost:8000/search/?query=${query}`)
        .then((response) => {
          this.suggestions = [
            ...response.data.songs,
            ...response.data.artists,
            ...response.data.albums,
          ];
          logger.info(
            `Fetched ${response.data.songs.length} songs, ${response.data.artists.length} artists, ${response.data.albums.length} albums`,
          ); // Log results
        })
        .catch((error) => {
          logger.error(
            `Error fetching search results for query "${query}": ${error}`,
          ); // Log the error
        });
    });

    // Initialize 3D visualizer
    const canvas = document.getElementById("search-canvas");
    const container = this.$refs.canvasContainer;

    if (!container || !canvas) {
      logger.error("Error initializing 3D canvas"); // Log error if canvas fails
      return;
    }

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      75,
      container.clientWidth / container.clientHeight,
      0.1,
      8000,
    );

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    scene.background = new THREE.Color(0x1a1a1a);

    // Create a dynamic sphere that pulses to represent music
    const geometry = new THREE.SphereGeometry(2, 64, 64);
    const material = new THREE.MeshStandardMaterial({
      color: 0xff6347,
      emissive: 0xff6347,
      emissiveIntensity: 0.7,
      wireframe: true,
    });
    const sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);

    camera.position.z = 5;

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      sphere.rotation.x += 0.01;
      sphere.rotation.y += 0.01;
      renderer.render(scene, camera);
    };
    animate();

    // Cleanup on component destroy
    // eslint-disable-next-line vue/no-deprecated-events-api
    this.$once("hook:beforeDestroy", () => {
      emitter.off("search"); // Remove event listener
    });
  },
};
</script>

<style scoped>
.search-section {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}

.search-section input:focus {
  border-color: #ff6347; /* Highlight input field */
}

ul {
  position: absolute;
  z-index: 10;
  width: 100%;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 8px;
  color: white;
}

ul li:hover {
  background: #ff6347;
}

.search-section h2 {
  color: #ff6347;
}

#search-canvas {
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
}
</style>
