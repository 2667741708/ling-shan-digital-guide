import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

import { MORPH_TARGET_BY_VISEME, REALISTIC_AVATAR_MODEL_URL, normalizeMorphName, visemeWeight } from "../src/store/avatarRenderer";
import { buildVisemeTimeline, estimateSpeechDurationMs, frameAtTime } from "../src/store/avatarLipSync";

const FRONTEND_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");

function readGlbJson(path: string) {
  const buffer = readFileSync(path);
  expect(buffer.toString("utf-8", 0, 4)).toBe("glTF");
  const version = buffer.readUInt32LE(4);
  expect(version).toBe(2);
  const jsonLength = buffer.readUInt32LE(12);
  const jsonType = buffer.readUInt32LE(16);
  expect(jsonType).toBe(0x4e4f534a);
  return JSON.parse(buffer.toString("utf-8", 20, 20 + jsonLength));
}

describe("avatar local-2d lip sync", () => {
  it("builds a full-duration viseme timeline with punctuation pauses", () => {
    const timeline = buildVisemeTimeline("欢迎来到灵山。请看大佛。", 4200);

    expect(timeline[0].startMs).toBe(0);
    expect(timeline.at(-1)?.endMs).toBe(4200);
    expect(timeline.some((frame) => frame.viseme === "closed" && frame.endMs > frame.startMs)).toBe(true);
    expect(timeline.some((frame) => frame.mouthOpen > 0.5)).toBe(true);
  });

  it("returns the active frame for an elapsed speech time", () => {
    const timeline = buildVisemeTimeline("梵宫适合慢慢参观", 2800);

    expect(frameAtTime(timeline, -1).viseme).toBe("closed");
    expect(frameAtTime(timeline, 900).mouthOpen).toBeGreaterThan(0);
    expect(frameAtTime(timeline, 9999).viseme).toBe("closed");
  });

  it("estimates duration from speaking rate and keeps short answers visible", () => {
    expect(estimateSpeechDurationMs("好", 1)).toBeGreaterThanOrEqual(1200);
    expect(estimateSpeechDurationMs("灵山大佛高八十八米，是灵山胜境的核心景观。", 0.8)).toBeGreaterThan(
      estimateSpeechDurationMs("灵山大佛高八十八米，是灵山胜境的核心景观。", 1.4),
    );
  });

  it("maps consonant mouth contacts to detailed mouth assets", () => {
    const timeline = buildVisemeTimeline("mbp fv", 1800);
    const visemes = timeline.map((frame) => frame.viseme);

    expect(visemes).toContain("mbp");
    expect(visemes).toContain("fv");
  });

  it("publishes every local-2d mouth viseme asset in the frontend public directory", () => {
    const manifestPath = resolve(FRONTEND_ROOT, "public/avatar/mouth/mouth-manifest.json");
    const manifest = JSON.parse(readFileSync(manifestPath, "utf-8"));

    for (const viseme of ["closed", "mbp", "aa", "ee", "oh", "round", "fv", "smile"]) {
      const svgPath = resolve(FRONTEND_ROOT, manifest.visemes[viseme].svg.replace("/avatar/", "public/avatar/"));
      const objPath = resolve(FRONTEND_ROOT, manifest.visemes[viseme].obj.replace("/avatar/", "public/avatar/"));
      expect(existsSync(svgPath)).toBe(true);
      expect(existsSync(objPath)).toBe(true);
    }
  });

  it("provides stable realistic-3d morph target candidates for the AvatarRenderer", () => {
    expect(REALISTIC_AVATAR_MODEL_URL).toBe("/avatar/models/lingling-realistic.glb");
    expect(MORPH_TARGET_BY_VISEME.aa.map(normalizeMorphName)).toContain("visemeaa");
    expect(MORPH_TARGET_BY_VISEME.round.map(normalizeMorphName)).toContain("visemeround");
    expect(visemeWeight("closed", 0, 0.3)).toBeGreaterThan(0);
    expect(visemeWeight("aa", 0.9, 0.72)).toBeGreaterThan(visemeWeight("fv", 0.22, 0.78));
  });

  it("ships a realistic-3d Lingling GLB with the frontend viseme morph targets", () => {
    const modelPath = resolve(FRONTEND_ROOT, "public/avatar/models/lingling-realistic.glb");
    const gltf = readGlbJson(modelPath);
    const targetNames = new Set<string>();

    for (const mesh of gltf.meshes ?? []) {
      for (const name of mesh.extras?.targetNames ?? []) {
        targetNames.add(name);
      }
    }

    expect(gltf.meshes?.length ?? 0).toBeGreaterThan(0);
    expect(gltf.scenes?.[0]?.extras?.lingling_reference_dir).toContain("数字人形象示例");
    expect(gltf.scenes?.[0]?.extras?.lingling_design_brief).toContain("古风汉服");
    for (const viseme of ["closed", "mbp", "aa", "ee", "oh", "round", "fv", "smile"]) {
      expect(targetNames.has(viseme)).toBe(true);
    }
  });
});
