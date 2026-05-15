import { onMounted, ref } from "vue";
import { archiveKnowledgeDocument, deleteKnowledgeDocument, fetchKnowledgeDocs, fetchKnowledgeHistory, fetchKnowledgeVersions, publishKnowledgeDocument, reindexKnowledgeBase, searchKnowledge, updateKnowledgeDocument, uploadKnowledgeDocument } from "../../api/admin";
const docs = ref([]);
const versions = ref([]);
const history = ref([]);
const selectedDoc = ref(null);
const selectedFile = ref(null);
const statusFilter = ref("all");
const uploadTitle = ref("");
const changeNote = ref("后台上传");
const editorTitle = ref("");
const editorContent = ref("");
const editingId = ref("");
const searchQuery = ref("灵山大佛适合怎么讲解？");
const searchResult = ref([]);
const busy = ref(false);
const notice = ref("");
const statusText = {
    all: "全部",
    draft: "草稿",
    active: "已发布",
    archived: "已归档",
    deleted: "已删除"
};
async function loadDocs() {
    docs.value = await fetchKnowledgeDocs(statusFilter.value);
}
function onFileChange(event) {
    const input = event.target;
    selectedFile.value = input.files?.[0] ?? null;
    if (selectedFile.value && !uploadTitle.value) {
        uploadTitle.value = selectedFile.value.name.replace(/\.[^.]+$/, "");
    }
}
async function runWithNotice(action, message) {
    busy.value = true;
    notice.value = "";
    try {
        await action();
        notice.value = message;
        await loadDocs();
        if (selectedDoc.value)
            await inspectDoc(selectedDoc.value.id);
    }
    catch (error) {
        notice.value = error instanceof Error ? error.message : "操作失败";
    }
    finally {
        busy.value = false;
    }
}
async function uploadDoc() {
    if (!selectedFile.value) {
        notice.value = "请选择要上传的知识文档";
        return;
    }
    await runWithNotice(() => uploadKnowledgeDocument(selectedFile.value, uploadTitle.value, changeNote.value), "上传成功，当前为草稿；发布后才会进入游客端 RAG");
    selectedFile.value = null;
}
async function createTextDoc() {
    if (!editorTitle.value.trim() || !editorContent.value.trim()) {
        notice.value = "请填写资料标题和正文";
        return;
    }
    const file = new File([editorContent.value], `${editorTitle.value.trim()}.md`, { type: "text/markdown" });
    await runWithNotice(() => uploadKnowledgeDocument(file, editorTitle.value, changeNote.value), "文本资料已保存为草稿");
    editingId.value = "";
}
function editDoc(doc) {
    editingId.value = doc.id;
    editorTitle.value = doc.title;
    editorContent.value = doc.preview || "";
    selectedDoc.value = doc;
}
async function updateDoc() {
    if (!editingId.value) {
        await createTextDoc();
        return;
    }
    await runWithNotice(() => updateKnowledgeDocument(editingId.value, { title: editorTitle.value, content: editorContent.value, change_note: changeNote.value }), "资料已生成新草稿版本；发布后才会进入游客端 RAG");
}
async function changeStatus(doc, action) {
    const messages = {
        publish: "资料已发布，已重建向量索引",
        archive: "资料已归档，已从游客端 RAG 中移除",
        delete: "资料已软删除，历史仍保留"
    };
    const actions = {
        publish: () => publishKnowledgeDocument(doc.id),
        archive: () => archiveKnowledgeDocument(doc.id),
        delete: () => deleteKnowledgeDocument(doc.id)
    };
    await runWithNotice(actions[action], messages[action]);
}
async function rebuild() {
    await runWithNotice(() => reindexKnowledgeBase(), "已重新构建知识库向量索引");
}
async function runSearch() {
    const data = await searchKnowledge(searchQuery.value);
    searchResult.value = data.chunks || [];
}
async function inspectDoc(documentId) {
    const doc = docs.value.find((item) => item.id === documentId);
    if (doc)
        selectedDoc.value = doc;
    versions.value = await fetchKnowledgeVersions(documentId);
    history.value = await fetchKnowledgeHistory(documentId);
}
function logout() {
    localStorage.removeItem("admin_token");
    localStorage.removeItem("admin_username");
    window.location.href = "/admin/login";
}
onMounted(async () => {
    await loadDocs();
    await runSearch();
});
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.main, __VLS_intrinsicElements.main)({
    ...{ class: "page" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.nav, __VLS_intrinsicElements.nav)({
    ...{ class: "top-nav" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
const __VLS_0 = {}.RouterLink;
/** @type {[typeof __VLS_components.RouterLink, typeof __VLS_components.routerLink, typeof __VLS_components.RouterLink, typeof __VLS_components.routerLink, ]} */ ;
// @ts-ignore
const __VLS_1 = __VLS_asFunctionalComponent(__VLS_0, new __VLS_0({
    to: "/admin",
}));
const __VLS_2 = __VLS_1({
    to: "/admin",
}, ...__VLS_functionalComponentArgsRest(__VLS_1));
__VLS_3.slots.default;
var __VLS_3;
const __VLS_4 = {}.RouterLink;
/** @type {[typeof __VLS_components.RouterLink, typeof __VLS_components.routerLink, typeof __VLS_components.RouterLink, typeof __VLS_components.routerLink, ]} */ ;
// @ts-ignore
const __VLS_5 = __VLS_asFunctionalComponent(__VLS_4, new __VLS_4({
    to: "/guide",
}));
const __VLS_6 = __VLS_5({
    to: "/guide",
}, ...__VLS_functionalComponentArgsRest(__VLS_5));
__VLS_7.slots.default;
var __VLS_7;
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (__VLS_ctx.logout) },
    ...{ class: "secondary" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "knowledge-grid" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "panel" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "section-heading" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "form-stack" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    placeholder: "例如：梵宫讲解词",
});
(__VLS_ctx.uploadTitle);
__VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    placeholder: "例如：补充雨天讲解词",
});
(__VLS_ctx.changeNote);
__VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    ...{ onChange: (__VLS_ctx.onFileChange) },
    type: "file",
    accept: ".md,.txt,.csv,.json,.docx,.xlsx",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (__VLS_ctx.uploadDoc) },
    disabled: (__VLS_ctx.busy),
});
if (__VLS_ctx.selectedFile) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "muted" },
    });
    (__VLS_ctx.selectedFile.name);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "panel" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "section-heading" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "form-stack" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    placeholder: "例如：雨天游览 FAQ",
});
(__VLS_ctx.editorTitle);
__VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.textarea, __VLS_intrinsicElements.textarea)({
    value: (__VLS_ctx.editorContent),
    rows: "9",
    placeholder: "输入讲解词、常见问答或文史资料正文",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "actions-line" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (__VLS_ctx.updateDoc) },
    disabled: (__VLS_ctx.busy),
});
(__VLS_ctx.editingId ? "生成新版本" : "新增文本草稿");
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (...[$event]) => {
            __VLS_ctx.editingId = '';
            __VLS_ctx.editorTitle = '';
            __VLS_ctx.editorContent = '';
        } },
    ...{ class: "secondary" },
    disabled: (__VLS_ctx.busy),
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "panel" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "section-heading" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "actions-line" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.select, __VLS_intrinsicElements.select)({
    ...{ onChange: (__VLS_ctx.loadDocs) },
    value: (__VLS_ctx.statusFilter),
});
for (const [label, key] of __VLS_getVForSourceType((__VLS_ctx.statusText))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
        key: (key),
        value: (key),
    });
    (label);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (__VLS_ctx.rebuild) },
    disabled: (__VLS_ctx.busy),
});
if (__VLS_ctx.notice) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "notice" },
    });
    (__VLS_ctx.notice);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "knowledge-table" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "knowledge-row head" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
for (const [doc] of __VLS_getVForSourceType((__VLS_ctx.docs))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        key: (doc.id),
        ...{ class: "knowledge-row" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
    (doc.title);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
    (doc.source);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    (__VLS_ctx.statusText[doc.status] || doc.status);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    (doc.current_version);
    (doc.version_count);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "row-actions" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (...[$event]) => {
                __VLS_ctx.inspectDoc(doc.id);
            } },
        ...{ class: "secondary" },
        disabled: (doc.status === 'deleted'),
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (...[$event]) => {
                __VLS_ctx.editDoc(doc);
            } },
        ...{ class: "secondary" },
        disabled: (doc.status === 'deleted' || !doc.preview),
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (...[$event]) => {
                __VLS_ctx.changeStatus(doc, 'publish');
            } },
        disabled: (doc.status === 'active' || doc.status === 'deleted' || __VLS_ctx.busy),
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (...[$event]) => {
                __VLS_ctx.changeStatus(doc, 'archive');
            } },
        ...{ class: "secondary" },
        disabled: (doc.status !== 'active' || __VLS_ctx.busy),
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (...[$event]) => {
                __VLS_ctx.changeStatus(doc, 'delete');
            } },
        ...{ class: "danger" },
        disabled: (doc.status === 'deleted' || __VLS_ctx.busy),
    });
}
if (__VLS_ctx.selectedDoc) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
        ...{ class: "knowledge-grid" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "panel" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
    (__VLS_ctx.selectedDoc.title);
    for (const [version] of __VLS_getVForSourceType((__VLS_ctx.versions))) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            key: (version.id),
            ...{ class: "history-row" },
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
        (version.version);
        (version.is_current ? "当前" : "");
        __VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
        (version.created_by);
        (version.created_at);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
        (version.change_note);
    }
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "panel" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
    for (const [item] of __VLS_getVForSourceType((__VLS_ctx.history))) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            key: (item.id),
            ...{ class: "history-row" },
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
        (item.action);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
        (item.actor);
        (item.created_at);
    }
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "panel" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "section-heading" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "search-line" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    ...{ onKeyup: (__VLS_ctx.runSearch) },
    placeholder: "输入测试问题",
});
(__VLS_ctx.searchQuery);
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (__VLS_ctx.runSearch) },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.ol, __VLS_intrinsicElements.ol)({
    ...{ class: "search-results" },
});
for (const [chunk] of __VLS_getVForSourceType((__VLS_ctx.searchResult))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.li, __VLS_intrinsicElements.li)({
        key: (chunk.chunk_id),
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
    (chunk.title);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    (chunk.source);
    (chunk.score);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
    (chunk.text);
}
/** @type {__VLS_StyleScopedClasses['page']} */ ;
/** @type {__VLS_StyleScopedClasses['top-nav']} */ ;
/** @type {__VLS_StyleScopedClasses['secondary']} */ ;
/** @type {__VLS_StyleScopedClasses['knowledge-grid']} */ ;
/** @type {__VLS_StyleScopedClasses['panel']} */ ;
/** @type {__VLS_StyleScopedClasses['section-heading']} */ ;
/** @type {__VLS_StyleScopedClasses['form-stack']} */ ;
/** @type {__VLS_StyleScopedClasses['muted']} */ ;
/** @type {__VLS_StyleScopedClasses['panel']} */ ;
/** @type {__VLS_StyleScopedClasses['section-heading']} */ ;
/** @type {__VLS_StyleScopedClasses['form-stack']} */ ;
/** @type {__VLS_StyleScopedClasses['actions-line']} */ ;
/** @type {__VLS_StyleScopedClasses['secondary']} */ ;
/** @type {__VLS_StyleScopedClasses['panel']} */ ;
/** @type {__VLS_StyleScopedClasses['section-heading']} */ ;
/** @type {__VLS_StyleScopedClasses['actions-line']} */ ;
/** @type {__VLS_StyleScopedClasses['notice']} */ ;
/** @type {__VLS_StyleScopedClasses['knowledge-table']} */ ;
/** @type {__VLS_StyleScopedClasses['knowledge-row']} */ ;
/** @type {__VLS_StyleScopedClasses['head']} */ ;
/** @type {__VLS_StyleScopedClasses['knowledge-row']} */ ;
/** @type {__VLS_StyleScopedClasses['row-actions']} */ ;
/** @type {__VLS_StyleScopedClasses['secondary']} */ ;
/** @type {__VLS_StyleScopedClasses['secondary']} */ ;
/** @type {__VLS_StyleScopedClasses['secondary']} */ ;
/** @type {__VLS_StyleScopedClasses['danger']} */ ;
/** @type {__VLS_StyleScopedClasses['knowledge-grid']} */ ;
/** @type {__VLS_StyleScopedClasses['panel']} */ ;
/** @type {__VLS_StyleScopedClasses['history-row']} */ ;
/** @type {__VLS_StyleScopedClasses['panel']} */ ;
/** @type {__VLS_StyleScopedClasses['history-row']} */ ;
/** @type {__VLS_StyleScopedClasses['panel']} */ ;
/** @type {__VLS_StyleScopedClasses['section-heading']} */ ;
/** @type {__VLS_StyleScopedClasses['search-line']} */ ;
/** @type {__VLS_StyleScopedClasses['search-results']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            docs: docs,
            versions: versions,
            history: history,
            selectedDoc: selectedDoc,
            selectedFile: selectedFile,
            statusFilter: statusFilter,
            uploadTitle: uploadTitle,
            changeNote: changeNote,
            editorTitle: editorTitle,
            editorContent: editorContent,
            editingId: editingId,
            searchQuery: searchQuery,
            searchResult: searchResult,
            busy: busy,
            notice: notice,
            statusText: statusText,
            loadDocs: loadDocs,
            onFileChange: onFileChange,
            uploadDoc: uploadDoc,
            editDoc: editDoc,
            updateDoc: updateDoc,
            changeStatus: changeStatus,
            rebuild: rebuild,
            runSearch: runSearch,
            inspectDoc: inspectDoc,
            logout: logout,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
//# sourceMappingURL=KnowledgeManage.vue.js.map