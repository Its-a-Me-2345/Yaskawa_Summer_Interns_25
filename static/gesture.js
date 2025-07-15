const config = {
  video: { width: 640, height: 480, fps: 15 },
};

let videoWidth, videoHeight, drawingContext, canvas, gestureEstimator;
let model;

const gestureStrings = {
  'victory': '✌️ X axis → +',
  'yo': '🤟 X axis → -',
  'thumbs_up': '👍 Z axis → +',
  'thumbs_down': '👎 Z axis → -',
};

function logGestureCommand(name) {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/log-gesture', true);
  xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  xhr.send(JSON.stringify({ gesture: name, timestamp: new Date().toISOString() }));
}

const fingerLookupIndices = {
  thumb: [0, 1, 2, 3, 4],
  index: [0, 5, 6, 7, 8],
  middle: [0, 9, 10, 11, 12],
  ring: [0, 13, 14, 15, 16],
  pinky: [0, 17, 18, 19, 20],
};

const landmarkColors = {
  thumb: 'red',
  index: 'blue',
  middle: 'green',
  ring: 'orange',
  pinky: 'purple',
  palmBase: 'black',
};

function drawKeyPoints(keypoints) {
  for (let i = 0; i < keypoints.length; i++) {
    const y = keypoints[i][0];
    const x = keypoints[i][1];
    drawPoint(x - 2, y - 2, 3);
  }

  const fingers = Object.keys(fingerLookupIndices);
  for (let i = 0; i < fingers.length; i++) {
    const finger = fingers[i];
    const points = fingerLookupIndices[finger].map((inx) => keypoints[inx]);
    drawPath(points, false, landmarkColors[finger]);
  }
}

function drawPoint(y, x, r) {
  drawingContext.beginPath();
  drawingContext.arc(x, y, r, 0, 2 * Math.PI);
  drawingContext.fill();
}

function drawPath(points, closePath, color) {
  drawingContext.strokeStyle = color;
  const region = new Path2D();
  region.moveTo(points[0][0], points[0][1]);
  for (let i = 1; i < points.length; i++) {
    const point = points[i];
    region.lineTo(point[0], point[1]);
  }
  if (closePath) region.closePath();
  drawingContext.stroke(region);
}

async function loadWebcam(width, height, fps) {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    throw new Error('Camera not available');
  }

  let video = document.getElementById('webcam');
  video.muted = true;
  video.width = width;
  video.height = height;

  const stream = await navigator.mediaDevices.getUserMedia({
    audio: false,
    video: {
      facingMode: 'user',
      width,
      height,
      frameRate: { max: fps },
    },
  });

  video.srcObject = stream;

  return new Promise((resolve) => {
    video.onloadedmetadata = () => resolve(video);
  });
}

async function loadVideo() {
  const video = await loadWebcam(config.video.width, config.video.height, config.video.fps);
  video.play();
  return video;
}

// 👉 Custom Gesture Definitions
function createYoGesture() {
  const g = new fp.GestureDescription('yo'); // fixed name
  g.addCurl(fp.Finger.Thumb, fp.FingerCurl.NoCurl, 1.0);
  g.addCurl(fp.Finger.Index, fp.FingerCurl.NoCurl, 1.0);
  g.addCurl(fp.Finger.Pinky, fp.FingerCurl.NoCurl, 1.0);
  g.addCurl(fp.Finger.Middle, fp.FingerCurl.FullCurl, 1.0);
  g.addCurl(fp.Finger.Ring, fp.FingerCurl.FullCurl, 1.0);
  return g;
}

function createThumbsUpGesture() {
  const g = new fp.GestureDescription('thumbs_up'); // fixed name
  g.addCurl(fp.Finger.Thumb, fp.FingerCurl.NoCurl, 1.0);
  g.addDirection(fp.Finger.Thumb, fp.FingerDirection.VerticalUp, 1.0);
  for (let f of [fp.Finger.Index, fp.Finger.Middle, fp.Finger.Ring, fp.Finger.Pinky]) {
    g.addCurl(f, fp.FingerCurl.FullCurl, 1.0);
  }
  return g;
}

function createThumbsDownGesture() {
  const g = new fp.GestureDescription('thumbs_down'); // fixed name
  g.addCurl(fp.Finger.Thumb, fp.FingerCurl.NoCurl, 1.0);
  g.addDirection(fp.Finger.Thumb, fp.FingerDirection.VerticalDown, 1.0);
  for (let f of [fp.Finger.Index, fp.Finger.Middle, fp.Finger.Ring, fp.Finger.Pinky]) {
    g.addCurl(f, fp.FingerCurl.FullCurl, 1.0);
  }
  return g;
}

async function continuouslyDetectLandmarks(video) {
  const knownGestures = [
    fp.Gestures.VictoryGesture,
    createYoGesture(),
    createThumbsUpGesture(),
    createThumbsDownGesture(),
  ];

  gestureEstimator = new fp.GestureEstimator(knownGestures);
  model = await handpose.load();

  async function runDetection() {
    drawingContext.drawImage(video, 0, 0, videoWidth, videoHeight, 0, 0, canvas.width, canvas.height);
    const predictions = await model.estimateHands(video);

    if (predictions.length > 0) {
      const result = predictions[0].landmarks;
      drawKeyPoints(result);

      const est = gestureEstimator.estimate(result, 8.5);
      if (est.gestures.length > 0) {
        let res = est.gestures.reduce((p, c) => (p.score > c.score ? p : c));
        document.getElementById('gesture-text').textContent =
          gestureStrings[res.name] || res.name;
        logGestureCommand(res.name);
      }
    }

    requestAnimationFrame(runDetection);
  }

  runDetection();
}

async function main() {
  let video = await loadVideo();

  videoWidth = video.videoWidth;
  videoHeight = video.videoHeight;

  canvas = document.getElementById('canvas');
  canvas.width = videoWidth;
  canvas.height = videoHeight;

  drawingContext = canvas.getContext('2d');
  drawingContext.clearRect(0, 0, videoWidth, videoHeight);
  drawingContext.fillStyle = 'white';
  drawingContext.translate(canvas.width, 0);
  drawingContext.scale(-1, 1);

  continuouslyDetectLandmarks(video);
}

main();