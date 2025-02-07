<template>
  <div>
    <DeviceSpecific />
    <TrendingSongs />
    <Visual3D />
  </div>
</template>

<script>
import DeviceSpecific from "../components/DeviceSpecific.vue";
import TrendingSongs from "../components/TrendingSongs.vue";
import Visual3D from "../components/Visual3D.vue";

export default {
  components: {
    DeviceSpecific,
    TrendingSongs,
    Visual3D,
  },
};
</script>
