<script setup lang="ts">
import { computed } from "vue";
import { useAvatarStore } from "../../store/avatar";

const avatar = useAvatarStore();
const expression = computed(() => {
  if (avatar.state === "speaking") return "讲解中";
  if (avatar.state === "thinking") return "思考中";
  if (avatar.state === "listening") return "倾听中";
  if (avatar.state === "concerned") return "关切";
  return "微笑待机";
});
</script>

<template>
  <div class="avatar-stage">
    <div class="avatar-body">
      <div class="avatar-face">
        <div class="eye left" />
        <div class="eye right" />
        <div class="mouth" :style="{ height: `${8 + avatar.mouthOpen * 24}px` }" />
      </div>
      <div class="avatar-clothes" />
    </div>
    <div class="avatar-status">{{ expression }}</div>
  </div>
</template>
