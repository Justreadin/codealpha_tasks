export default {
  namespaced: true,
  state: () => ({
    messages: [], // Stores chat messages
    loading: false, // Tracks loading state
    error: null, // Tracks errors
    typing: false, // Indicates if the bot is typing
  }),
  mutations: {
    ADD_MESSAGE(state, message) {
      state.messages.push(message);
    },
    SET_LOADING(state, isLoading) {
      state.loading = isLoading;
    },
    SET_TYPING(state, isTyping) {
      state.typing = isTyping;
    },
    SET_ERROR(state, error) {
      state.error = error;
    },
    CLEAR_ERROR(state) {
      state.error = null;
    },
    CLEAR_CHAT(state) {
      state.messages = [];
    },
  },
  actions: {
    async sendMessage({ commit }, { sender, text }) {
      // Add user message to chat
      commit("ADD_MESSAGE", { sender, text, timestamp: new Date() });

      // Simulate bot typing
      commit("SET_TYPING", true);

      try {
        // Simulated delay for typing effect
        await new Promise((resolve) => setTimeout(resolve, 1000));

        // API call to get bot's response
        const response = await fetch("http://localhost:8000/chat/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: text }),
        });

        if (!response.ok)
          throw new Error("Failed to get a response from the chat API");

        const data = await response.json();

        // Add bot's response to chat
        commit("ADD_MESSAGE", {
          sender: "Lyrical AI",
          text: data.reply,
          timestamp: new Date(),
        });
      } catch (error) {
        this.$logger.error("Error during chat:", error);
        commit("SET_ERROR", error.message);
        this.logError("Error during chat interaction", error); // Log the error
      } finally {
        // End bot typing
        commit("SET_TYPING", false);
      }
    },
    clearChat({ commit }) {
      commit("CLEAR_CHAT");
    },
  },
  getters: {
    getMessages: (state) => state.messages,
    isLoading: (state) => state.loading,
    isTyping: (state) => state.typing,
    hasError: (state) => !!state.error,
    errorMessage: (state) => state.error,
  },

  methods: {
    logError(message, error) {
      // Log error details to backend (where Winston is set up)
      fetch("http://localhost:8000/log/error", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message,
          error: error.message || "No additional error info",
          stack: error.stack || "No stack trace",
          timestamp: new Date().toISOString(),
        }),
      }).catch((err) => {
        this.$logger.error("Failed to log error:", err);
      });
    },
  },
};
