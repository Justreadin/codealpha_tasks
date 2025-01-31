<template>
  <div
    class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-700 text-white grid grid-rows-[auto,1fr]"
  >
    <!-- AppHeader with Combined Navigation and Icon Bar -->
    <AppHeader />

    <!-- Main Content Area -->
    <div
      class="p-4 lg:p-6 bg-gray-800 rounded-lg shadow-md m-0 lg:m-0 overflow-hidden w-full"
    >
      <router-view />
    </div>

    <!-- Floating Chat Button -->
    <button
      @click="toggleChat"
      class="fixed bottom-4 right-4 md:bottom-6 md:right-6 bg-gradient-to-r from-blue-500 to-teal-500 text-white p-4 md:p-5 rounded-full shadow-xl hover:scale-110 transform transition-transform duration-300 ease-in-out focus:outline-none focus:ring-4 focus:ring-teal-300"
      aria-label="Chat"
    >
      💬
    </button>

    <!-- Chat Component -->
    <transition name="fade">
      <UserChat
        v-if="showChat"
        @close="toggleChat"
        class="fixed bottom-16 right-4 md:right-6 w-full md:w-80 h-3/4 md:h-96 bg-gray-900 rounded-lg shadow-lg p-4"
      />
    </transition>
  </div>
</template>

<script>
import AppHeader from "./components/AppHeader.vue";
import UserChat from "./components/UserChat.vue";

export default {
  components: {
    AppHeader,
    UserChat,
  },
  data() {
    return {
      showChat: false, // State to control chat visibility
    };
  },
  methods: {
    toggleChat() {
      this.showChat = !this.showChat;
    },
  },
};
</script>

<style scoped>
/* Smooth fade animation for the chat component */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Floating Chat Button Styling */
button:focus {
  outline: none;
}

/* Main Content Area */
main {
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.05);
  width: 100%;
}

/* Enhance scrollbars for modern styling */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-thumb {
  background: linear-gradient(to right, #4fd1c5, #4299e1);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to right, #38b2ac, #3182ce);
}
</style>
