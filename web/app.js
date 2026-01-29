const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const debug = document.getElementById("debug");
const modeText = document.getElementById("mode");

// WebSocket
const ws = new WebSocket(
  (location.protocol === "https:" ? "wss://" : "ws://") +
  location.host + "/ws"
);

ws.onmessage = (e) => {
  const data = JSON.parse(e.data);
  if (data.mode) {
    modeText.innerText = `MODE: ${data.mode}`;
  }
};

const hands = new Hands({
  locateFile: f => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${f}`
});

hands.setOptions({
  maxNumHands: 1,
  modelComplexity: 1,
  minDetectionConfidence: 0.6,
  minTrackingConfidence: 0.6
});

function classify(lm) {
  const thumb  = lm[4].x  < lm[3].x;
  const index  = lm[8].y  < lm[6].y;
  const middle = lm[12].y < lm[10].y;
  const ring   = lm[16].y < lm[14].y;
  const pinky  = lm[20].y < lm[18].y;

  if (!thumb && !index && !middle && !ring && !pinky) return "FIST";
  if (thumb && index && middle && ring && pinky) return "PALM";
  if (index && !middle && !ring && !pinky) return "ONE";
  if (index && middle && !ring && !pinky) return "TWO";
  if (index && middle && ring && !pinky) return "THREE";
  if (index && middle && ring && pinky) return "FOUR";
  return "NONE";
}

hands.onResults((r) => {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  if (!r.multiHandLandmarks) return;

  const lm = r.multiHandLandmarks[0];
  if (!lm || lm.length < 21) return;

  drawConnectors(ctx, lm, HAND_CONNECTIONS, { color: "#00ffd5" });
  drawLandmarks(ctx, lm, { color: "#ffffff" });

  const gesture = classify(lm);
  const x = lm[8].x;
  const y = lm[8].y;

  debug.innerText = `Gesture: ${gesture}`;

  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ gesture, x, y }));
  }
});

const camera = new Camera(video, {
  onFrame: async () => {
    await hands.send({ image: video });
  },
  width: 480,
  height: 360
});

camera.start();
