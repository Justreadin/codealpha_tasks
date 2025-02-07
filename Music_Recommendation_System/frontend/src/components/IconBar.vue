<template>
  <div
    class="bg-gradient-to-r from-indigo-700 via-purple-600 to-pink-600 p-4 rounded-lg shadow-xl flex justify-around items-center"
  >
    <!-- Navigation Buttons -->
    <div class="flex space-x-6">
      <button @click="navigateToHome" class="icon-button">
        <i class="fas fa-home"></i>
        <span>Home</span>
      </button>

      <button @click="navigateToRecommendations" class="icon-button">
        <i class="fas fa-star"></i>
        <span>Recommendations</span>
      </button>

      <button @click="navigateToPlaylists" class="icon-button">
        <i class="fas fa-music"></i>
        <span>Playlists</span>
      </button>

      <button @click="navigateToSearch" class="icon-button">
        <i class="fas fa-search"></i>
        <span>Search</span>
      </button>
    </div>

    <!-- Chat Button -->
    <button @click="navigateToChat" class="icon-button">
      <i class="fas fa-comments"></i>
      <span>Chat</span>
    </button>

    <!-- Floating Chat Button -->
    <div
      @click="toggleChat"
      class="fixed bottom-6 right-6 bg-gradient-to-r from-pink-500 to-purple-600 p-4 rounded-full shadow-lg cursor-pointer hover:scale-110 transform transition duration-300"
    >
      <i class="fas fa-comments text-white text-2xl"></i>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    navigateToHome() {
      this.$router.push({ name: "home" });
    },
    navigateToRecommendations() {
      this.$router.push({ name: "recommendations" });
    },
    navigateToPlaylists() {
      this.$router.push({ name: "song-playlists" }); // Updated route name to kebab-case
    },
    navigateToSearch() {
      this.$router.push({ name: "search" });
    },
    navigateToChat() {
      this.$router.push({ name: "user-chat" }); // Updated route name to kebab-case
    },
    toggleChat() {
      // Logic to show or hide the chat interface
      const chatElement = document.getElementById("chat-interface");
      if (chatElement) chatElement.classList.toggle("hidden");
    },
  },
};
</script>
<style scoped>
/* Styling for icon buttons */
::v-deep(.icon-button) {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  transition:
    transform 0.2s ease-in-out,
    color 0.2s ease-in-out;
}

::v-deep(.icon-button i) {
  font-size: 1.5rem;
  margin-bottom: 4px;
}

::v-deep(.icon-button:hover) {
  color: #4fd1c5; /* Teal hover effect */
  transform: translateY(-4px);
}

/* Floating chat button hover animation */
::v-deep(button:hover) {
  transform: scale(1.1);
  transition: transform 0.3s ease-in-out;
}
</style>
