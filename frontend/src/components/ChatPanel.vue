<script setup lang="ts">
import { ref } from "vue";

defineProps<{ messages: Array<{ role: string; content: string }> }>();
defineEmits<{ send: [message: string] }>();

const draft = ref("");
</script>

<template>
  <section class="panel chat-panel">
    <div class="messages">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
        {{ message.content }}
      </div>
    </div>
    <form class="chat-input" @submit.prevent="$emit('send', draft); draft = ''">
      <input v-model="draft" placeholder="向灵灵提问，例如：我只有两个小时，喜欢历史，怎么逛？" />
      <button>发送</button>
    </form>
  </section>
</template>
