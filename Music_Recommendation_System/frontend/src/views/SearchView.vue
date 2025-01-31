<template>
  <div>
    <h1 class="text-2xl font-bold mb-4 text-red-500">Search</h1>
    <SearchBar />
  </div>
</template>

<script>
import SearchBar from "../components/SearchBar.vue";

export default {
  components: {
    SearchBar,
  },
};
</script>
