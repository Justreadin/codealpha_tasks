import { createStore } from "vuex";
import user from "./modules/user";
import recommendations from "./modules/recommendations";
import playlists from "./modules/playlists";
import chat from "./modules/chat";

const store = createStore({
  modules: {
    user,
    recommendations,
    playlists,
    chat,
  },
});

export default store;
