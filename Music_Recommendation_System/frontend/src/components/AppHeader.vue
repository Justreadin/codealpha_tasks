<template>
  <header class="bg-gradient-to-r from-blue-600 to-purple-600 shadow-lg">
    <!-- Desktop Layout -->
    <div
      class="hidden lg:grid grid-cols-[auto,1fr,auto] items-center px-6 py-4"
    >
      <!-- Logo Section -->
      <div class="flex items-center space-x-4">
        <h1 class="text-red text-xl font-bold tracking-wide">Lyrical AI</h1>
      </div>

      <!-- Navigation Buttons -->
      <nav class="flex items-center justify-center space-x-6">
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
        <button @click="navigateToChat" class="icon-button">
          <i class="fas fa-comments"></i>
          <span>Chat</span>
        </button>
      </nav>

      <!-- Profile Section -->
      <div class="flex items-center space-x-4">
        <button
          @click="handleProfileClick"
          class="flex items-center space-x-2 bg-white px-4 py-2 rounded-full shadow-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-400"
        >
          <span class="text-gray-700 font-medium hidden md:block">Welcome</span>
        </button>
      </div>
    </div>

    <!-- Mobile Layout -->
    <div class="lg:hidden flex items-center justify-between px-4 py-3">
      <!-- Logo Section -->
      <div class="flex items-center space-x-4">
        <h1 class="text-white text-lg font-semibold tracking-wide">
          Lyrical AI
        </h1>
      </div>

      <!-- Menu Toggle Button -->
      <button
        @click="toggleSidebar"
        class="text-white text-2xl focus:outline-none"
      >
        <i class="fas fa-bars"></i>
      </button>
    </div>

    <!-- Sidebar for Mobile -->
    <transition name="slide">
      <div
        v-if="showSidebar"
        class="fixed inset-0 bg-gray-900 bg-opacity-80 z-50"
      >
        <div
          class="w-64 bg-gradient-to-r from-indigo-700 via-purple-600 to-pink-600 h-full flex flex-col p-6"
        >
          <button @click="toggleSidebar" class="text-white self-end mb-6">
            <i class="fas fa-times text-2xl"></i>
          </button>
          <nav class="flex flex-col space-y-4">
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
            <button @click="navigateToChat" class="icon-button">
              <i class="fas fa-comments"></i>
              <span>Chat</span>
            </button>
          </nav>
        </div>
      </div>
    </transition>
  </header>
</template>

<script>
export default {
  data() {
    return {
      showSidebar: false, // Sidebar visibility state
    };
  },
  methods: {
    navigateToHome() {
      this.$router.push({ name: "home" });
    },
    navigateToRecommendations() {
      this.$router.push({ name: "recommendations" });
    },
    navigateToPlaylists() {
      this.$router.push({ name: "song-playlists" });
    },
    navigateToSearch() {
      this.$router.push({ name: "search" });
    },
    navigateToChat() {
      this.$router.push({ name: "user-chat" });
    },
    handleProfileClick() {
      alert("Profile clicked!");
    },
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
    },
  },
};
</script>
<style scoped>
/* Shared styles for navigation buttons */
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

/* Mobile sidebar transition */
::v-deep(.slide-enter-active),
::v-deep(.slide-leave-active) {
  transition: transform 0.3s ease;
}

::v-deep(.slide-enter-from) {
  transform: translateX(-100%);
}

::v-deep(.slide-leave-to) {
  transform: translateX(-100%);
}
</style>
