from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.errors import MessageNotModified
from anikamusic import app
from anikamusic.utils import help_pannel, help_back_markup
from anikamusic.utils.database import get_lang
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers

@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client, update):
    is_callback = isinstance(update, CallbackQuery)
    chat_id = update.message.chat.id if is_callback else update.chat.id
    if is_callback:
        try: await update.answer()
        except: pass

    language = await get_lang(chat_id)
    _ = get_string(language)
    keyboard = help_pannel(_, START=None)

    if is_callback:
        try:
            await update.edit_message_text(_["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard)
        except MessageNotModified: pass
    else:
        await update.reply_photo(photo=START_IMG_URL, caption=_["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard)

# This part makes the "Usage" work when you click a command button
@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
async def helper_cb(client, query: CallbackQuery):
    callback_data = query.data.strip()
    cb = callback_data.split(None, 1)[1]
    language = await get_lang(query.message.chat.id)
    _ = get_string(language)
    keyboard = help_back_markup(_)
    
    if cb in helpers.__dict__:
        await query.edit_message_text(getattr(helpers, cb), reply_markup=keyboard)
    else:
        await query.answer("Usage guide not found.", show_alert=True)

# This part makes the arrows work for all 33 commands
@app.on_callback_query(filters.regex("mbot_cb") & ~BANNED_USERS)
async def help_pagination(client, query: CallbackQuery):
    try:
        await query.answer()
        language = await get_lang(query.message.chat.id)
        _ = get_string(language)
        
        # If the first button is Admin (H_B_1), we are on Page 1, so go to Page 2
        current_text = query.message.reply_markup.inline_keyboard[0][0].text
        state = True if current_text == _["H_B_1"] else False
        
        keyboard = help_pannel(_, START=state)
        await query.edit_message_text(_["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard)
    except: pass
