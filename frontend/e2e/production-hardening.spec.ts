import { expect, request, test } from "@playwright/test";

const apiBaseURL = process.env.E2E_API_BASE_URL || "http://127.0.0.1:8000";

test("admin knowledge, visitor answer, rating review and account permissions", async ({ page }) => {
  const api = await request.newContext({ baseURL: apiBaseURL });

  const login = await api.post("/api/v1/auth/login", {
    data: { username: "admin", password: "123456" }
  });
  expect(login.ok()).toBeTruthy();
  const token = (await login.json()).data.token as string;
  const headers = { Authorization: `Bearer ${token}` };

  const userResponse = await api.post("/api/v1/admin/users", {
    headers,
    data: {
      username: `e2e_viewer_${Date.now()}`,
      password: "viewer-pass-123",
      role: "viewer"
    }
  });
  expect([200, 400]).toContain(userResponse.status());

  const upload = await api.post("/api/v1/admin/knowledge-bases/default/documents", {
    headers,
    multipart: {
      title: "E2E 雨天路线",
      change_note: "playwright e2e",
      file: {
        name: "e2e-rain-guide.md",
        mimeType: "text/markdown",
        buffer: Buffer.from("E2E 雨天路线建议：先参观梵宫，再到游客中心休息。", "utf-8")
      }
    }
  });
  expect(upload.ok()).toBeTruthy();
  const documentId = (await upload.json()).data.id as string;

  const publish = await api.post(`/api/v1/admin/documents/${documentId}/publish`, { headers });
  expect(publish.ok()).toBeTruthy();

  const retrieve = await api.post("/api/v1/rag/retrieve", {
    data: { query: "雨天路线怎么安排", top_k: 3 }
  });
  expect(retrieve.ok()).toBeTruthy();
  expect((await retrieve.json()).data.chunks.length).toBeGreaterThan(0);

  const guideAsk = await api.post("/api/v1/guide/ask", {
    data: {
      question: "雨天路线怎么安排？",
      scene_code: "main_gate",
      user_profile: { group_type: "family" }
    }
  });
  expect(guideAsk.ok()).toBeTruthy();
  expect((await guideAsk.json()).data.text).toBeTruthy();

  const rating = await api.post("/api/v1/visitor/ratings", {
    data: {
      session_uuid: "playwright_e2e_session",
      spot_id: 6,
      overall_rating: 4,
      comment: "E2E 审核评论",
      is_public: true
    }
  });
  expect(rating.ok()).toBeTruthy();
  const ratingId = (await rating.json()).data.id as string;

  const review = await api.put(`/api/v1/admin/ratings/${ratingId}/review`, {
    headers,
    data: { review_status: "hidden", is_public: false }
  });
  expect(review.ok()).toBeTruthy();

  await page.goto("/admin/login");
  await expect(page.getByText("管理后台登录")).toBeVisible();
  await page.goto("/guide");
  await expect(page.locator("body")).toContainText("灵");
});
