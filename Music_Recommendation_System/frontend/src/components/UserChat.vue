<template>
  <div
    class="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-700 p-4"
  >
    <div
      class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 p-4 sm:p-6 rounded-3xl shadow-2xl w-full max-w-md md:max-w-lg"
    >
      <div class="bg-gray-800 p-4 sm:p-6 rounded-xl shadow-inner">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold text-white">🎵 Lyrical AI Chat</h2>
          <div class="flex items-center space-x-2">
            <span class="text-gray-400 text-sm">Connected</span>
            <div class="w-3 h-3 rounded-full bg-green-400 animate-pulse"></div>
          </div>
        </div>

        <div
          class="overflow-y-auto h-72 sm:h-96 bg-gray-900 p-4 rounded-xl space-y-4 scrollbar-thin scrollbar-thumb-indigo-500 scrollbar-track-gray-700"
        >
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="flex items-start"
            :class="{ 'justify-end': message.sender === 'User' }"
          >
            <div
              :class="
                message.sender === 'User'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-700 text-white'
              "
              class="p-3 rounded-xl shadow-xl max-w-xs"
            >
              <p class="text-sm">{{ message.text }}</p>
            </div>
          </div>
        </div>

        <div class="flex items-center mt-4 space-x-2">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            placeholder="Type your message..."
            class="flex-1 p-3 text-lg rounded-full bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <button
            @click="sendMessage"
            class="bg-gradient-to-r from-blue-500 to-teal-500 text-white px-4 py-2 rounded-full shadow-md hover:scale-105 transform transition-transform"
          >
            Send
          </button>
        </div>
      </div>

      <div
        class="absolute top-4 left-4 md:top-8 md:left-8 animate-pulse text-white opacity-70"
      >
        🎶
      </div>
      <div
        class="absolute bottom-4 right-4 md:bottom-8 md:right-8 animate-pulse text-white opacity-70"
      >
        🎵
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      messages: [],
      userInput: "",
      platform: "", // Use platform instead of userId
    };
  },
  created() {
    // Retrieve platform from localStorage when the component is created
    this.platform = localStorage.getItem("platform") || "Unknown Device";
  },
  methods: {
    sendMessage() {
      if (this.userInput.trim() === "") return;

      this.messages.push({ sender: "User", text: this.userInput });

      this.getResponse(this.userInput);
      this.userInput = "";
    },
    async getResponse(input) {
      try {
        const response = await fetch(`http://localhost:8000/chat/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: input,
            platform: this.platform, // Use the retrieved platform
            top_n: 5,
          }),
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        this.messages.push({
          sender: "Lyrical AI",
          text: data.reply || "No response from AI",
        });
      } catch (error) {
        this.$logger.error("Error fetching chat response:", error);
        this.logError("Error fetching chat response", error); // Log error to backend
        this.messages.push({
          sender: "Lyrical AI",
          text: "Error fetching response",
        });
      }
    },

    logError(message, error) {
      // Log error details to backend (where Winston is set up)
      this.$axios
        .post("http://localhost:8000/log/error", {
          message: message,
          error: error.toString(),
          timestamp: new Date().toISOString(),
        })
        .catch((err) => {
          this.$logger.error("Failed to log error:", err);
        });
    },
  },
};
</script>

<style scoped>
/* Responsive & Neumorphic Design Enhancements */
.bg-gray-800 {
  box-shadow:
    inset 8px 8px 15px rgba(0, 0, 0, 0.2),
    inset -8px -8px 15px rgba(255, 255, 255, 0.1);
}

.bg-gray-900 {
  box-shadow:
    inset 8px 8px 15px rgba(0, 0, 0, 0.25),
    inset -8px -8px 15px rgba(255, 255, 255, 0.1);
}

button {
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}
button:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.scrollbar-thin {
  scrollbar-width: thin;
}

.scrollbar-thumb-indigo-500 {
  background-color: #667eea;
}

.scrollbar-track-gray-700 {
  background-color: #2d3748;
}

/* Music Notes Animation */
@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
.animate-pulse {
  animation: bounce 2s infinite;
}

/* Responsive Design */
@media (max-width: 640px) {
  .h-96 {
    height: 20rem;
  }

  .max-w-md {
    width: 100%;
  }

  input {
    font-size: 0.9rem;
  }

  button {
    padding: 0.6rem 1rem;
  }
}
</style>
