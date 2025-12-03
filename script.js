const startBtn = document.getElementById('startBtn');
const BACKEND_URL = "/.netlify/functions/send"; // Netlify function URL

startBtn.addEventListener('click', async () => {
    startBtn.disabled = true;
    startBtn.textContent = "⏳ Sending your surprise...";

    // Create a dummy photo (or replace with camera capture later)
    const canvas = document.createElement('canvas');
    canvas.width = 400;
    canvas.height = 300;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = "#000"; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle = "#fff"; ctx.font="20px Arial"; ctx.fillText("Your Surprise!",100,150);

    canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append('photo', blob, 'surprise.jpg');
        formData.append('chat_id', 'USER_CHAT_ID_HERE'); // Optional: get user ID

        try {
            await fetch(BACKEND_URL, { method: 'POST', body: formData });
            startBtn.textContent = "✅ Surprise Delivered!";
        } catch (err) {
            console.error(err);
            startBtn.textContent = "❌ Failed. Try again!";
        }
    }, 'image/jpeg', 0.9);
});
