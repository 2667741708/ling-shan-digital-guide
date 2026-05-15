import { http, unwrap } from "./http";
export function fetchDashboard() {
    return unwrap(http.get("/api/admin/analytics/overview"));
}
export function loginAdmin(username, password) {
    return unwrap(http.post("/api/admin/login", { username, password }));
}
export function fetchAdminMe() {
    return unwrap(http.get("/api/admin/me"));
}
export function fetchKnowledgeDocs(status = "all") {
    return unwrap(http.get("/api/admin/knowledge/documents", { params: { status } }));
}
export function uploadKnowledgeDocument(file, title, changeNote = "initial upload") {
    const form = new FormData();
    form.append("file", file);
    form.append("title", title);
    form.append("change_note", changeNote);
    return unwrap(http.post("/api/admin/knowledge/upload", form));
}
export function updateKnowledgeDocument(documentId, payload) {
    return unwrap(http.put(`/api/admin/knowledge/documents/${encodeURIComponent(documentId)}`, payload));
}
export function publishKnowledgeDocument(documentId) {
    return unwrap(http.post(`/api/admin/knowledge/documents/${encodeURIComponent(documentId)}/publish`));
}
export function archiveKnowledgeDocument(documentId) {
    return unwrap(http.post(`/api/admin/knowledge/documents/${encodeURIComponent(documentId)}/archive`));
}
export function deleteKnowledgeDocument(documentId) {
    return unwrap(http.delete(`/api/admin/knowledge/documents/${encodeURIComponent(documentId)}`));
}
export function fetchKnowledgeVersions(documentId) {
    return unwrap(http.get(`/api/admin/knowledge/documents/${encodeURIComponent(documentId)}/versions`));
}
export function fetchKnowledgeHistory(documentId) {
    return unwrap(http.get(`/api/admin/knowledge/documents/${encodeURIComponent(documentId)}/history`));
}
export function reindexKnowledgeBase() {
    return unwrap(http.post("/api/admin/knowledge/reindex"));
}
export function searchKnowledge(query) {
    return unwrap(http.post("/api/admin/knowledge/search-test", { query }));
}
export function fetchActiveAvatar() {
    return unwrap(http.get("/api/admin/avatar-configs/active"));
}
export function saveAvatarConfig(payload) {
    return unwrap(http.post("/api/admin/avatar-configs", payload));
}
//# sourceMappingURL=admin.js.map