<template>
  <div
    class="min-h-screen bg-gray-900 text-white p-6 flex flex-col items-center"
  >
    <!-- Chat Section -->
    <div class="w-full max-w-2xl">
      <UserChat />
    </div>
  </div>
</template>

<script>
import UserChat from "../components/UserChat.vue";

export default {
  components: {
    UserChat,
  },
};
</script>

<style scoped>
/* Custom styles for gradient text */
.text-gradient {
  background: linear-gradient(to right, #667eea, #9f7aea, #ed64a6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
