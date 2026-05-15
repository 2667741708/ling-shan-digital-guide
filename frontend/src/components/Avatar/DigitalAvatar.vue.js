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
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "avatar-stage" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "avatar-body" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "avatar-face" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div)({
    ...{ class: "eye left" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div)({
    ...{ class: "eye right" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div)({
    ...{ class: "mouth" },
    ...{ style: ({ height: `${8 + __VLS_ctx.avatar.mouthOpen * 24}px` }) },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div)({
    ...{ class: "avatar-clothes" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "avatar-status" },
});
(__VLS_ctx.expression);
/** @type {__VLS_StyleScopedClasses['avatar-stage']} */ ;
/** @type {__VLS_StyleScopedClasses['avatar-body']} */ ;
/** @type {__VLS_StyleScopedClasses['avatar-face']} */ ;
/** @type {__VLS_StyleScopedClasses['eye']} */ ;
/** @type {__VLS_StyleScopedClasses['left']} */ ;
/** @type {__VLS_StyleScopedClasses['eye']} */ ;
/** @type {__VLS_StyleScopedClasses['right']} */ ;
/** @type {__VLS_StyleScopedClasses['mouth']} */ ;
/** @type {__VLS_StyleScopedClasses['avatar-clothes']} */ ;
/** @type {__VLS_StyleScopedClasses['avatar-status']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            avatar: avatar,
            expression: expression,
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