export type Viseme = "closed" | "mbp" | "aa" | "ee" | "oh" | "round" | "fv" | "smile";

export interface VisemeFrame {
  startMs: number;
  endMs: number;
  viseme: Viseme;
  mouthOpen: number;
  mouthWidth: number;
}

const CLOSED_FRAME: VisemeFrame = {
  startMs: 0,
  endMs: 0,
  viseme: "closed",
  mouthOpen: 0,
  mouthWidth: 0,
};

const PUNCTUATION_PAUSES: Record<string, number> = {
  "，": 160,
  ",": 160,
  "、": 130,
  "。": 280,
  ".": 260,
  "！": 300,
  "!": 300,
  "？": 300,
  "?": 300,
  "；": 240,
  ";": 220,
  "：": 180,
  ":": 180,
};

const VISEME_SHAPES: Record<Viseme, Pick<VisemeFrame, "mouthOpen" | "mouthWidth">> = {
  closed: { mouthOpen: 0, mouthWidth: 0.3 },
  mbp: { mouthOpen: 0.04, mouthWidth: 0.36 },
  aa: { mouthOpen: 0.9, mouthWidth: 0.72 },
  ee: { mouthOpen: 0.38, mouthWidth: 1 },
  oh: { mouthOpen: 0.74, mouthWidth: 0.48 },
  round: { mouthOpen: 0.58, mouthWidth: 0.38 },
  fv: { mouthOpen: 0.22, mouthWidth: 0.78 },
  smile: { mouthOpen: 0.32, mouthWidth: 0.88 },
};

function isPauseToken(token: string): boolean {
  return Object.prototype.hasOwnProperty.call(PUNCTUATION_PAUSES, token);
}

function charToViseme(token: string, index: number): Viseme {
  const normalized = token.toLowerCase();
  if (isPauseToken(token) || /\s/.test(token)) return "closed";
  if ("mbp".includes(normalized)) return "mbp";
  if ("fv".includes(normalized)) return "fv";
  if ("aāáǎà".includes(normalized)) return "aa";
  if ("eēéěèiyīíǐì".includes(normalized)) return "ee";
  if ("oōóǒò".includes(normalized)) return "oh";
  if ("uūúǔùüǖǘǚǜvw".includes(normalized)) return "round";

  const codePoint = token.codePointAt(0) || index;
  const sequence: Viseme[] = ["aa", "ee", "oh", "smile", "round", "fv", "mbp", "ee"];
  return sequence[(codePoint + index) % sequence.length];
}

export function estimateSpeechDurationMs(text: string, rate = 1): number {
  const normalizedRate = Math.min(1.8, Math.max(0.5, rate || 1));
  const characters = Array.from(text.trim()).filter((token) => !/\s/.test(token));
  const speechCharacters = characters.filter((token) => !isPauseToken(token)).length;
  const pauseMs = characters.reduce((total, token) => total + (PUNCTUATION_PAUSES[token] || 0), 0);
  const spokenMs = (speechCharacters * 170) / normalizedRate;

  return Math.round(Math.min(18000, Math.max(1200, spokenMs + pauseMs + 500)));
}

export function buildVisemeTimeline(text: string, durationMs = estimateSpeechDurationMs(text)): VisemeFrame[] {
  const safeDuration = Math.max(240, Math.round(durationMs));
  const tokens = Array.from(text.trim()).filter((token) => !/\s/.test(token));
  if (!tokens.length) {
    return [{ ...CLOSED_FRAME, endMs: safeDuration }];
  }

  const weights = tokens.map((token) => (isPauseToken(token) ? Math.max(1.2, (PUNCTUATION_PAUSES[token] || 180) / 120) : 1));
  const totalWeight = weights.reduce((sum, weight) => sum + weight, 0);
  let cursor = 0;

  return tokens.map((token, index) => {
    const isLast = index === tokens.length - 1;
    const frameDuration = isLast ? safeDuration - cursor : Math.max(60, Math.round((safeDuration * weights[index]) / totalWeight));
    const startMs = cursor;
    const endMs = isLast ? safeDuration : Math.min(safeDuration, startMs + frameDuration);
    cursor = endMs;

    const viseme = charToViseme(token, index);
    const shape = VISEME_SHAPES[viseme];
    return {
      startMs,
      endMs,
      viseme,
      mouthOpen: shape.mouthOpen,
      mouthWidth: shape.mouthWidth,
    };
  });
}

export function frameAtTime(timeline: VisemeFrame[], elapsedMs: number): VisemeFrame {
  if (!timeline.length || elapsedMs < 0) return CLOSED_FRAME;
  const activeFrame = timeline.find((frame) => elapsedMs >= frame.startMs && elapsedMs < frame.endMs);
  const finalEndMs = timeline[timeline.length - 1]?.endMs || 0;
  return activeFrame || { ...CLOSED_FRAME, startMs: finalEndMs, endMs: finalEndMs };
}
