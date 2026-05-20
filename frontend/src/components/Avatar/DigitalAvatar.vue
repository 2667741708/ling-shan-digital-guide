<script setup lang="ts">
import { computed, defineAsyncComponent, ref } from "vue";
import { useAvatarStore } from "../../store/avatar";
import type { Viseme } from "../../store/avatarLipSync";
import { REALISTIC_AVATAR_MODEL_URL } from "../../store/avatarRenderer";

const avatar = useAvatarStore();
const AvatarRenderer = defineAsyncComponent(() => import("./AvatarRenderer.vue"));
const realisticAvatarReady = ref(false);
const realisticAvatarError = ref("");
const MOUTH_ASSET_BY_VISEME: Record<Viseme, string> = {
  closed: "/avatar/mouth/viseme-closed.svg",
  mbp: "/avatar/mouth/viseme-mbp.svg",
  aa: "/avatar/mouth/viseme-aa.svg",
  ee: "/avatar/mouth/viseme-ee.svg",
  oh: "/avatar/mouth/viseme-oh.svg",
  round: "/avatar/mouth/viseme-round.svg",
  fv: "/avatar/mouth/viseme-fv.svg",
  smile: "/avatar/mouth/viseme-smile.svg",
};

const expression = computed(() => {
  if (avatar.state === "speaking") return "讲解中";
  if (avatar.state === "thinking") return "思考中";
  if (avatar.state === "listening") return "倾听中";
  if (avatar.state === "concerned") return "关切";
  return "微笑待机";
});

const statusClass = computed(() => `avatar-stage state-${avatar.state}`);
const lipSyncModeLabel = computed(() => (realisticAvatarReady.value ? "realistic-3d" : avatar.lipSyncMode));
const mouthAssetHref = computed(() => MOUTH_ASSET_BY_VISEME[avatar.viseme] || MOUTH_ASSET_BY_VISEME.closed);
const mouthFrame = computed(() => {
  const width = 54 + avatar.mouthWidth * 18;
  const height = 26 + avatar.mouthOpen * 18;
  return {
    x: 164 - width / 2,
    y: 182 - height / 2,
    width,
    height,
  };
});
const speechProgressStyle = computed(() => ({ transform: `scaleX(${avatar.speechProgress || 0})` }));

function markRealisticAvatarReady() {
  realisticAvatarReady.value = true;
  realisticAvatarError.value = "";
}

function markRealisticAvatarFailed(reason: string) {
  realisticAvatarReady.value = false;
  realisticAvatarError.value = reason;
}

function playLocalDemo() {
  const text = "欢迎来到灵山胜境，我是 AI 数字人导游灵灵，现在为您演示本地二维口型同步。";
  const speechRate = 0.95;
  if (!("speechSynthesis" in window)) {
    avatar.simulateSpeaking(text, { rate: speechRate });
    return;
  }
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "zh-CN";
  utterance.rate = speechRate;
  utterance.pitch = 1.08;
  utterance.onstart = () => avatar.simulateSpeaking(text, { rate: speechRate, holdUntilStopped: true });
  utterance.onend = () => avatar.finishSpeaking();
  utterance.onerror = () => avatar.finishSpeaking("浏览器语音播报暂时不可用，local-2d 口型演示已结束。");
  window.speechSynthesis.speak(utterance);
  avatar.simulateSpeaking(text, { rate: speechRate, holdUntilStopped: true });
}
</script>

<template>
  <section :class="statusClass" aria-label="AI 数字人导游灵灵">
    <div class="avatar-scene">
      <div class="avatar-glow" />
      <AvatarRenderer
        :class="['avatar-renderer', { 'is-ready': realisticAvatarReady }]"
        :model-url="REALISTIC_AVATAR_MODEL_URL"
        :viseme="avatar.viseme"
        :mouth-open="avatar.mouthOpen"
        :mouth-width="avatar.mouthWidth"
        :avatar-state="avatar.state"
        @ready="markRealisticAvatarReady"
        @failed="markRealisticAvatarFailed"
      />
      <svg
        v-show="!realisticAvatarReady"
        class="lingling-portrait"
        viewBox="0 0 320 520"
        role="img"
        aria-label="灵灵数字人形象"
      >
        <defs>
          <linearGradient id="hanfu" x1="0" x2="1" y1="0" y2="1">
            <stop offset="0%" stop-color="#2c8a71" />
            <stop offset="100%" stop-color="#17544b" />
          </linearGradient>
          <linearGradient id="sash" x1="0" x2="1">
            <stop offset="0%" stop-color="#f1c56d" />
            <stop offset="100%" stop-color="#e18c5b" />
          </linearGradient>
        </defs>

        <path class="shadow" d="M75 486c40 22 132 22 171 0 12-7 10-20-8-27-47-18-109-18-157 0-18 7-19 20-6 27z" />
        <path class="sleeve sleeve-left" d="M85 268c-33 38-48 86-39 119 4 15 25 16 37 3 17-19 32-61 43-102z" />
        <path class="sleeve sleeve-right" d="M232 268c35 36 52 84 45 118-3 15-25 18-38 5-18-18-35-61-46-102z" />
        <path class="body" d="M96 244c-16 58-19 139-8 218 40 22 105 23 145 0 11-79 9-160-8-218-31 18-98 18-129 0z" />
        <path class="inner-robe" d="M132 252c-17 47-22 113-16 196 13 6 29 9 45 9 17 0 34-3 48-10 5-82 0-148-18-195-18 9-41 13-59 0z" />
        <path class="sash" d="M104 344c38 18 79 19 118 0 4 14 6 29 7 45-38 18-87 18-126 0 0-16 1-31 1-45z" />
        <path class="neck" d="M136 205h49v47c-13 13-35 13-49 0z" />
        <path class="hair-back" d="M82 151c0-59 36-102 82-102s82 43 82 102c0 67-33 104-82 104s-82-37-82-104z" />
        <path class="face" d="M101 143c0-49 27-80 63-80s63 31 63 80c0 55-25 88-63 88s-63-33-63-88z" />
        <path class="bangs" d="M98 133c9-48 33-75 66-75 37 0 61 31 68 82-24-16-49-31-69-57-16 28-38 42-65 50z" />
        <circle class="hairpin" cx="214" cy="80" r="11" />
        <path class="hairpin-line" d="M203 75l34-18" />
        <path class="eye eye-left" d="M130 151c8-8 19-8 28 0" />
        <path class="eye eye-right" d="M171 151c8-8 19-8 28 0" />
        <circle class="blush blush-left" cx="129" cy="174" r="9" />
        <circle class="blush blush-right" cx="198" cy="174" r="9" />
        <g :class="['mouth-svg', `viseme-${avatar.viseme}`]">
          <ellipse
            class="mouth-depth"
            cx="164"
            cy="184"
            :rx="mouthFrame.width * 0.42"
            :ry="mouthFrame.height * 0.3"
          />
          <image
            :href="mouthAssetHref"
            :x="mouthFrame.x"
            :y="mouthFrame.y"
            :width="mouthFrame.width"
            :height="mouthFrame.height"
            preserveAspectRatio="xMidYMid meet"
          />
        </g>
        <path class="guide-badge" d="M122 304h78v42h-78z" />
        <text x="160" y="331" text-anchor="middle" class="badge-text">AI 导游</text>
        <path class="hand-left" d="M73 383c-5 11 1 23 12 25 18 4 34-6 39-22-14-7-32-8-51-3z" />
        <path class="hand-right" d="M244 382c6 10 3 22-7 28-16 9-37 2-45-14 13-10 30-15 52-14z" />
      </svg>
      <div class="voice-ring" />
    </div>
    <div class="avatar-info">
      <strong>灵灵</strong>
      <span>{{ expression }}</span>
      <small :title="realisticAvatarError || undefined">{{ lipSyncModeLabel }} · {{ avatar.viseme }}</small>
    </div>
    <button class="avatar-demo-button" type="button" @click="playLocalDemo">本地口型演示</button>
    <div class="speech-progress" aria-hidden="true"><i :style="speechProgressStyle" /></div>
    <p class="avatar-caption">{{ avatar.caption }}</p>
  </section>
</template>
