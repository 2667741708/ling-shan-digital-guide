<script setup lang="ts">
import { onMounted, ref } from "vue";

import { fetchKnowledgeDocs } from "../../api/admin";

const docs = ref<any[]>([]);

onMounted(async () => {
  docs.value = await fetchKnowledgeDocs() as any[];
});
</script>

<template>
  <main class="page">
    <nav class="top-nav">
      <strong>知识库管理</strong>
      <router-link to="/admin">返回大屏</router-link>
    </nav>
    <section class="panel">
      <h2>文档列表</h2>
      <div v-for="doc in docs" :key="doc.id" class="row">
        <span>{{ doc.title }}</span>
        <span>{{ doc.status }}</span>
        <span>{{ doc.chunk_count }} 个切片</span>
      </div>
    </section>
  </main>
</template>
