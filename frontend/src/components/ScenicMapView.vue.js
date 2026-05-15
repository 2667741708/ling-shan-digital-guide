import { computed, ref } from "vue";
const props = defineProps();
const selectedId = ref(null);
const selectedSpot = computed(() => {
    return props.spots.find((spot) => spot.id === selectedId.value) || props.spots.find((spot) => spot.id === 11) || props.spots[0];
});
const routePoints = computed(() => {
    const ids = props.routeSpotIds && props.routeSpotIds.length > 0 ? props.routeSpotIds : [1, 2, 4, 5, 6, 11, 12, 13];
    return ids
        .map((id) => props.spots.find((spot) => spot.id === id))
        .filter((spot) => Boolean(spot))
        .map((spot) => `${spot.map_x},${spot.map_y}`)
        .join(" ");
});
function selectSpot(id) {
    selectedId.value = id;
}
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "map-shell" },
    'aria-label': "灵山胜境景区地图",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "map-toolbar" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (...[$event]) => {
            __VLS_ctx.selectedId = 11;
        } },
    type: "button",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "realistic-map" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.svg, __VLS_intrinsicElements.svg)({
    viewBox: "0 0 100 100",
    preserveAspectRatio: "none",
    'aria-hidden': "true",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.defs, __VLS_intrinsicElements.defs)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.linearGradient, __VLS_intrinsicElements.linearGradient)({
    id: "terrain",
    x1: "0",
    x2: "1",
    y1: "0",
    y2: "1",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.stop)({
    offset: "0%",
    'stop-color': "#dcebd4",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.stop)({
    offset: "55%",
    'stop-color': "#cfe3d0",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.stop)({
    offset: "100%",
    'stop-color': "#b9d5c0",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.linearGradient, __VLS_intrinsicElements.linearGradient)({
    id: "lake",
    x1: "0",
    x2: "1",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.stop)({
    offset: "0%",
    'stop-color': "#c4e5ee",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.stop)({
    offset: "100%",
    'stop-color': "#8fc6d7",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.rect)({
    width: "100",
    height: "100",
    fill: "url(#terrain)",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    d: "M0 73 C16 67 25 72 38 65 C52 58 61 62 76 53 C88 46 94 50 100 43 L100 100 L0 100Z",
    fill: "url(#lake)",
    opacity: "0.82",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    d: "M0 18 C17 6 34 9 51 17 C69 25 82 17 100 9 L100 0 L0 0Z",
    fill: "#8caf8d",
    opacity: "0.62",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    d: "M3 32 C17 24 27 24 41 30 C54 36 69 33 95 21",
    fill: "none",
    stroke: "#98b98f",
    'stroke-width': "2.8",
    opacity: "0.45",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    d: "M13 82 C24 72 33 64 39 55 C45 47 52 40 56 38 C62 34 67 27 72 22 C77 17 82 16 88 18",
    fill: "none",
    stroke: "#f9f2d8",
    'stroke-width': "2.5",
    'stroke-linecap': "round",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    d: "M43 18 C51 26 56 31 60 38 C65 48 70 52 83 58",
    fill: "none",
    stroke: "#f9f2d8",
    'stroke-width': "1.7",
    'stroke-linecap': "round",
    opacity: "0.78",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.path)({
    d: "M58 16 C52 23 48 29 44 38 C39 48 32 56 21 74",
    fill: "none",
    stroke: "#f9f2d8",
    'stroke-width': "1.4",
    'stroke-linecap': "round",
    opacity: "0.6",
});
if (__VLS_ctx.routePoints) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.polyline)({
        points: (__VLS_ctx.routePoints),
        fill: "none",
        stroke: "#d55a3d",
        'stroke-width': "1.25",
        'stroke-linecap': "round",
        'stroke-linejoin': "round",
    });
}
for (const [spot] of __VLS_getVForSourceType((__VLS_ctx.spots))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (...[$event]) => {
                __VLS_ctx.selectSpot(spot.id);
            } },
        key: (spot.id),
        ...{ class: (['map-poi', { active: __VLS_ctx.selectedSpot?.id === spot.id, route: __VLS_ctx.routeSpotIds?.includes(spot.id) }]) },
        type: "button",
        ...{ style: ({ left: `${spot.map_x}%`, top: `${spot.map_y}%` }) },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span)({
        ...{ class: "poi-dot" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
        ...{ class: "poi-label" },
    });
    (spot.name);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "map-legend" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.i)({
    ...{ class: "legend-route" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.i)({
    ...{ class: "legend-lake" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.i)({
    ...{ class: "legend-axis" },
});
if (__VLS_ctx.selectedSpot) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.aside, __VLS_intrinsicElements.aside)({
        ...{ class: "spot-detail" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
    (__VLS_ctx.selectedSpot.name);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
    (__VLS_ctx.selectedSpot.description);
    if (__VLS_ctx.selectedSpot.guide_text) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
            ...{ class: "guide-text" },
        });
        (__VLS_ctx.selectedSpot.guide_text);
    }
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "tag-row" },
    });
    for (const [tag] of __VLS_getVForSourceType((__VLS_ctx.selectedSpot.tags))) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
            key: (tag),
        });
        (tag);
    }
    __VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
    (__VLS_ctx.selectedSpot.recommended_duration || 10);
}
/** @type {__VLS_StyleScopedClasses['map-shell']} */ ;
/** @type {__VLS_StyleScopedClasses['map-toolbar']} */ ;
/** @type {__VLS_StyleScopedClasses['realistic-map']} */ ;
/** @type {__VLS_StyleScopedClasses['poi-dot']} */ ;
/** @type {__VLS_StyleScopedClasses['poi-label']} */ ;
/** @type {__VLS_StyleScopedClasses['map-legend']} */ ;
/** @type {__VLS_StyleScopedClasses['legend-route']} */ ;
/** @type {__VLS_StyleScopedClasses['legend-lake']} */ ;
/** @type {__VLS_StyleScopedClasses['legend-axis']} */ ;
/** @type {__VLS_StyleScopedClasses['spot-detail']} */ ;
/** @type {__VLS_StyleScopedClasses['guide-text']} */ ;
/** @type {__VLS_StyleScopedClasses['tag-row']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            selectedId: selectedId,
            selectedSpot: selectedSpot,
            routePoints: routePoints,
            selectSpot: selectSpot,
        };
    },
    __typeProps: {},
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
    __typeProps: {},
});
; /* PartiallyEnd: #4569/main.vue */
//# sourceMappingURL=ScenicMapView.vue.js.map