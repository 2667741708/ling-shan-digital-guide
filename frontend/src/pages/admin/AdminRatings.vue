<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";

import { fetchAdminRatings, fetchRatingReport, reviewRating } from "../../api/admin";

const filters = reactive({
  spot_id: "",
  sentiment: "",
  review_status: "",
  start_date: "",
  end_date: "",
  keyword: ""
});
const ratings = ref<any[]>([]);
const report = ref<any>({});
const loading = ref(false);

async function loadRatings() {
  loading.value = true;
  const params: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(filters)) {
    if (value !== "") {
      params[key] = value;
    }
  }
  ratings.value = (await fetchAdminRatings(params)) as any[];
  report.value = (await fetchRatingReport({
    start_date: filters.start_date || undefined,
    end_date: filters.end_date || undefined
  })) as Record<string, any>;
  loading.value = false;
}

async function handleReview(ratingId: string, reviewStatus: string, isPublic?: boolean) {
  await reviewRating(ratingId, { review_status: reviewStatus, is_public: isPublic });
  await loadRatings();
}

function logout() {
  localStorage.removeItem("admin_token");
  localStorage.removeItem("admin_username");
  window.location.href = "/admin/login";
}

onMounted(loadRatings);
</script>

<template>
  <main class="page admin">
    <nav class="top-nav">
      <strong>评分运营</strong>
      <router-link to="/admin">数据大屏</router-link>
      <router-link to="/admin/knowledge">知识库</router-link>
      <router-link to="/admin/avatar">数字人配置</router-link>
      <button type="button" @click="logout">退出</button>
    </nav>

    <section class="panel admin-filter-panel">
      <div>
        <label>景点 ID</label>
        <input v-model="filters.spot_id" placeholder="例如 6" />
      </div>
      <div>
        <label>情绪</label>
        <select v-model="filters.sentiment">
          <option value="">全部</option>
          <option value="positive">正向</option>
          <option value="neutral">中性</option>
          <option value="negative">负向</option>
        </select>
      </div>
      <div>
        <label>审核状态</label>
        <select v-model="filters.review_status">
          <option value="">全部</option>
          <option value="pending">待审核</option>
          <option value="approved">已通过</option>
          <option value="rejected">已拒绝</option>
          <option value="hidden">已隐藏</option>
        </select>
      </div>
      <div>
        <label>开始日期</label>
        <input v-model="filters.start_date" type="date" />
      </div>
      <div>
        <label>结束日期</label>
        <input v-model="filters.end_date" type="date" />
      </div>
      <div>
        <label>关键词</label>
        <input v-model="filters.keyword" placeholder="排队 / 拍照 / 服务" />
      </div>
      <button type="button" :disabled="loading" @click="loadRatings">{{ loading ? "加载中..." : "筛选" }}</button>
    </section>

    <section class="metric-grid">
      <div class="metric">评分总数<strong>{{ report.summary?.total_ratings || 0 }}</strong></div>
      <div class="metric">平均满意度<strong>{{ report.summary?.average_overall || "暂无" }}</strong></div>
      <div class="metric">负向评论<strong>{{ report.summary?.negative_count || 0 }}</strong></div>
      <div class="metric">公开评论<strong>{{ report.summary?.public_comment_count || 0 }}</strong></div>
      <div class="metric">拍照均分<strong>{{ report.dimension_averages?.photo || "暂无" }}</strong></div>
      <div class="metric">设施均分<strong>{{ report.dimension_averages?.facility || "暂无" }}</strong></div>
    </section>

    <section class="dashboard-grid">
      <div class="panel wide-panel">
        <div class="section-heading">
          <span>游客感受度报告</span>
          <strong>服务建议</strong>
        </div>
        <p v-if="!report.service_suggestions?.length">暂无建议。</p>
        <div v-for="item in report.service_suggestions" :key="item" class="insight-row">{{ item }}</div>
      </div>

      <div class="panel">
        <div class="section-heading">
          <span>拍照价值景点</span>
          <strong>Top</strong>
        </div>
        <div v-for="item in report.photo_value_spots" :key="item.spot_id" class="rank-row">
          <span>{{ item.spot_name }}</span>
          <small>拍照 {{ item.average_photo }} · {{ item.total_ratings }} 条</small>
          <strong>{{ item.average_photo }}</strong>
        </div>
      </div>

      <div class="panel">
        <div class="section-heading">
          <span>设施风险景点</span>
          <strong>Low</strong>
        </div>
        <div v-for="item in report.facility_risk_spots" :key="item.spot_id" class="rank-row">
          <span>{{ item.spot_name }}</span>
          <small>设施 {{ item.average_facility }} · {{ item.total_ratings }} 条</small>
          <strong>{{ item.average_facility || "-" }}</strong>
        </div>
      </div>

      <div class="panel wide-panel">
        <div class="section-heading">
          <span>评论审核</span>
          <strong>{{ ratings.length }} 条</strong>
        </div>
        <p v-if="!ratings.length">暂无评分记录。</p>
        <article v-for="item in ratings" :key="item.id" class="rating-audit-card">
          <header>
            <strong>{{ item.spot_name || `景点 ${item.spot_id}` }}</strong>
            <span>{{ item.overall_rating }} 分 · {{ item.sentiment }} · {{ item.review_status }}</span>
          </header>
          <p>{{ item.comment || "无文字评论" }}</p>
          <div class="tag-cloud">
            <span v-for="tag in item.user_tags" :key="tag">{{ tag }}</span>
          </div>
          <footer>
            <small>{{ item.source }} · {{ item.created_at }}</small>
            <div>
              <button type="button" @click="handleReview(item.id, 'approved', true)">通过公开</button>
              <button type="button" @click="handleReview(item.id, 'hidden', false)">隐藏</button>
              <button type="button" @click="handleReview(item.id, 'rejected', false)">拒绝</button>
            </div>
          </footer>
        </article>
      </div>
    </section>
  </main>
</template>
