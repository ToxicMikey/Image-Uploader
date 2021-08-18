import os
import uuid
import shutil
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from creds import Credentials
from telegraph import upload_file

logging.basicConfig(level=logging.INFO)


TGraph = Client(
    "Image upload bot",
    bot_token=Credentials.BOT_TOKEN,
    api_id=Credentials.API_ID,
    api_hash=Credentials.API_HASH,
)


@TGraph.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        text=f"Hello {message.from_user.first_name}!\n<b>Tôi là phương tiện nhỏ hoặc tệp tin tới bot tải lên liên kết telegra.ph.</b>\n\n▷ Gửi cho tôi file dưới 5MB.\n▷ Sau đó, tôi sẽ tải xuống.\n▷  Sau đó tôi sẽ tải nó lên liên kết telegra.ph.",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="👥 Group", url=f"https://t.me/chiasecamxuc"), InlineKeyboardButton(text="Channel 📢", url=f"https://t.me/cypersex"), ],
                                           [InlineKeyboardButton(text="🤫 My Site", url=f"https://cypersex.xyz"), InlineKeyboardButton(text="Bots of Ryo 🤪", url=f"https://t.me/botsofryo"), InlineKeyboardButton(text="Contact 🤖", url=f"https://t.me/ryostar"),]
                                        #   [InlineKeyboardButton(text="⚜️ Subscribe Now YouTube ⚜️", url=f"https://youtube.com/playlist?list=PLzkiTywVmsSfmhaDdWNZ5PRmmMKGTIxPJ")]
                                          ])
        )


@TGraph.on_message(filters.photo)
async def getimage(client, message):
    tmp = os.path.join("downloads", str(message.chat.id))
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    img_path = os.path.join(tmp, str(uuid.uuid4()) + ".jpg")
    dwn = await message.reply_text("<b>Downloading to my server...</b>", True)
    img_path = await client.download_media(message=message, file_name=img_path)
    await dwn.edit_text("<code>Uploading as telegra.ph link...</code>")
    try:
        response = upload_file(img_path)
    except Exception as error:
        await dwn.edit_text(f"<b>Oops something went wrong\n Please ▷Contact @RyoStar.</b>")
        return
    await dwn.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>,\n\n<b>▷ Please Subscribe</b> ❤️ [@BotsOfRyo](https://t.me/BotsOfRyo)",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🔗 Xem liên kết", url=f"https://telegra.ph{response[0]}"), InlineKeyboardButton(text="Chia sẻ liên kết 👥", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}"), ],
                                           [InlineKeyboardButton(text="👉 Share & Support Me ❤️", url="https://t.me/share/url?url=83ng+k%C3%BD+t.me%2Fcypersex")]])
        )
    shutil.rmtree(tmp, ignore_errors=True)


TGraph.run()
