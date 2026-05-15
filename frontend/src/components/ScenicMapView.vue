<script setup lang="ts">
defineProps<{ spots: Array<{ id: number; name: string; map_x: number; map_y: number }> }>();
</script>

<template>
  <section class="panel scenic-map">
    <div v-for="spot in spots" :key="spot.id" class="poi" :style="{ left: `${spot.map_x}%`, top: `${spot.map_y}%` }">
      <span>{{ spot.name }}</span>
    </div>
  </section>
</template>
