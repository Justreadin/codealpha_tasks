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

// Add Axios and the logging utility to the global properties of Vue
const app = createApp(App);
app.config.globalProperties.$axios = axios; // Access `this.$axios` in components

app.use(router); // Use the router
app.use(store); // Use the Vuex store

app.mount("#app");
