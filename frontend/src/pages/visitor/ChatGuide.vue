<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import { createSession, fetchScenicSpots, recommendRoute, sendText, type RoutePlan, type ScenicSpot } from "../../api/visitor";
import DigitalAvatar from "../../components/Avatar/DigitalAvatar.vue";
import ChatPanel from "../../components/ChatPanel.vue";
import ScenicMapView from "../../components/ScenicMapView.vue";
import { useAvatarStore } from "../../store/avatar";

const avatar = useAvatarStore();
const sessionUuid = ref("");
const messages = ref([{ role: "assistant", content: "您好，我是您的 AI 数字人导游灵灵。" }]);
const references = ref<Array<{ document: string; chunk_id: string | number }>>([]);
const routePlan = ref<RoutePlan | null>(null);
const spots = ref<ScenicSpot[]>([]);
const busy = ref(false);
const modelUsed = ref("本地降级");
const latencyMs = ref(0);

const quickPrompts = [
  "我第一次来灵山胜境，应该先看哪里？",
  "我只有两个小时，喜欢历史和拍照，帮我推荐路线。",
  "灵山大佛有什么历史故事？",
  "梵宫和五印坛城有什么特色？",
  "带小孩适合走哪条路线？",
  "附近哪里有洗手间？",
];

const routeSpotIds = computed(() => routePlan.value?.spots.map((spot) => spot.id) || [1, 2, 4, 5, 6, 11]);

onMounted(async () => {
  const session: any = await createSession();
  sessionUuid.value = session.session_uuid;
  spots.value = await fetchScenicSpots();
  routePlan.value = await recommendRoute(sessionUuid.value);
});

async function handleSend(message: string) {
  if (!message.trim()) return;
  messages.value.push({ role: "user", content: message });
  avatar.setState("thinking");
  busy.value = true;
  try {
    const response: any = await sendText(sessionUuid.value, message);
    messages.value.push({ role: "assistant", content: response.answer });
    references.value = response.references || [];
    modelUsed.value = response.model_used || "unknown";
    latencyMs.value = response.latency_ms || 0;
    if (response.cards?.[0]?.spot_ids) {
      routePlan.value = await recommendRoute(sessionUuid.value, {
        interest: message.includes("亲子") ? ["family"] : message.includes("自然") ? ["nature", "photo"] : ["history", "photo"],
        available_time: message.includes("一小时") || message.includes("1小时") ? 60 : 120,
      });
    }
    speakAnswer(response.answer);
  } catch (error) {
    avatar.setState("error");
    messages.value.push({ role: "assistant", content: "抱歉，当前问答服务暂时不可用，请稍后再试或改用演示问题。" });
  } finally {
    busy.value = false;
  }
}

function speakAnswer(text: string) {
  avatar.simulateSpeaking(text);
  if (!("speechSynthesis" in window)) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "zh-CN";
  utterance.rate = 0.95;
  utterance.pitch = 1.08;
  window.speechSynthesis.speak(utterance);
}

function handleListen() {
  const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
  if (!SpeechRecognition) {
    messages.value.push({ role: "assistant", content: "当前浏览器不支持语音识别，请先使用文字输入。Chrome 浏览器通常可以使用该功能。" });
    avatar.setState("concerned");
    return;
  }
  const recognition = new SpeechRecognition();
  recognition.lang = "zh-CN";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  avatar.setState("listening");
  recognition.onresult = (event: any) => {
    const text = event.results?.[0]?.[0]?.transcript || "";
    if (text) handleSend(text);
  };
  recognition.onerror = () => {
    avatar.setState("concerned");
    messages.value.push({ role: "assistant", content: "语音识别没有成功，请换成文字输入或重新点击录音。" });
  };
  recognition.onend = () => {
    if (avatar.state === "listening") avatar.setState("idle");
  };
  recognition.start();
}
</script>

<template>
  <main class="page guide-page">
    <nav class="top-nav">
      <strong>LingTour AI · 灵山数字人导览</strong>
      <router-link to="/">首页</router-link>
      <router-link to="/map">地图导览</router-link>
      <router-link to="/admin">管理大屏</router-link>
    </nav>

    <section class="guide-grid">
      <DigitalAvatar />
      <ChatPanel :messages="messages" :quick-prompts="quickPrompts" :busy="busy" @send="handleSend" @listen="handleListen" />
    </section>

    <section class="guide-support">
      <div class="route-panel panel" v-if="routePlan">
        <div class="section-heading">
          <span>当前推荐路线</span>
          <strong>{{ routePlan.route_name }}</strong>
        </div>
        <ol class="route-steps">
          <li v-for="spot in routePlan.spots" :key="spot.id">
            <strong>{{ spot.name }}</strong>
            <span>{{ spot.stay_minutes }} 分钟</span>
          </li>
        </ol>
        <p>{{ routePlan.reason }}</p>
      </div>

      <ScenicMapView :spots="spots" :route-spot-ids="routeSpotIds" />

      <div class="reference-panel panel">
        <div class="section-heading">
          <span>回答依据</span>
          <strong>{{ modelUsed }} · {{ latencyMs }}ms</strong>
        </div>
        <p v-if="!references.length">提问后这里会显示知识库引用来源。</p>
        <ul v-else>
          <li v-for="reference in references" :key="`${reference.document}-${reference.chunk_id}`">
            {{ reference.document }} #{{ reference.chunk_id }}
          </li>
        </ul>
      </div>
    </section>
  </main>
</template>
