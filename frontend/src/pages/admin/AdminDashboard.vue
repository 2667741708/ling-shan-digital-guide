<script setup lang="ts">
import { onMounted, ref } from "vue";

import { fetchDashboard } from "../../api/admin";

const data = ref<any>({});

onMounted(async () => {
  data.value = await fetchDashboard();
});

function logout() {
  localStorage.removeItem("admin_token");
  localStorage.removeItem("admin_username");
  window.location.href = "/admin/login";
}
</script>

<template>
  <main class="page admin">
    <nav class="top-nav">
      <strong>管理后台数据大屏</strong>
      <router-link to="/">游客端</router-link>
      <router-link to="/admin/knowledge">知识库</router-link>
      <router-link to="/admin/avatar">数字人配置</router-link>
      <button type="button" @click="logout">退出</button>
    </nav>
    <section class="metric-grid">
      <div class="metric">今日服务人次<strong>{{ data.today_service_count }}</strong></div>
      <div class="metric">平均响应时间<strong>{{ data.avg_latency_ms }}ms</strong></div>
      <div class="metric">满意度<strong>{{ data.satisfaction_score }}</strong></div>
      <div class="metric">知识命中率<strong>{{ Math.round((data.knowledge_hit_rate || 0) * 100) }}%</strong></div>
    </section>
    <section class="dashboard-grid">
      <div class="panel">
        <div class="section-heading">
          <span>热门问答</span>
          <strong>Top {{ data.hot_questions?.length || 0 }}</strong>
        </div>
        <div v-for="item in data.hot_questions" :key="item.topic" class="bar-row">
          <span>{{ item.topic }}</span>
          <div><i :style="{ width: `${Math.min(item.count, 100)}%` }" /></div>
          <strong>{{ item.count }}</strong>
        </div>
      </div>
      <div class="panel">
        <div class="section-heading">
          <span>热门景点</span>
          <strong>灵山胜境</strong>
        </div>
        <div v-for="item in data.hot_spots" :key="item.name" class="rank-row">
          <span>{{ item.name }}</span>
          <strong>{{ item.count }}</strong>
        </div>
      </div>
      <div class="panel">
        <div class="section-heading">
          <span>路线偏好</span>
          <strong>游客画像</strong>
        </div>
        <div class="preference-grid">
          <div v-for="item in data.route_preferences" :key="item.name">
            <strong>{{ item.value }}%</strong>
            <span>{{ item.name }}</span>
          </div>
        </div>
      </div>
      <div class="panel">
        <div class="section-heading">
          <span>情绪趋势</span>
          <strong>近三日</strong>
        </div>
        <div v-for="item in data.emotion_trend" :key="item.date" class="emotion-row">
          <span>{{ item.date }}</span>
          <b class="positive" :style="{ width: `${item.positive}%` }" />
          <b class="neutral" :style="{ width: `${item.neutral}%` }" />
          <b class="negative" :style="{ width: `${item.negative}%` }" />
        </div>
      </div>
    </section>
  </main>
</template>
