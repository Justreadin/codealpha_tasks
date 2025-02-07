<template>
  <div
    class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-700 text-white grid grid-rows-[auto,1fr]"
  >
    <!-- App Header with Navigation -->
    <AppHeader />

    <!-- Main Content -->
    <router-view class="p-4 lg:p-6 bg-gray-800 rounded-lg shadow-md w-full" />
  </div>
</template>

<script>
import AppHeader from "./components/AppHeader.vue";

export default {
  components: {
    AppHeader,
  },
};
</script>

<style scoped>
/* Smooth fade animation for child components */
:deep(.fade-enter-active),
:deep(.fade-leave-active) {
  transition: opacity 0.5s ease;
}
:deep(.fade-enter-from),
:deep(.fade-leave-to) {
  opacity: 0;
}

/* Scrollbar Enhancements */
:deep(::-webkit-scrollbar) {
  width: 8px;
}
:deep(::-webkit-scrollbar-thumb) {
  background: linear-gradient(to right, #4fd1c5, #4299e1);
  border-radius: 4px;
}
:deep(::-webkit-scrollbar-thumb:hover) {
  background: linear-gradient(to right, #38b2ac, #3182ce);
}
</style>
