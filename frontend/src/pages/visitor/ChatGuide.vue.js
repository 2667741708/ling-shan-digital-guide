import { onMounted, ref } from "vue";
import { createSession, sendText } from "../../api/visitor";
import DigitalAvatar from "../../components/Avatar/DigitalAvatar.vue";
import ChatPanel from "../../components/ChatPanel.vue";
import { useAvatarStore } from "../../store/avatar";
const avatar = useAvatarStore();
const sessionUuid = ref("");
const messages = ref([{ role: "assistant", content: "您好，我是您的 AI 数字人导游灵灵。" }]);
onMounted(async () => {
    const session = await createSession();
    sessionUuid.value = session.session_uuid;
});
async function handleSend(message) {
    if (!message.trim())
        return;
    messages.value.push({ role: "user", content: message });
    avatar.setState("thinking");
    const response = await sendText(sessionUuid.value, message);
    messages.value.push({ role: "assistant", content: response.answer });
    avatar.simulateSpeaking();
}
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.main, __VLS_intrinsicElements.main)({
    ...{ class: "page guide-grid" },
});
/** @type {[typeof DigitalAvatar, ]} */ ;
// @ts-ignore
const __VLS_0 = __VLS_asFunctionalComponent(DigitalAvatar, new DigitalAvatar({}));
const __VLS_1 = __VLS_0({}, ...__VLS_functionalComponentArgsRest(__VLS_0));
/** @type {[typeof ChatPanel, ]} */ ;
// @ts-ignore
const __VLS_3 = __VLS_asFunctionalComponent(ChatPanel, new ChatPanel({
    ...{ 'onSend': {} },
    messages: (__VLS_ctx.messages),
}));
const __VLS_4 = __VLS_3({
    ...{ 'onSend': {} },
    messages: (__VLS_ctx.messages),
}, ...__VLS_functionalComponentArgsRest(__VLS_3));
let __VLS_6;
let __VLS_7;
let __VLS_8;
const __VLS_9 = {
    onSend: (__VLS_ctx.handleSend)
};
var __VLS_5;
/** @type {__VLS_StyleScopedClasses['page']} */ ;
/** @type {__VLS_StyleScopedClasses['guide-grid']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            DigitalAvatar: DigitalAvatar,
            ChatPanel: ChatPanel,
            messages: messages,
            handleSend: handleSend,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
//# sourceMappingURL=ChatGuide.vue.js.map