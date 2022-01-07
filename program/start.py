from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from program import __version__
from driver.veez import user
from driver.filters import command, other_filters
from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""✨ **Hoşgeldin {message.from_user.mention()} !**\n
💭 [{BOT_NAME}](https://t.me/{BOT_USERNAME}) **Ban yetkisi gerekmeden grubunuzda güvenli şekilde çalıştırabilirsiniz olası durumlarda Asistanı elle eklemeniz gerekebilir !**

💡 **Bot komutlarını öğrenmek için komutlar bölümüne tıklayın » 📚 Komutlar Butonu!**

🔖 **Bot hakkında bilgi almak için lütfen kılavuzu okuyun » ❓ Temel Kılavuz!**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Beni Grubuna Ekle ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓ Temel Kılavuz", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("📚 Komutlar", callback_data="cbcmds"),
                    InlineKeyboardButton("❤️ Sahip", url=f"https://t.me/Aaarwencanm"),
                ],
                [
                    InlineKeyboardButton(
                        "👥 Sohbet Grubu", url=f"https://t.me/pavyons"
                    ),
                    InlineKeyboardButton(
                        "📣 Kanal", url=f"https://t.me/gloowarcihwe"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🌐 Destek Kanalı", url="https://t.me/tubidybotdestek"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def alive(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✨ Grup", url=f"https://t.me/pavyons"),
                InlineKeyboardButton(
                    "📣 Kanal", url=f"https://t.me/gloowarcihwe"
                ),
            ]
        ]
    )

    alive = f"**Merhaba {message.from_user.mention()}, Ben {BOT_NAME}**\n\n✨ Bot normal çalışıyor\n🍀 Yapımcı: [{ALIVE_NAME}](https://t.me/Dnztrmn)\n✨ Bot Versiyon: `v{__version__}`\n🍀 Pyrogram Versiyon: `{pyrover}`\n✨ Python Versiyon: `{__python_version__}`\n🍀 PyTgCalls versiyon: `{pytover.__version__}`\n✨ Çalışma süresi: `{uptime}`\n\n**Beni grubuna eklediğin için teşekkür ederim. Video, Canlı yayın ve Müziğin keyfini çıkarman dileği ile herhangi bir sorununuz olursa yapımcı ile iletişime geçebilirsiniz** ❤"

    await message.reply_photo(
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PİNG!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 Bot durumu:\n"
        f"• **Süre:** `{uptime}`\n"
        f"• **Başlangıç zamanı:** `{START_TIME_ISO}`"
    )


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    ass_uname = (await user.get_me()).username
    bot_id = (await c.get_me()).id
    for member in m.new_chat_members:
        if member.id == bot_id:
            return await m.reply(
                "❤️ **Beni grubuna eklediğin için teşekkür ederim !**\n\n"
                "**Şimdi bei yetkilendir ve sonra  /davetet komutu ile asistanı grubuna ekle bazı durumlarda birden fazla denemeniz gerekebilir yada elle eklemeniz gerekebilir.**\n\n"
                "**Bu komutu kullanarak yönetici listesini yenile** /reload",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📣 Kanal", url=f"https://t.me/gloowarcihwe"),
                            InlineKeyboardButton("💭 Grup", url=f"https://t.me/pavyons")
                        ],
                        [
                            InlineKeyboardButton("👤 Asistan", url=f"https://t.me/pavyonsasistanplayer")
                        ]
                    ]
                )
            )
