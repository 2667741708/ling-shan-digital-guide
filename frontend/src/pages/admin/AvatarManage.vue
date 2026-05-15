<script setup lang="ts">
import { onMounted, ref } from "vue";

import { fetchActiveAvatar } from "../../api/admin";

const avatar = ref<any>({});

onMounted(async () => {
  avatar.value = await fetchActiveAvatar();
});
</script>

<template>
  <main class="page">
    <nav class="top-nav">
      <strong>数字人形象管理</strong>
      <router-link to="/admin">返回大屏</router-link>
    </nav>
    <section class="panel form-preview">
      <label>名称 <input v-model="avatar.name" /></label>
      <label>风格 <input v-model="avatar.avatar_style" /></label>
      <label>音色 <input v-model="avatar.voice_name" /></label>
      <label>欢迎语 <textarea v-model="avatar.opening_text" /></label>
    </section>
  </main>
</template>
