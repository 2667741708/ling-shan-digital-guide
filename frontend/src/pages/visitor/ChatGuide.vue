<script setup lang="ts">
import { onMounted, ref } from "vue";

import { createSession, sendText } from "../../api/visitor";
import DigitalAvatar from "../../components/Avatar/DigitalAvatar.vue";
import ChatPanel from "../../components/ChatPanel.vue";
import { useAvatarStore } from "../../store/avatar";

const avatar = useAvatarStore();
const sessionUuid = ref("");
const messages = ref([{ role: "assistant", content: "您好，我是您的 AI 数字人导游灵灵。" }]);

onMounted(async () => {
  const session: any = await createSession();
  sessionUuid.value = session.session_uuid;
});

async function handleSend(message: string) {
  if (!message.trim()) return;
  messages.value.push({ role: "user", content: message });
  avatar.setState("thinking");
  const response: any = await sendText(sessionUuid.value, message);
  messages.value.push({ role: "assistant", content: response.answer });
  avatar.simulateSpeaking();
}
</script>

<template>
  <main class="page guide-grid">
    <DigitalAvatar />
    <ChatPanel :messages="messages" @send="handleSend" />
  </main>
</template>
