import { computed } from "vue";
import { useAvatarStore } from "../../store/avatar";
const avatar = useAvatarStore();
const expression = computed(() => {
    if (avatar.state === "speaking")
        return "讲解中";
    if (avatar.state === "thinking")
        return "思考中";
    if (avatar.state === "listening")
        return "倾听中";
    if (avatar.state === "concerned")
        return "关切";
    return "微笑待机";
});
const statusClass = computed(() => `avatar-stage state-${avatar.state}`);
const mouthHeight = computed(() => 3 + avatar.mouthOpen * 12);
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: (__VLS_ctx.statusClass) },
    'aria-label': "AI 数字人导游灵灵",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "avatar-scene" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div)({
    ...{ class: "avatar-glow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.svg, __VLS_intrinsicElements.svg)({
    ...{ class: "lingling-portrait" },
    viewBox: "0 0 320 520",
    role: "img",
    'aria-label': "灵灵数字人形象",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.defs, __VLS_intrinsicElements.defs)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.linearGradient, __VLS_intrinsicElements.linearGradient)({
    id: "hanfu",
    x1: "0",
    x2: "1",
    y1: "0",
    y2: "1",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.stop)({
    offset: "0%",
    'stop-color': "#2c8a71",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.stop)({
    offset: "100%",
    'stop-color': "#17544b",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.linearGradient, __VLS_intrinsicElements.linearGradient)({
    id: "sash",
    x1: "0",
    x2: "1",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.stop)({
    offset: "0%",
    'stop-color': "#f1c56d",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.stop)({
    offset: "100%",
    'stop-color': "#e18c5b",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "shadow" },
    d: "M75 486c40 22 132 22 171 0 12-7 10-20-8-27-47-18-109-18-157 0-18 7-19 20-6 27z",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "sleeve sleeve-left" },
    d: "M85 268c-33 38-48 86-39 119 4 15 25 16 37 3 17-19 32-61 43-102z",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "sleeve sleeve-right" },
    d: "M232 268c35 36 52 84 45 118-3 15-25 18-38 5-18-18-35-61-46-102z",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "body" },
    d: "M96 244c-16 58-19 139-8 218 40 22 105 23 145 0 11-79 9-160-8-218-31 18-98 18-129 0z",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "inner-robe" },
    d: "M132 252c-17 47-22 113-16 196 13 6 29 9 45 9 17 0 34-3 48-10 5-82 0-148-18-195-18 9-41 13-59 0z",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "sash" },
    d: "M104 344c38 18 79 19 118 0 4 14 6 29 7 45-38 18-87 18-126 0 0-16 1-31 1-45z",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "neck" },
    d: "M136 205h49v47c-13 13-35 13-49 0z",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "hair-back" },
    d: "M82 151c0-59 36-102 82-102s82 43 82 102c0 67-33 104-82 104s-82-37-82-104z",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "face" },
    d: "M101 143c0-49 27-80 63-80s63 31 63 80c0 55-25 88-63 88s-63-33-63-88z",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "bangs" },
    d: "M98 133c9-48 33-75 66-75 37 0 61 31 68 82-24-16-49-31-69-57-16 28-38 42-65 50z",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.circle)({
    ...{ class: "hairpin" },
    cx: "214",
    cy: "80",
    r: "11",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "hairpin-line" },
    d: "M203 75l34-18",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "eye eye-left" },
    d: "M130 151c8-8 19-8 28 0",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "eye eye-right" },
    d: "M171 151c8-8 19-8 28 0",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.circle)({
    ...{ class: "blush blush-left" },
    cx: "129",
    cy: "174",
    r: "9",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.circle)({
    ...{ class: "blush blush-right" },
    cx: "198",
    cy: "174",
    r: "9",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.rect)({
    ...{ class: "mouth-svg" },
    x: "154",
    y: "183",
    width: "20",
    height: (__VLS_ctx.mouthHeight),
    rx: "8",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "guide-badge" },
    d: "M122 304h78v42h-78z",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.text, __VLS_intrinsicElements.text)({
    x: "160",
    y: "331",
    'text-anchor': "middle",
    ...{ class: "badge-text" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "hand-left" },
    d: "M73 383c-5 11 1 23 12 25 18 4 34-6 39-22-14-7-32-8-51-3z",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    ...{ class: "hand-right" },
    d: "M244 382c6 10 3 22-7 28-16 9-37 2-45-14 13-10 30-15 52-14z",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div)({
    ...{ class: "voice-ring" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "avatar-info" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
(__VLS_ctx.expression);
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "avatar-caption" },
});
(__VLS_ctx.avatar.caption);
/** @type {__VLS_StyleScopedClasses['avatar-scene']} */ ;
/** @type {__VLS_StyleScopedClasses['avatar-glow']} */ ;
/** @type {__VLS_StyleScopedClasses['lingling-portrait']} */ ;
/** @type {__VLS_StyleScopedClasses['shadow']} */ ;
/** @type {__VLS_StyleScopedClasses['sleeve']} */ ;
/** @type {__VLS_StyleScopedClasses['sleeve-left']} */ ;
/** @type {__VLS_StyleScopedClasses['sleeve']} */ ;
/** @type {__VLS_StyleScopedClasses['sleeve-right']} */ ;
/** @type {__VLS_StyleScopedClasses['body']} */ ;
/** @type {__VLS_StyleScopedClasses['inner-robe']} */ ;
/** @type {__VLS_StyleScopedClasses['sash']} */ ;
/** @type {__VLS_StyleScopedClasses['neck']} */ ;
/** @type {__VLS_StyleScopedClasses['hair-back']} */ ;
/** @type {__VLS_StyleScopedClasses['face']} */ ;
/** @type {__VLS_StyleScopedClasses['bangs']} */ ;
/** @type {__VLS_StyleScopedClasses['hairpin']} */ ;
/** @type {__VLS_StyleScopedClasses['hairpin-line']} */ ;
/** @type {__VLS_StyleScopedClasses['eye']} */ ;
/** @type {__VLS_StyleScopedClasses['eye-left']} */ ;
/** @type {__VLS_StyleScopedClasses['eye']} */ ;
/** @type {__VLS_StyleScopedClasses['eye-right']} */ ;
/** @type {__VLS_StyleScopedClasses['blush']} */ ;
/** @type {__VLS_StyleScopedClasses['blush-left']} */ ;
/** @type {__VLS_StyleScopedClasses['blush']} */ ;
/** @type {__VLS_StyleScopedClasses['blush-right']} */ ;
/** @type {__VLS_StyleScopedClasses['mouth-svg']} */ ;
/** @type {__VLS_StyleScopedClasses['guide-badge']} */ ;
/** @type {__VLS_StyleScopedClasses['badge-text']} */ ;
/** @type {__VLS_StyleScopedClasses['hand-left']} */ ;
/** @type {__VLS_StyleScopedClasses['hand-right']} */ ;
/** @type {__VLS_StyleScopedClasses['voice-ring']} */ ;
/** @type {__VLS_StyleScopedClasses['avatar-info']} */ ;
/** @type {__VLS_StyleScopedClasses['avatar-caption']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            avatar: avatar,
            expression: expression,
            statusClass: statusClass,
            mouthHeight: mouthHeight,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
//# sourceMappingURL=DigitalAvatar.vue.js.map