<template>
  <div
    class="bg-gradient-to-r from-blue-500 via-teal-500 to-green-500 p-6 rounded-3xl shadow-2xl w-full max-w-lg mx-auto"
  >
    <div
      class="bg-gray-800 p-6 rounded-xl shadow-2xl transform transition-all hover:scale-105 hover:rotate-3d"
    >
      <h2 class="text-2xl font-extrabold mb-6 text-red-500 text-center">
        Your Playlists
      </h2>

      <div v-if="isLoading" class="flex justify-center items-center space-x-2">
        <span class="text-white text-lg">Loading Playlists...</span>
        <svg
          class="animate-spin h-6 w-6 text-red-500"
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

      <ul v-else-if="playlists.length > 0" class="space-y-6">
        <li
          v-for="playlist in playlists"
          :key="playlist.id"
          class="flex justify-between bg-gray-700 p-5 rounded-xl shadow-xl transform hover:scale-105 transition-all"
        >
          <div class="flex flex-col justify-between w-3/4">
            <span class="text-white text-xl font-semibold">{{
              playlist.name
            }}</span>
            <span class="text-gray-400 text-sm"
              >{{ playlist.song_count }} songs</span
            >
          </div>
          <button
            @click="viewPlaylist(playlist)"
            class="bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-600 focus:ring-4 focus:ring-red-300 transition-all"
          >
            View
          </button>
        </li>
      </ul>

      <p v-else class="text-white text-center text-lg">
        No playlists found. Create a new one!
      </p>

      <input
        v-model="newPlaylistName"
        placeholder="Create a new playlist"
        class="w-full p-3 mt-6 rounded-md bg-gray-700 text-white placeholder-gray-400 focus:outline-none"
        @keyup.enter="createPlaylist"
      />

      <div v-if="error" class="mt-6 text-red-500 text-center">
        <span>{{ errorMessage }}</span>
      </div>
    </div>

    <div
      ref="canvasContainer"
      class="w-full h-72 mt-6 bg-black rounded-3xl shadow-2xl"
    ></div>
  </div>
</template>

<script>
import axios from "axios";
import * as THREE from "three";
import logger from "@/utils/logger";

export default {
  data() {
    return {
      playlists: [],
      newPlaylistName: "",
      isLoading: true,
      error: false,
      errorMessage: "",
    };
  },
  methods: {
    async fetchPlaylists() {
      this.isLoading = true;
      this.error = false;

      try {
        const response = await axios.get("/user/playlists");
        this.playlists = response.data.playlists;
        logger.info("Playlists fetched successfully"); // Log successful fetch
      } catch (error) {
        this.error = true;
        this.errorMessage = "Error fetching playlists. Please try again later.";
        logger.error("Error fetching playlists:", error); // Log the error
      } finally {
        this.isLoading = false;
      }
    },

    async createPlaylist() {
      if (!this.newPlaylistName.trim()) return;

      try {
        const response = await axios.post("/user/create_playlist", {
          name: this.newPlaylistName,
        });

        this.playlists.push(response.data.playlist);
        this.newPlaylistName = "";
        logger.info(`Playlist '${this.newPlaylistName}' created successfully`); // Log playlist creation
      } catch (error) {
        logger.error("Error creating playlist:", error); // Log creation error
      }
    },

    viewPlaylist(playlist) {
      logger.info("Viewing playlist:", playlist); // Log playlist view
    },

    setup3DArt() {
      const container = this.$refs.canvasContainer;

      if (!container.clientWidth || !container.clientHeight) {
        logger.error("Canvas container has zero dimensions."); // Log container error
        return;
      }

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(
        75,
        container.clientWidth / container.clientHeight,
        0.1,
        8000,
      );

      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(container.clientWidth, container.clientHeight);
      container.appendChild(renderer.domElement);

      const geometry = new THREE.ConeGeometry(1, 3, 5);
      const material = new THREE.MeshBasicMaterial({
        color: 0xffff00,
        wireframe: true,
      });
      const note = new THREE.Mesh(geometry, material);
      note.rotation.x = Math.PI / 4;
      scene.add(note);

      const light = new THREE.PointLight(0x00ff00, 1, 100);
      light.position.set(5, 5, 5);
      scene.add(light);

      camera.position.z = 6;

      const animate = () => {
        requestAnimationFrame(animate);
        note.rotation.y += 0.01;
        renderer.render(scene, camera);
      };

      animate();
    },
  },
  mounted() {
    this.fetchPlaylists();
    this.setup3DArt();
  },
};
</script>
<style scoped>
/* Enhanced container with rounded corners and 3D effects */
::v-deep(.bg-gray-700) {
  box-shadow:
    8px 8px 15px rgba(0, 0, 0, 0.3),
    -8px -8px 15px rgba(255, 255, 255, 0.2);
}

/* Input field with smooth transitions */
::v-deep(input) {
  transition: all 0.3s ease;
}

::v-deep(input:focus) {
  transform: scale(1.05);
}

/* Button hover effect */
::v-deep(button:hover) {
  transform: scale(1.05);
}

/* Loading spinner animation */
::v-deep(svg) {
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

/* Container hover 3D effect */
::v-deep(.transform:hover) {
  transform: scale(1.05) rotate(5deg);
}
</style>
