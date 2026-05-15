import { http, unwrap } from "./http";

export interface ScenicSpot {
  id: number;
  name: string;
  description: string;
  guide_text?: string;
  map_x: number;
  map_y: number;
  tags?: string[];
  recommended_duration?: number;
}

export interface RouteSpot {
  id: number;
  name: string;
  stay_minutes: number;
  reason?: string;
}

export interface RoutePlan {
  route_name: string;
  total_duration: number;
  spots: RouteSpot[];
  reason: string;
}

export function createSession() {
  return unwrap(http.post("/api/visitor/sessions", {
    device_type: "web",
    user_profile: { interest: ["history", "photo"], available_time: 120, physical_strength: "normal" },
    start_location: { type: "manual", spot_id: 1 }
  }));
}

export function sendText(sessionUuid: string, message: string) {
  return unwrap(http.post("/api/visitor/chat/text", { session_uuid: sessionUuid, message }));
}

export function fetchScenicSpots(): Promise<ScenicSpot[]> {
  return unwrap(http.get("/api/visitor/scenic-spots"));
}

export function recommendRoute(sessionUuid: string, overrides: Partial<{ interest: string[]; available_time: number; physical_strength: string; start_spot_id: number }> = {}): Promise<RoutePlan> {
  return unwrap(http.post("/api/visitor/routes/recommend", {
    session_uuid: sessionUuid,
    interest: ["history", "photo"],
    available_time: 120,
    physical_strength: "normal",
    start_spot_id: 1,
    ...overrides
  }));
}
