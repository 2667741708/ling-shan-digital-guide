import { onMounted, ref } from "vue";
import { fetchScenicSpots } from "../../api/visitor";
import ScenicMapView from "../../components/ScenicMapView.vue";
const spots = ref([]);
onMounted(async () => {
    spots.value = await fetchScenicSpots();
});
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.main, __VLS_intrinsicElements.main)({
    ...{ class: "page" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.nav, __VLS_intrinsicElements.nav)({
    ...{ class: "top-nav" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
const __VLS_0 = {}.RouterLink;
/** @type {[typeof __VLS_components.RouterLink, typeof __VLS_components.routerLink, typeof __VLS_components.RouterLink, typeof __VLS_components.routerLink, ]} */ ;
// @ts-ignore
const __VLS_1 = __VLS_asFunctionalComponent(__VLS_0, new __VLS_0({
    to: "/guide",
}));
const __VLS_2 = __VLS_1({
    to: "/guide",
}, ...__VLS_functionalComponentArgsRest(__VLS_1));
__VLS_3.slots.default;
var __VLS_3;
/** @type {[typeof ScenicMapView, ]} */ ;
// @ts-ignore
const __VLS_4 = __VLS_asFunctionalComponent(ScenicMapView, new ScenicMapView({
    spots: (__VLS_ctx.spots),
}));
const __VLS_5 = __VLS_4({
    spots: (__VLS_ctx.spots),
}, ...__VLS_functionalComponentArgsRest(__VLS_4));
/** @type {__VLS_StyleScopedClasses['page']} */ ;
/** @type {__VLS_StyleScopedClasses['top-nav']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            ScenicMapView: ScenicMapView,
            spots: spots,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
//# sourceMappingURL=ScenicMap.vue.js.map