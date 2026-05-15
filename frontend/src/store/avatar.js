import { defineStore } from "pinia";
export const useAvatarStore = defineStore("avatar", {
    state: () => ({
        state: "idle",
        mouthOpen: 0
    }),
    actions: {
        setState(state) {
            this.state = state;
        },
        simulateSpeaking() {
            this.state = "speaking";
            let tick = 0;
            const timer = window.setInterval(() => {
                tick += 1;
                this.mouthOpen = tick % 2 === 0 ? 1 : 0.25;
                if (tick > 20) {
                    window.clearInterval(timer);
                    this.mouthOpen = 0;
                    this.state = "idle";
                }
            }, 120);
        }
    }
});
//# sourceMappingURL=avatar.js.map