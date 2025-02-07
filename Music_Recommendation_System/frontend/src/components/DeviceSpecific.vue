<template>
  <div class="bg-gray-800 p-4 rounded-md shadow-md mt-4">
    <h2 class="text-lg font-bold mb-2 text-red-500">Device Detection</h2>
    <div v-if="isLoading" class="flex justify-center items-center space-x-2">
      <span class="text-white">Detecting device...</span>
      <svg
        class="animate-spin h-5 w-5 text-red-500"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <circle cx="12" cy="12" r="10" />
        <path d="M22 12a10 10 0 1 1-10 10" />
      </svg>
    </div>
    <div v-else>
      <p class="text-white">
        Your device has been detected as:
        <span class="font-bold text-green-500">{{ platform }}</span>
      </p>
      <p class="text-sm text-gray-400 mt-2">
        The device type has been saved to local storage and registered with the
        API.
      </p>
    </div>
    <div v-if="error" class="mt-4 text-red-500">
      <span
        >Error detecting device or registering data. Please try again
        later.</span
      >
    </div>
  </div>
</template>

<script>
import axios from "axios";
import logger from "@/utils/logger";

export default {
  data() {
    return {
      user_id: "", // Detected platform/device type as user_id
      isLoading: true, // Loading state
      error: false, // Error state
    };
  },
  created() {
    this.detectDevice();
  },
  methods: {
    async detectDevice() {
      try {
        const userAgent = navigator.userAgent.toLowerCase();
        let user_id = "Unknown Device";

        if (/mobile/i.test(userAgent)) {
          user_id = "Mobile";
        } else if (/tablet/i.test(userAgent)) {
          user_id = "Tablet";
        } else {
          user_id = "Desktop";
        }

        // Save user_id in local storage for use by other components
        localStorage.setItem("user_id", user_id);
        this.user_id = user_id;

        // Register the device with the backend API
        logger.info(`Detected device: ${user_id}`);
        await this.registerUser(user_id);
      } catch (error) {
        logger.error(`Error detecting device or registering user: ${error}`);
        this.error = true;
      } finally {
        this.isLoading = false;
      }
    },

    async registerUser(user_id) {
      try {
        const response = await axios.post(
          "http://localhost:8000/user/register",
          {
            phone_model: user_id, // Use user_id instead of platform
            name: "Guest User",
          },
        );

        logger.info(`User registered successfully: ${response.data.message}`);
      } catch (error) {
        logger.error(
          `Error registering user: ${error.response?.data || error}`,
        );
        this.error = true;
      }
    },
  },
};
</script>

<style scoped>
/* Styling for neumorphism effect */
::v-deep(.bg-gray-800) {
  box-shadow:
    8px 8px 15px rgba(0, 0, 0, 0.2),
    -8px -8px 15px rgba(255, 255, 255, 0.1);
}

/* Spinning animation for SVG elements */
::v-deep(svg) {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
