import { computed, onMounted, ref } from "vue";
import { createSession, fetchScenicSpots, recommendRoute, sendText } from "../../api/visitor";
import DigitalAvatar from "../../components/Avatar/DigitalAvatar.vue";
import ChatPanel from "../../components/ChatPanel.vue";
import ScenicMapView from "../../components/ScenicMapView.vue";
import { useAvatarStore } from "../../store/avatar";
const avatar = useAvatarStore();
const sessionUuid = ref("");
const messages = ref([{ role: "assistant", content: "您好，我是您的 AI 数字人导游灵灵。" }]);
const references = ref([]);
const routePlan = ref(null);
const spots = ref([]);
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
    const session = await createSession();
    sessionUuid.value = session.session_uuid;
    spots.value = await fetchScenicSpots();
    routePlan.value = await recommendRoute(sessionUuid.value);
});
async function handleSend(message) {
    if (!message.trim())
        return;
    messages.value.push({ role: "user", content: message });
    avatar.setState("thinking");
    busy.value = true;
    try {
        const response = await sendText(sessionUuid.value, message);
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
    }
    catch (error) {
        avatar.setState("error");
        messages.value.push({ role: "assistant", content: "抱歉，当前问答服务暂时不可用，请稍后再试或改用演示问题。" });
    }
    finally {
        busy.value = false;
    }
}
function speakAnswer(text) {
    avatar.simulateSpeaking(text);
    if (!("speechSynthesis" in window))
        return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "zh-CN";
    utterance.rate = 0.95;
    utterance.pitch = 1.08;
    window.speechSynthesis.speak(utterance);
}
function handleListen() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
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
    recognition.onresult = (event) => {
        const text = event.results?.[0]?.[0]?.transcript || "";
        if (text)
            handleSend(text);
    };
    recognition.onerror = () => {
        avatar.setState("concerned");
        messages.value.push({ role: "assistant", content: "语音识别没有成功，请换成文字输入或重新点击录音。" });
    };
    recognition.onend = () => {
        if (avatar.state === "listening")
            avatar.setState("idle");
    };
    recognition.start();
}
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.main, __VLS_intrinsicElements.main)({
    ...{ class: "page guide-page" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.nav, __VLS_intrinsicElements.nav)({
    ...{ class: "top-nav" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
const __VLS_0 = {}.RouterLink;
/** @type {[typeof __VLS_components.RouterLink, typeof __VLS_components.routerLink, typeof __VLS_components.RouterLink, typeof __VLS_components.routerLink, ]} */ ;
// @ts-ignore
const __VLS_1 = __VLS_asFunctionalComponent(__VLS_0, new __VLS_0({
    to: "/",
}));
const __VLS_2 = __VLS_1({
    to: "/",
}, ...__VLS_functionalComponentArgsRest(__VLS_1));
__VLS_3.slots.default;
var __VLS_3;
const __VLS_4 = {}.RouterLink;
/** @type {[typeof __VLS_components.RouterLink, typeof __VLS_components.routerLink, typeof __VLS_components.RouterLink, typeof __VLS_components.routerLink, ]} */ ;
// @ts-ignore
const __VLS_5 = __VLS_asFunctionalComponent(__VLS_4, new __VLS_4({
    to: "/map",
}));
const __VLS_6 = __VLS_5({
    to: "/map",
}, ...__VLS_functionalComponentArgsRest(__VLS_5));
__VLS_7.slots.default;
var __VLS_7;
const __VLS_8 = {}.RouterLink;
/** @type {[typeof __VLS_components.RouterLink, typeof __VLS_components.routerLink, typeof __VLS_components.RouterLink, typeof __VLS_components.routerLink, ]} */ ;
// @ts-ignore
const __VLS_9 = __VLS_asFunctionalComponent(__VLS_8, new __VLS_8({
    to: "/admin",
}));
const __VLS_10 = __VLS_9({
    to: "/admin",
}, ...__VLS_functionalComponentArgsRest(__VLS_9));
__VLS_11.slots.default;
var __VLS_11;
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "guide-grid" },
});
/** @type {[typeof DigitalAvatar, ]} */ ;
// @ts-ignore
const __VLS_12 = __VLS_asFunctionalComponent(DigitalAvatar, new DigitalAvatar({}));
const __VLS_13 = __VLS_12({}, ...__VLS_functionalComponentArgsRest(__VLS_12));
/** @type {[typeof ChatPanel, ]} */ ;
// @ts-ignore
const __VLS_15 = __VLS_asFunctionalComponent(ChatPanel, new ChatPanel({
    ...{ 'onSend': {} },
    ...{ 'onListen': {} },
    messages: (__VLS_ctx.messages),
    quickPrompts: (__VLS_ctx.quickPrompts),
    busy: (__VLS_ctx.busy),
}));
const __VLS_16 = __VLS_15({
    ...{ 'onSend': {} },
    ...{ 'onListen': {} },
    messages: (__VLS_ctx.messages),
    quickPrompts: (__VLS_ctx.quickPrompts),
    busy: (__VLS_ctx.busy),
}, ...__VLS_functionalComponentArgsRest(__VLS_15));
let __VLS_18;
let __VLS_19;
let __VLS_20;
const __VLS_21 = {
    onSend: (__VLS_ctx.handleSend)
};
const __VLS_22 = {
    onListen: (__VLS_ctx.handleListen)
};
var __VLS_17;
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "guide-support" },
});
if (__VLS_ctx.routePlan) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "route-panel panel" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "section-heading" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
    (__VLS_ctx.routePlan.route_name);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.ol, __VLS_intrinsicElements.ol)({
        ...{ class: "route-steps" },
    });
    for (const [spot] of __VLS_getVForSourceType((__VLS_ctx.routePlan.spots))) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.li, __VLS_intrinsicElements.li)({
            key: (spot.id),
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
        (spot.name);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
        (spot.stay_minutes);
    }
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
    (__VLS_ctx.routePlan.reason);
}
/** @type {[typeof ScenicMapView, ]} */ ;
// @ts-ignore
const __VLS_23 = __VLS_asFunctionalComponent(ScenicMapView, new ScenicMapView({
    spots: (__VLS_ctx.spots),
    routeSpotIds: (__VLS_ctx.routeSpotIds),
}));
const __VLS_24 = __VLS_23({
    spots: (__VLS_ctx.spots),
    routeSpotIds: (__VLS_ctx.routeSpotIds),
}, ...__VLS_functionalComponentArgsRest(__VLS_23));
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "reference-panel panel" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "section-heading" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
(__VLS_ctx.modelUsed);
(__VLS_ctx.latencyMs);
if (!__VLS_ctx.references.length) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
}
else {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.ul, __VLS_intrinsicElements.ul)({});
    for (const [reference] of __VLS_getVForSourceType((__VLS_ctx.references))) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.li, __VLS_intrinsicElements.li)({
            key: (`${reference.document}-${reference.chunk_id}`),
        });
        (reference.document);
        (reference.chunk_id);
    }
}
/** @type {__VLS_StyleScopedClasses['page']} */ ;
/** @type {__VLS_StyleScopedClasses['guide-page']} */ ;
/** @type {__VLS_StyleScopedClasses['top-nav']} */ ;
/** @type {__VLS_StyleScopedClasses['guide-grid']} */ ;
/** @type {__VLS_StyleScopedClasses['guide-support']} */ ;
/** @type {__VLS_StyleScopedClasses['route-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['panel']} */ ;
/** @type {__VLS_StyleScopedClasses['section-heading']} */ ;
/** @type {__VLS_StyleScopedClasses['route-steps']} */ ;
/** @type {__VLS_StyleScopedClasses['reference-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['panel']} */ ;
/** @type {__VLS_StyleScopedClasses['section-heading']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            DigitalAvatar: DigitalAvatar,
            ChatPanel: ChatPanel,
            ScenicMapView: ScenicMapView,
            messages: messages,
            references: references,
            routePlan: routePlan,
            spots: spots,
            busy: busy,
            modelUsed: modelUsed,
            latencyMs: latencyMs,
            quickPrompts: quickPrompts,
            routeSpotIds: routeSpotIds,
            handleSend: handleSend,
            handleListen: handleListen,
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