<script setup lang="ts">
import { onMounted, ref } from "vue";

import { fetchScenicSpots } from "../../api/visitor";
import ScenicMapView from "../../components/ScenicMapView.vue";

const spots = ref([]);

onMounted(async () => {
  spots.value = await fetchScenicSpots() as never[];
});
</script>

<template>
  <main class="page">
    <nav class="top-nav">
      <strong>景区地图导览</strong>
      <router-link to="/guide">返回数字人</router-link>
    </nav>
    <ScenicMapView :spots="spots" />
  </main>
</template>
