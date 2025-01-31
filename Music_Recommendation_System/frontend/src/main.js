import { createApp } from "vue";
import App from "./App.vue";
// import './assets/styles.css'; // Optional: custom CSS overrides if needed
import router from "./router"; // Router configuration
import store from "./store"; // Import Vuex store
import "@fortawesome/fontawesome-free/css/all.css";
import axios from "axios";

// Set up Axios to connect to the Python backend
axios.defaults.baseURL = "http://localhost:8000"; // Replace with your backend's base URL
axios.defaults.headers.common["Content-Type"] = "application/json"; // Optional: for JSON content type

// Add Axios interceptors for automatic logging of errors
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    this.$logger.error("Axios Error:", error);

    // Attempt to send error log to the backend
    try {
      await axios.post("/log", {
        level: "error",
        message: `Axios request failed: ${error.message}`,
      });
    } catch (loggingError) {
      this.$logger.error("Error logging to backend:", loggingError);
    }

    return Promise.reject(error);
  },
);

// Utility to send logs manually from anywhere in the app
const sendLogToBackend = async (level, message) => {
  try {
    await axios.post("/log", { level, message });
  } catch (err) {
    this.$logger.error("Failed to send log to backend:", err);
  }
};

// Add Axios and the logging utility to the global properties of Vue
const app = createApp(App);
app.config.globalProperties.$axios = axios; // Access `this.$axios` in components
app.config.globalProperties.$log = sendLogToBackend; // Access `this.$log` for manual logging

app.use(router); // Use the router
app.use(store); // Use the Vuex store

app.mount("#app");
