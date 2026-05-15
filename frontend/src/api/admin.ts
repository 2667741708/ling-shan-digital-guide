import { http, unwrap } from "./http";

export function fetchDashboard() {
  return unwrap(http.get("/api/admin/analytics/overview"));
}

export function fetchKnowledgeDocs() {
  return unwrap(http.get("/api/admin/knowledge/documents"));
}

export function uploadKnowledgeDocument(file: File, title: string) {
  const form = new FormData();
  form.append("file", file);
  form.append("title", title);
  return unwrap(http.post("/api/admin/knowledge/upload", form));
}

export function updateKnowledgeDocument(documentId: string, payload: { title?: string; content?: string }) {
  return unwrap(http.put(`/api/admin/knowledge/documents/${encodeURIComponent(documentId)}`, payload));
}

export function deleteKnowledgeDocument(documentId: string) {
  return unwrap(http.delete(`/api/admin/knowledge/documents/${encodeURIComponent(documentId)}`));
}

export function reindexKnowledgeBase() {
  return unwrap(http.post("/api/admin/knowledge/reindex"));
}

export function searchKnowledge(query: string) {
  return unwrap(http.post("/api/admin/knowledge/search-test", { query }));
}

export function fetchActiveAvatar() {
  return unwrap(http.get("/api/admin/avatar-configs/active"));
}
