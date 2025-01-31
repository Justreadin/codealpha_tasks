export default {
  namespaced: true,
  state: () => ({
    user: null,
  }),
  mutations: {
    SET_USER(state, user) {
      state.user = user;
    },
  },
  actions: {
    login({ commit }, user) {
      commit("SET_USER", user);
    },
    logout({ commit }) {
      commit("SET_USER", null);
    },
  },
  getters: {
    isLoggedIn: (state) => !!state.user,
    getUser: (state) => state.user,
  },
};
