<script setup lang="ts">
import { onMounted, ref } from "vue";

import {
  deleteKnowledgeDocument,
  fetchKnowledgeDocs,
  reindexKnowledgeBase,
  searchKnowledge,
  updateKnowledgeDocument,
  uploadKnowledgeDocument
} from "../../api/admin";

type KnowledgeDoc = {
  id: string;
  title: string;
  file_name: string;
  source: string;
  status: string;
  editable: boolean;
  chunk_count: number;
  updated_at: string;
  preview: string;
};

const docs = ref<KnowledgeDoc[]>([]);
const selectedFile = ref<File | null>(null);
const uploadTitle = ref("");
const editorTitle = ref("");
const editorContent = ref("");
const editingId = ref("");
const searchQuery = ref("灵山大佛适合怎么讲解？");
const searchResult = ref<any[]>([]);
const busy = ref(false);
const notice = ref("");

async function loadDocs() {
  docs.value = await fetchKnowledgeDocs() as KnowledgeDoc[];
}

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement;
  selectedFile.value = input.files?.[0] ?? null;
  if (selectedFile.value && !uploadTitle.value) {
    uploadTitle.value = selectedFile.value.name.replace(/\.[^.]+$/, "");
  }
}

async function runWithNotice(action: () => Promise<unknown>, message: string) {
  busy.value = true;
  notice.value = "";
  try {
    await action();
    notice.value = message;
    await loadDocs();
  } catch (error) {
    notice.value = error instanceof Error ? error.message : "操作失败";
  } finally {
    busy.value = false;
  }
}

async function uploadDoc() {
  if (!selectedFile.value) {
    notice.value = "请选择要上传的知识文档";
    return;
  }
  await runWithNotice(
    () => uploadKnowledgeDocument(selectedFile.value as File, uploadTitle.value),
    "上传成功，已自动重建向量索引"
  );
  selectedFile.value = null;
}

async function createTextDoc() {
  if (!editorTitle.value.trim() || !editorContent.value.trim()) {
    notice.value = "请填写资料标题和正文";
    return;
  }
  const file = new File([editorContent.value], `${editorTitle.value.trim()}.md`, { type: "text/markdown" });
  await runWithNotice(() => uploadKnowledgeDocument(file, editorTitle.value), "文本资料已保存并进入知识库");
  editingId.value = "";
}

function editDoc(doc: KnowledgeDoc) {
  editingId.value = doc.id;
  editorTitle.value = doc.title;
  editorContent.value = doc.preview || "";
}

async function updateDoc() {
  if (!editingId.value) {
    await createTextDoc();
    return;
  }
  await runWithNotice(
    () => updateKnowledgeDocument(editingId.value, { title: editorTitle.value, content: editorContent.value }),
    "资料已更新，向量索引已刷新"
  );
}

async function removeDoc(doc: KnowledgeDoc) {
  if (!doc.editable) {
    notice.value = "内置资料不可在页面删除";
    return;
  }
  await runWithNotice(() => deleteKnowledgeDocument(doc.id), "资料已删除，向量索引已刷新");
}

async function rebuild() {
  await runWithNotice(() => reindexKnowledgeBase(), "已重新构建知识库向量索引");
}

async function runSearch() {
  const data = await searchKnowledge(searchQuery.value) as any;
  searchResult.value = data.chunks || [];
}

onMounted(async () => {
  await loadDocs();
  await runSearch();
});
</script>

<template>
  <main class="page">
    <nav class="top-nav">
      <strong>知识库管理</strong>
      <router-link to="/admin">返回大屏</router-link>
      <router-link to="/guide">游客端验证</router-link>
    </nav>

    <section class="knowledge-grid">
      <div class="panel">
        <div class="section-heading">
          <div>
            <strong>上传知识文档</strong>
            <span>支持 Markdown、TXT、CSV、JSON、DOCX、XLSX，上传后自动切片并重建索引。</span>
          </div>
        </div>
        <div class="form-stack">
          <label>
            资料标题
            <input v-model="uploadTitle" placeholder="例如：梵宫讲解词" />
          </label>
          <label>
            选择文件
            <input type="file" accept=".md,.txt,.csv,.json,.docx,.xlsx" @change="onFileChange" />
          </label>
          <button :disabled="busy" @click="uploadDoc">上传并入库</button>
          <p v-if="selectedFile" class="muted">待上传：{{ selectedFile.name }}</p>
        </div>
      </div>

      <div class="panel">
        <div class="section-heading">
          <div>
            <strong>维护文本资料</strong>
            <span>可直接新增或编辑后台上传的讲解词、FAQ、文史资料。</span>
          </div>
        </div>
        <div class="form-stack">
          <label>
            标题
            <input v-model="editorTitle" placeholder="例如：雨天游览 FAQ" />
          </label>
          <label>
            正文
            <textarea v-model="editorContent" rows="9" placeholder="输入讲解词、常见问答或文史资料正文"></textarea>
          </label>
          <div class="actions-line">
            <button :disabled="busy" @click="updateDoc">{{ editingId ? "更新资料" : "新增文本资料" }}</button>
            <button class="secondary" :disabled="busy" @click="editingId = ''; editorTitle = ''; editorContent = ''">清空</button>
          </div>
        </div>
      </div>
    </section>

    <section class="panel">
      <div class="section-heading">
        <div>
          <strong>文档列表</strong>
          <span>内置资料只读，后台上传资料可编辑和删除。</span>
        </div>
        <button :disabled="busy" @click="rebuild">重建索引</button>
      </div>
      <p v-if="notice" class="notice">{{ notice }}</p>
      <div class="knowledge-table">
        <div class="knowledge-row head">
          <span>资料</span>
          <span>状态</span>
          <span>切片</span>
          <span>操作</span>
        </div>
        <div v-for="doc in docs" :key="doc.source" class="knowledge-row">
          <div>
            <strong>{{ doc.title }}</strong>
            <small>{{ doc.source }}</small>
          </div>
          <span>{{ doc.editable ? "可维护" : doc.status }}</span>
          <span>{{ doc.chunk_count }}</span>
          <div class="row-actions">
            <button class="secondary" :disabled="!doc.editable" @click="editDoc(doc)">编辑</button>
            <button class="danger" :disabled="!doc.editable || busy" @click="removeDoc(doc)">删除</button>
          </div>
        </div>
      </div>
    </section>

    <section class="panel">
      <div class="section-heading">
        <div>
          <strong>检索测试</strong>
          <span>验证新增资料是否已经成为数字人回答依据。</span>
        </div>
      </div>
      <div class="search-line">
        <input v-model="searchQuery" placeholder="输入测试问题" @keyup.enter="runSearch" />
        <button @click="runSearch">检索</button>
      </div>
      <ol class="search-results">
        <li v-for="chunk in searchResult" :key="chunk.chunk_id">
          <strong>{{ chunk.title }}</strong>
          <span>{{ chunk.source }} · score {{ chunk.score }}</span>
          <p>{{ chunk.text }}</p>
        </li>
      </ol>
    </section>
  </main>
</template>
