import { http, unwrap } from "./http";
export function createSession() {
    return unwrap(http.post("/api/visitor/sessions", {
        device_type: "web",
        user_profile: { interest: ["history", "photo"], available_time: 120, physical_strength: "normal" },
        start_location: { type: "manual", spot_id: 1 }
    }));
}
export function sendText(sessionUuid, message) {
    return unwrap(http.post("/api/visitor/chat/text", { session_uuid: sessionUuid, message }));
}
export function fetchScenicSpots() {
    return unwrap(http.get("/api/visitor/scenic-spots"));
}
export function recommendRoute(sessionUuid, overrides = {}) {
    return unwrap(http.post("/api/visitor/routes/recommend", {
        session_uuid: sessionUuid,
        interest: ["history", "photo"],
        available_time: 120,
        physical_strength: "normal",
        start_spot_id: 1,
        ...overrides
    }));
}
//# sourceMappingURL=visitor.js.map