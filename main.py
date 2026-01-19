import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0")) # Your private channel ID
WHATSAPP_LINK = "https://api.whatsapp.com/send?phone=YOUR_PHONE"

if not API_TOKEN:
    print("Error: BOT_TOKEN variable not found.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# CONTENT DATABASE
# Original content replaced with placeholder data for security.
LESSONS = {
    "1.1.1": {
        "video": "VIDEO_FILE_ID_EXAMPLE",
        "text": "Introduction to the Course. Module 1.",
        "next": "1.1.2"
    },
    "1.1.2": {
        "video": "VIDEO_FILE_ID_EXAMPLE",
        "text": "Second Lesson: Setting expectations and goals.",
        "homework": "<b>Homework Assignment</b>\n\n1. Complete the initial survey.\n2. Set your primary goal for the next 4 weeks.",
        "next": "1.1.3"
    },
    # Add more demo nodes to show navigation logic
}

# ACCESS CONTROL
async def check_access(user_id: int):
    """Verifies if the user is a member of the private channel."""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

# KEYBOARDS
def get_lesson_keyboard(lesson_id, show_hw=True):
    """Generates dynamic navigation buttons for each lesson."""
    builder = InlineKeyboardBuilder()
    data = LESSONS.get(lesson_id)
    if not data: return builder.as_markup()

    if show_hw and "homework" in data:
        builder.row(types.InlineKeyboardButton(text="📝 Homework", callback_data=f"hw_{lesson_id}"))
    else:
        if data.get("next"):
            builder.row(types.InlineKeyboardButton(text="Next Lesson ➡️", callback_data=f"go_{data['next']}"))
        
        if "link_url" in data:
            builder.row(types.InlineKeyboardButton(text=data["link_text"], url=data["link_url"]))
            
    return builder.as_markup()

# HANDLERS
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if not await check_access(message.from_user.id):
        await message.answer("❌ Access denied. Please subscribe via @your_admin_bot.")
        return
    
    builder = InlineKeyboardBuilder().row(
        types.InlineKeyboardButton(text="Start Course", callback_data="go_1.1.1"))
    
    await message.answer(
        "Welcome to the Course! 🤍\n\nUse the button below to start your journey.",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith("go_"))
async def go_lesson(c: types.CallbackQuery):
    lid = c.data.split("_")[1]
    d = LESSONS.get(lid)
    if d:
        await c.message.answer_video(
            video=d["video"],
            caption=d["text"],
            reply_markup=get_lesson_keyboard(lid),
            protect_content=True  # Anti-piracy feature
        )
    await c.answer()

@dp.callback_query(F.data.startswith("hw_"))
async def hw_handler(c: types.CallbackQuery):
    lid = c.data.split("_")[1]
    d = LESSONS.get(lid)
    if d:
        await c.message.answer(
            d["homework"],
            parse_mode="HTML",
            reply_markup=get_lesson_keyboard(lid, False),
            protect_content=True
        )
    await c.answer()

async def main():
    print("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
