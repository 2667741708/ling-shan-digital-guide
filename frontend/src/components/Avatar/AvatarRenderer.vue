<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { VRMLoaderPlugin, VRMUtils, type VRM } from "@pixiv/three-vrm";
import type { AvatarState } from "../../store/avatar";
import type { Viseme } from "../../store/avatarLipSync";
import {
  MORPH_TARGET_BY_VISEME,
  REALISTIC_AVATAR_MODEL_URL,
  VRM_EXPRESSION_BY_VISEME,
  normalizeMorphName,
  stateMotionIntensity,
  visemeWeight,
} from "../../store/avatarRenderer";

interface Props {
  modelUrl?: string;
  viseme: Viseme;
  mouthOpen: number;
  mouthWidth: number;
  avatarState: AvatarState;
}

type MorphMesh = THREE.Mesh & {
  morphTargetDictionary?: Record<string, number>;
  morphTargetInfluences?: number[];
};

const props = withDefaults(defineProps<Props>(), {
  modelUrl: REALISTIC_AVATAR_MODEL_URL,
});
const emit = defineEmits<{
  ready: [];
  failed: [reason: string];
}>();

const hostRef = ref<HTMLDivElement | null>(null);
const canvasRef = ref<HTMLCanvasElement | null>(null);
const status = ref<"loading" | "ready" | "failed">("loading");

let renderer: THREE.WebGLRenderer | null = null;
let scene: THREE.Scene | null = null;
let camera: THREE.PerspectiveCamera | null = null;
let avatarRoot: THREE.Group | null = null;
let vrm: VRM | null = null;
let resizeObserver: ResizeObserver | null = null;
let animationId = 0;
let previousTime = 0;
let avatarBaseY = 0;
const clock = new THREE.Clock();
const morphMeshes: MorphMesh[] = [];

function clearScene() {
  cancelAnimationFrame(animationId);
  animationId = 0;
  resizeObserver?.disconnect();
  resizeObserver = null;
  if (avatarRoot) {
    avatarRoot.traverse((object) => {
      const mesh = object as THREE.Mesh;
      mesh.geometry?.dispose();
      const material = mesh.material;
      if (Array.isArray(material)) material.forEach((item) => item.dispose());
      else material?.dispose();
    });
  }
  renderer?.dispose();
  renderer = null;
  scene = null;
  camera = null;
  avatarRoot = null;
  vrm = null;
  avatarBaseY = 0;
  morphMeshes.length = 0;
}

function setCanvasSize() {
  if (!hostRef.value || !renderer || !camera) return;
  const width = Math.max(1, hostRef.value.clientWidth);
  const height = Math.max(1, hostRef.value.clientHeight);
  renderer.setSize(width, height, false);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}

function fitModelToStage(root: THREE.Object3D) {
  const box = new THREE.Box3().setFromObject(root);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  const maxAxis = Math.max(size.x, size.y, size.z) || 1;
  const scale = 3.15 / maxAxis;
  root.scale.setScalar(scale);
  root.position.set(-center.x * scale, -box.min.y * scale - 1.55, -center.z * scale);
}

function collectMorphMeshes(root: THREE.Object3D) {
  root.traverse((object) => {
    const mesh = object as MorphMesh;
    if (mesh.isMesh && mesh.morphTargetDictionary && mesh.morphTargetInfluences) {
      morphMeshes.push(mesh);
    }
  });
}

function resetMorphTargets() {
  for (const mesh of morphMeshes) {
    mesh.morphTargetInfluences?.fill(0);
  }
  vrm?.expressionManager?.resetValues();
}

function applyVrmExpressions(weight: number) {
  const manager = vrm?.expressionManager;
  if (!manager) return;

  for (const names of Object.values(VRM_EXPRESSION_BY_VISEME)) {
    for (const name of names) manager.setValue(name, 0);
  }
  for (const name of VRM_EXPRESSION_BY_VISEME[props.viseme]) {
    manager.setValue(name, weight);
  }
}

function applyMeshMorphTargets(weight: number) {
  const candidates = MORPH_TARGET_BY_VISEME[props.viseme].map(normalizeMorphName);
  for (const mesh of morphMeshes) {
    if (!mesh.morphTargetDictionary || !mesh.morphTargetInfluences) continue;
    for (const [name, index] of Object.entries(mesh.morphTargetDictionary)) {
      const normalized = normalizeMorphName(name);
      const shouldEnable = candidates.includes(normalized);
      mesh.morphTargetInfluences[index] = shouldEnable ? weight : 0;
    }
  }
}

function applyAvatarFrame() {
  const weight = visemeWeight(props.viseme, props.mouthOpen, props.mouthWidth);
  resetMorphTargets();
  applyVrmExpressions(weight);
  applyMeshMorphTargets(weight);
}

function animate(timeMs = 0) {
  if (!renderer || !scene || !camera || !avatarRoot) return;
  const elapsed = timeMs / 1000;
  const delta = previousTime ? (timeMs - previousTime) / 1000 : clock.getDelta();
  previousTime = timeMs;
  const intensity = stateMotionIntensity(props.avatarState);

  avatarRoot.position.y = avatarBaseY + Math.sin(elapsed * 2.2) * 0.018 * intensity;
  avatarRoot.rotation.y = Math.sin(elapsed * 0.9) * 0.035 * intensity;
  vrm?.update(delta);
  renderer.render(scene, camera);
  animationId = requestAnimationFrame(animate);
}

async function loadModel() {
  if (!hostRef.value || !canvasRef.value) return;
  clearScene();
  status.value = "loading";

  try {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
    camera.position.set(0, 1.1, 5.2);
    camera.lookAt(0, 0.25, 0);

    renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      canvas: canvasRef.value,
      powerPreference: "high-performance",
    });
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    const hemisphere = new THREE.HemisphereLight(0xf5fbff, 0x5b6f68, 2.1);
    const keyLight = new THREE.DirectionalLight(0xffffff, 2.6);
    keyLight.position.set(2.2, 4.8, 3.2);
    const fillLight = new THREE.DirectionalLight(0xaad7ff, 1.1);
    fillLight.position.set(-3.2, 2.6, 2.4);
    scene.add(hemisphere, keyLight, fillLight);

    const loader = new GLTFLoader();
    loader.register((parser) => new VRMLoaderPlugin(parser));
    const gltf = await loader.loadAsync(props.modelUrl);
    vrm = gltf.userData.vrm as VRM | undefined || null;
    if (vrm) {
      VRMUtils.removeUnnecessaryVertices(vrm.scene);
      VRMUtils.combineSkeletons(vrm.scene);
      avatarRoot = vrm.scene;
    } else {
      avatarRoot = gltf.scene;
    }

    fitModelToStage(avatarRoot);
    avatarBaseY = avatarRoot.position.y;
    collectMorphMeshes(avatarRoot);
    scene.add(avatarRoot);
    setCanvasSize();
    resizeObserver = new ResizeObserver(setCanvasSize);
    resizeObserver.observe(hostRef.value);
    applyAvatarFrame();
    status.value = "ready";
    emit("ready");
    animationId = requestAnimationFrame(animate);
  } catch (error) {
    status.value = "failed";
    clearScene();
    emit("failed", error instanceof Error ? error.message : String(error));
  }
}

watch(
  () => [props.viseme, props.mouthOpen, props.mouthWidth],
  () => {
    if (status.value === "ready") applyAvatarFrame();
  },
);

watch(
  () => props.modelUrl,
  () => {
    void loadModel();
  },
);

onMounted(() => {
  void loadModel();
});

onBeforeUnmount(clearScene);
</script>

<template>
  <div ref="hostRef" class="avatar-renderer-host" :data-status="status">
    <canvas ref="canvasRef" aria-label="真实 3D 数字人灵灵" />
  </div>
</template>
