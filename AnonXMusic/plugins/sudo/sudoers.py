from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.utils.database import add_sudo, remove_sudo
from AnonXMusic.utils.decorators.language import language
from AnonXMusic.utils.extraction import extract_user
from AnonXMusic.utils.inline import close_markup
from config import BANNED_USERS, OWNER_ID


@app.on_message(filters.command(["addsudo"]) & filters.user(OWNER_ID))
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply_text(_["sudo_1"].format(user.mention))
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(_["sudo_2"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])


@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(OWNER_ID))
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id not in SUDOERS:
        return await message.reply_text(_["sudo_3"].format(user.mention))
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(_["sudo_4"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])


@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"]) & ~BANNED_USERS)
@language
async def sudoers_list(client, message: Message, _):
    # Check if user is the owner or in the SUDOERS list
    if message.from_user.id != OWNER_ID and message.from_user.id not in SUDOERS:
        # Get the owner's profile to create a clickable link
        owner = await app.get_users(OWNER_ID)
        owner_link = f'<a href="tg://user?id={OWNER_ID}">{owner.first_name}</a>'

        # Reply with the customized message for unauthorized users
        return await message.reply_text(
            f"<b>sᴏʀʀʏ ʙᴀʙʏ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴄʜᴇᴄᴋ sᴜᴅᴏ ᴜsᴇʀs 😗</b>\n"
            f"<b>ᴛᴀʟᴋ ᴛᴏ ᴍʏ ᴏᴡɴᴇʀ 👨‍💻  {owner_link}</b>",
            disable_web_page_preview=True,
        )

    # Generate and send the sudo list for authorized users
    text = _["sudo_5"]
    user = await app.get_users(OWNER_ID)
    user = user.first_name if not user.mention else user.mention
    text += f"1➤ {user}\n"
    count = 0
    smex = 0
    for user_id in SUDOERS:
        if user_id != OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += _["sudo_6"]
                count += 1
                text += f"{count}➤ {user}\n"
            except:
                continue
    if not text:
        await message.reply_text(_["sudo_7"])
    else:
        await message.reply_text(text, reply_markup=close_markup(_))