import { createRouter, createWebHistory } from "vue-router";
import axios from "axios";

// Importing Views
import HomeView from "../views/HomeView.vue";
import RecommendationsView from "../views/RecommendationsView.vue";
import PlaylistView from "../views/PlaylistView.vue";
import SearchView from "../views/SearchView.vue";
import ChatView from "../views/ChatView.vue"; // Adjust the path if necessary

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    beforeEnter: async (to, from, next) => {
      try {
        const response = await axios.get("http://localhost:8000/home-data"); // Updated URL
        to.meta.apiData = response.data; // Pass data to the route's meta field
        next();
      } catch (error) {
        const errorMessage = "Error fetching home data";
        this.$logger.error(errorMessage, error);
        logError(errorMessage, error); // Log error to backend
        next(); // Continue to the route even if the API call fails
      }
    },
  },
  {
    path: "/recommendations",
    name: "recommendations",
    component: RecommendationsView,
    beforeEnter: async (to, from, next) => {
      try {
        const userId = to.params.user_id || "default_user"; // Dynamic user ID handling
        const response = await axios.get(
          `http://localhost:8000/recommend/combined/${userId}`,
        );
        to.meta.apiData = response.data; // Pass data to the route's meta field
        next();
      } catch (error) {
        const errorMessage = `Error fetching recommendations data for user: ${to.params.user_id}`;
        this.$logger.error(errorMessage, error);
        logError(errorMessage, error); // Log error to backend
        next();
      }
    },
  },
  {
    path: "/playlists",
    name: "song-playlists", // Use kebab-case naming convention for routes
    component: PlaylistView,
    beforeEnter: async (to, from, next) => {
      try {
        const userId = to.params.user_id || "default_user"; // Dynamic user ID handling
        const response = await axios.get(
          `http://localhost:8000/user/${userId}/generate_playlist/`,
        );
        to.meta.apiData = response.data;
        next();
      } catch (error) {
        const errorMessage = `Error fetching playlists data for user: ${to.params.user_id}`;
        this.$logger.error(errorMessage, error);
        logError(errorMessage, error); // Log error to backend
        next();
      }
    },
  },
  {
    path: "/search",
    name: "search",
    component: SearchView,
    beforeEnter: async (to, from, next) => {
      try {
        const response = await axios.get("http://localhost:8000/search"); // Updated URL
        to.meta.apiData = response.data;
        next();
      } catch (error) {
        const errorMessage = "Error fetching search data";
        this.$logger.error(errorMessage, error);
        logError(errorMessage, error); // Log error to backend
        next();
      }
    },
  },
  {
    path: "/chat",
    name: "user-chat", // Use kebab-case naming convention for routes
    component: ChatView,
    beforeEnter: async (to, from, next) => {
      try {
        const response = await axios.get("http://localhost:8000/chat"); // Updated URL
        to.meta.apiData = response.data;
        next();
      } catch (error) {
        const errorMessage = "Error fetching chat data";
        this.$logger.error(errorMessage, error);
        logError(errorMessage, error); // Log error to backend
        next();
      }
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

// Log error method outside the default export
function logError(message, error) {
  // Log error details to backend (where Winston is set up)
  axios
    .post("http://localhost:8000/log/error", {
      message: message,
      error: error.message || "No additional error info",
      stack: error.stack || "No stack trace",
      timestamp: new Date().toISOString(),
    })
    .catch((err) => {
      this.$logger.error("Failed to log error:", err);
    });
}
