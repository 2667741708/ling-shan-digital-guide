import type { AvatarState } from "./avatar";
import type { Viseme } from "./avatarLipSync";

export const REALISTIC_AVATAR_MODEL_URL = "/avatar/models/lingling-realistic.glb";

export type AvatarRenderMode = "realistic-3d" | "local-2d";

export const VRM_EXPRESSION_BY_VISEME: Record<Viseme, string[]> = {
  closed: [],
  mbp: ["m", "mouthClose", "neutral"],
  aa: ["aa", "a", "mouthOpen"],
  ee: ["ee", "ih", "i"],
  oh: ["oh", "o"],
  round: ["ou", "u", "oh"],
  fv: ["aa", "mouthOpen"],
  smile: ["happy", "relaxed", "smile"],
};

export const MORPH_TARGET_BY_VISEME: Record<Viseme, string[]> = {
  closed: ["mouthclose", "mouth_close", "viseme_sil", "sil", "neutral"],
  mbp: ["viseme_mbp", "mouth_mbp", "mbp", "m", "b", "p", "mouthclose"],
  aa: ["viseme_aa", "mouth_aa", "aa", "a", "jawopen", "mouthopen"],
  ee: ["viseme_ee", "mouth_ee", "ee", "ih", "i", "mouthwide"],
  oh: ["viseme_oh", "mouth_oh", "oh", "o"],
  round: ["viseme_round", "viseme_ou", "mouth_round", "round", "ou", "u", "w"],
  fv: ["viseme_fv", "mouth_fv", "fv", "f", "v"],
  smile: ["viseme_smile", "mouth_smile", "smile", "happy"],
};

export function normalizeMorphName(name: string): string {
  return name.replace(/[\s._-]+/g, "").toLowerCase();
}

export function visemeWeight(viseme: Viseme, mouthOpen: number, mouthWidth: number): number {
  if (viseme === "closed") return Math.max(0, Math.min(0.35, 1 - mouthOpen - mouthWidth * 0.2));
  if (viseme === "mbp") return 0.82;
  if (viseme === "smile") return Math.max(0.45, Math.min(1, mouthWidth));
  return Math.max(0.18, Math.min(1, mouthOpen * 0.85 + mouthWidth * 0.25));
}

export function stateMotionIntensity(state: AvatarState): number {
  if (state === "speaking") return 1;
  if (state === "listening" || state === "thinking") return 0.55;
  if (state === "concerned" || state === "error") return 0.28;
  return 0.18;
}
