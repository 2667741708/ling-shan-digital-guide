<script setup lang="ts">
import { onMounted, ref } from "vue";

import { fetchDashboard } from "../../api/admin";

const data = ref<any>({});

onMounted(async () => {
  data.value = await fetchDashboard();
});
</script>

<template>
  <main class="page admin">
    <nav class="top-nav">
      <strong>管理后台数据大屏</strong>
      <router-link to="/">游客端</router-link>
      <router-link to="/admin/knowledge">知识库</router-link>
      <router-link to="/admin/avatar">数字人配置</router-link>
    </nav>
    <section class="metric-grid">
      <div class="metric">今日服务人次<strong>{{ data.today_service_count }}</strong></div>
      <div class="metric">平均响应时间<strong>{{ data.avg_latency_ms }}ms</strong></div>
      <div class="metric">满意度<strong>{{ data.satisfaction_score }}</strong></div>
      <div class="metric">知识命中率<strong>{{ Math.round((data.knowledge_hit_rate || 0) * 100) }}%</strong></div>
    </section>
    <section class="panel">
      <h2>热门问答</h2>
      <p v-for="item in data.hot_questions" :key="item.topic">{{ item.topic }}：{{ item.count }}</p>
    </section>
  </main>
</template>
