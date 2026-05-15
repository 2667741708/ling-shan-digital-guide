import { http, unwrap } from "./http";

export function fetchDashboard() {
  return unwrap(http.get("/api/admin/analytics/overview"));
}

export function fetchKnowledgeDocs() {
  return unwrap(http.get("/api/admin/knowledge/documents"));
}

export function fetchActiveAvatar() {
  return unwrap(http.get("/api/admin/avatar-configs/active"));
}
