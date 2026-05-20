<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";

import { createAdminUser, fetchAdminUsers, resetAdminUserPassword, updateAdminUserStatus } from "../../api/admin";

type AdminUser = {
  id: string;
  username: string;
  role: string;
  permissions: string[];
  enabled: boolean;
  last_login_at: string | null;
  created_at: string;
};

const users = ref<AdminUser[]>([]);
const notice = ref("");
const busy = ref(false);
const form = reactive({
  username: "",
  password: "",
  role: "viewer"
});
const resetPasswords = reactive<Record<string, string>>({});

const roleLabels: Record<string, string> = {
  super_admin: "超级管理员",
  knowledge_manager: "知识库管理员",
  operator: "运营审核员",
  viewer: "只读观察员"
};

async function loadUsers() {
  users.value = (await fetchAdminUsers()) as AdminUser[];
}

async function runAction(action: () => Promise<unknown>, message: string) {
  busy.value = true;
  notice.value = "";
  try {
    await action();
    notice.value = message;
    await loadUsers();
  } catch (error: any) {
    notice.value = error?.response?.data?.detail || error?.message || "操作失败";
  } finally {
    busy.value = false;
  }
}

async function submitCreate() {
  if (!form.username.trim() || !form.password.trim()) {
    notice.value = "请填写账号和密码";
    return;
  }
  await runAction(
    () => createAdminUser({ username: form.username.trim(), password: form.password, role: form.role }),
    "管理员账号已创建"
  );
  form.username = "";
  form.password = "";
  form.role = "viewer";
}

async function toggleUser(user: AdminUser) {
  await runAction(() => updateAdminUserStatus(user.id, !user.enabled), user.enabled ? "账号已禁用" : "账号已启用");
}

async function resetPassword(user: AdminUser) {
  const nextPassword = resetPasswords[user.id] || "";
  if (nextPassword.length < 8) {
    notice.value = "新密码至少 8 位";
    return;
  }
  await runAction(() => resetAdminUserPassword(user.id, nextPassword), "密码已重置");
  resetPasswords[user.id] = "";
}

function logout() {
  localStorage.removeItem("admin_token");
  localStorage.removeItem("admin_username");
  window.location.href = "/admin/login";
}

onMounted(loadUsers);
</script>

<template>
  <main class="page admin">
    <nav class="top-nav">
      <strong>管理员账号</strong>
      <router-link to="/admin">数据大屏</router-link>
      <router-link to="/admin/ratings">评分运营</router-link>
      <router-link to="/admin/knowledge">知识库</router-link>
      <button type="button" @click="logout">退出</button>
    </nav>

    <section class="knowledge-grid">
      <div class="panel">
        <div class="section-heading">
          <div>
            <strong>新增账号</strong>
            <span>只有超级管理员可管理后台账号。</span>
          </div>
        </div>
        <div class="form-stack">
          <label>账号 <input v-model="form.username" autocomplete="off" placeholder="例如 knowledge_editor" /></label>
          <label>初始密码 <input v-model="form.password" type="password" autocomplete="new-password" /></label>
          <label>
            角色
            <select v-model="form.role">
              <option value="viewer">只读观察员</option>
              <option value="operator">运营审核员</option>
              <option value="knowledge_manager">知识库管理员</option>
              <option value="super_admin">超级管理员</option>
            </select>
          </label>
          <button type="button" :disabled="busy" @click="submitCreate">创建账号</button>
          <p v-if="notice" class="notice">{{ notice }}</p>
        </div>
      </div>

      <div class="panel">
        <div class="section-heading">
          <div>
            <strong>角色权限</strong>
            <span>写操作按最小权限开放。</span>
          </div>
        </div>
        <div class="role-list">
          <div v-for="(label, key) in roleLabels" :key="key" class="history-row">
            <strong>{{ label }}</strong>
            <small>{{ key }}</small>
          </div>
        </div>
      </div>
    </section>

    <section class="panel">
      <div class="section-heading">
        <div>
          <strong>账号列表</strong>
          <span>{{ users.length }} 个后台账号</span>
        </div>
      </div>
      <div class="knowledge-table">
        <div class="knowledge-row head">
          <span>账号</span>
          <span>角色</span>
          <span>状态</span>
          <span>操作</span>
        </div>
        <div v-for="user in users" :key="user.id" class="knowledge-row">
          <div>
            <strong>{{ user.username }}</strong>
            <small>创建于 {{ user.created_at }} · 最近登录 {{ user.last_login_at || "暂无" }}</small>
          </div>
          <span>{{ roleLabels[user.role] || user.role }}</span>
          <span>{{ user.enabled ? "启用" : "禁用" }}</span>
          <div class="row-actions">
            <button type="button" class="secondary" :disabled="busy" @click="toggleUser(user)">
              {{ user.enabled ? "禁用" : "启用" }}
            </button>
            <input v-model="resetPasswords[user.id]" type="password" autocomplete="new-password" placeholder="新密码" />
            <button type="button" :disabled="busy" @click="resetPassword(user)">重置密码</button>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>
