export default {
  namespaced: true,
  state: () => ({
    recommendations: [],
    loading: false,
    error: null,
  }),
  mutations: {
    SET_RECOMMENDATIONS(state, recommendations) {
      state.recommendations = recommendations;
    },
    SET_LOADING(state, isLoading) {
      state.loading = isLoading;
    },
    SET_ERROR(state, error) {
      state.error = error;
    },
    CLEAR_ERROR(state) {
      state.error = null;
    },
  },
  actions: {
    async fetchRecommendations({ commit }) {
      commit("SET_LOADING", true);
      commit("CLEAR_ERROR");
      try {
        const response = await fetch(
          "http://localhost:8000/recommend/new_releases/",
        ); // Replace with actual API endpoint
        if (!response.ok) throw new Error("Failed to fetch recommendations");
        const data = await response.json();
        commit("SET_RECOMMENDATIONS", data);
      } catch (error) {
        commit("SET_ERROR", error.message);
        this.$logger.error("Error fetching recommendations:", error);
        this.logError("Error fetching recommendations", error); // Log the error
      } finally {
        commit("SET_LOADING", false);
      }
    },
  },
  getters: {
    getRecommendations: (state) => state.recommendations,
    isLoading: (state) => state.loading,
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
