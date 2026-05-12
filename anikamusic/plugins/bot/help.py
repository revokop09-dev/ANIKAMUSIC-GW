from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.errors import MessageNotModified
from anikamusic import app
from anikamusic.utils import help_pannel
from anikamusic.utils.database import get_lang
from anikamusic.utils.decorators.language import LanguageStart
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string

@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client, update):
    is_callback = isinstance(update, CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        try:
            await update.edit_message_text(
                _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
            )
        except MessageNotModified:
            pass
    else:
        chat_id = update.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_)
        await update.reply_photo(
            photo=START_IMG_URL,
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )

@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = InlineKeyboardMarkup(
        [[types.InlineKeyboardButton(text=_["S_B_1"], url=f"https://t.me/{app.username}?start=help")]]
    )
    await message.reply_text(_["help_2"], reply_markup=keyboard)
