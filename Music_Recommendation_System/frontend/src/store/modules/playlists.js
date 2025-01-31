export default {
  namespaced: true,
  state: () => ({
    playlists: [],
    loading: false,
    error: null,
  }),
  mutations: {
    SET_PLAYLISTS(state, playlists) {
      state.playlists = playlists;
    },
    ADD_PLAYLIST(state, playlist) {
      state.playlists.push(playlist);
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
    async fetchPlaylists({ commit }) {
      commit("SET_LOADING", true);
      commit("CLEAR_ERROR");
      try {
        const response = await fetch("https://localhost:8000/user/playlists");
        if (!response.ok) throw new Error("Failed to fetch playlists");
        const data = await response.json();
        commit("SET_PLAYLISTS", data);
      } catch (error) {
        commit("SET_ERROR", error.message);
        this.dispatch("logError", {
          message: "Error fetching playlists",
          error,
        });
      } finally {
        commit("SET_LOADING", false);
      }
    },
    async addPlaylist({ commit }, playlistName) {
      commit("CLEAR_ERROR");
      try {
        const response = await fetch("/api/playlists", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: playlistName }),
        });
        if (!response.ok) throw new Error("Failed to add playlist");
        const data = await response.json();
        commit("ADD_PLAYLIST", data);
      } catch (error) {
        commit("SET_ERROR", error.message);
        this.dispatch("logError", { message: "Error adding playlist", error });
      }
    },
  },
  getters: {
    getPlaylists: (state) => state.playlists,
    isLoading: (state) => state.loading,
    hasError: (state) => !!state.error,
    errorMessage: (state) => state.error,
  },
  methods: {
    logError({ message, error }) {
      // Log error details to backend
      fetch("http://localhost:8000/log/error", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: message,
          error: error.message || "No additional error info",
          stack: error.stack || "No stack trace",
          timestamp: new Date().toISOString(),
        }),
      }).catch((err) => {
        // Use logger in case of failure
        this.$logger.error("Failed to log error:", err);
      });
    },
  },
};
