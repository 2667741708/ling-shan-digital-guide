import { defineStore } from "pinia";

import { buildVisemeTimeline, estimateSpeechDurationMs, frameAtTime, type Viseme, type VisemeFrame } from "./avatarLipSync";

export type AvatarState = "idle" | "listening" | "thinking" | "speaking" | "happy" | "concerned" | "error";

interface SimulateSpeakingOptions {
  durationMs?: number;
  rate?: number;
  doneCaption?: string;
  holdUntilStopped?: boolean;
}

function nowMs(): number {
  return typeof performance === "undefined" ? Date.now() : performance.now();
}

export const useAvatarStore = defineStore("avatar", {
  state: () => ({
    state: "idle" as AvatarState,
    mouthOpen: 0,
    mouthWidth: 0.3,
    viseme: "closed" as Viseme,
    lipSyncMode: "local-2d" as const,
    speechDurationMs: 0,
    speechProgress: 0,
    speechTimeline: [] as VisemeFrame[],
    speechTimerId: 0,
    emotion: "smile",
    caption: "您好，我是灵灵，正在为您守候。"
  }),
  actions: {
    setState(state: AvatarState) {
      if (state !== "speaking") this.stopSpeechTimer();
      this.state = state;
      this.emotion = state === "concerned" || state === "error" ? "concerned" : state === "thinking" ? "thinking" : "smile";
    },
    setLipFrame(frame: VisemeFrame) {
      this.viseme = frame.viseme;
      this.mouthOpen = frame.mouthOpen;
      this.mouthWidth = frame.mouthWidth;
    },
    closeMouth() {
      this.viseme = "closed";
      this.mouthOpen = 0;
      this.mouthWidth = 0.3;
      this.speechProgress = 0;
    },
    stopSpeechTimer() {
      if (this.speechTimerId) {
        window.clearInterval(this.speechTimerId);
        this.speechTimerId = 0;
      }
    },
    finishSpeaking(doneCaption = "您还可以继续问我路线、历史、拍照点或服务设施。") {
      this.stopSpeechTimer();
      this.closeMouth();
      this.state = "idle";
      this.emotion = "smile";
      this.caption = doneCaption;
    },
    simulateSpeaking(text = "", options: SimulateSpeakingOptions = {}) {
      this.stopSpeechTimer();
      this.state = "speaking";
      this.emotion = "smile";
      this.caption = text || "灵灵正在讲解。";
      this.speechDurationMs = options.durationMs || estimateSpeechDurationMs(this.caption, options.rate);
      this.speechTimeline = buildVisemeTimeline(this.caption, this.speechDurationMs);

      const startedAt = nowMs();
      const maxExternalDurationMs = Math.round(this.speechDurationMs * 1.6);
      const tick = () => {
        const elapsedMs = nowMs() - startedAt;
        this.speechProgress = Math.min(1, elapsedMs / this.speechDurationMs);
        const frameElapsedMs = options.holdUntilStopped ? elapsedMs % this.speechDurationMs : elapsedMs;
        this.setLipFrame(frameAtTime(this.speechTimeline, frameElapsedMs));
        if (elapsedMs >= this.speechDurationMs && !options.holdUntilStopped) {
          this.finishSpeaking(options.doneCaption);
        } else if (options.holdUntilStopped && elapsedMs >= maxExternalDurationMs) {
          this.finishSpeaking(options.doneCaption);
        }
      };

      tick();
      this.speechTimerId = window.setInterval(tick, 70);
      return this.speechDurationMs;
    }
  }
});
