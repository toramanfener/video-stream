# Copyright (C) 2021 Yasak Krallik-Project
# Proje Başlangıç Tarihi 20/10/2021
# Proje Yayım Tarihi 05/12/2021

import re
import asyncio

from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.veez import call_py, user
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:70]
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["oynat", f"oynat@{BOT_USERNAME}"]) & other_filters)
async def play(c: Client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="• Menü", callback_data="cbmenu"),
                InlineKeyboardButton(text="• Kapat", callback_data="cls"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("Sen  __Anonim yöneticisin__ !\n\n» Lütfen anonim hesaptan çık.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 Beni kullanmak için **Yönetici** konumuna yükselt ve şu  **İzinleri**:\n\n» ❌ __Mesajları Silme__\n» ❌ __Kullanıcı Ekleme__\n» ❌ __Sesli Sohbetleri Yönet__\n\nver ve  **Güncelle** Müziğin keyfini çıkartabilirsin.**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "Gerekli izin eksik:" + "\n\n» ❌ __Sesli Sohbetleri Yönet__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "Gerekli izin eksik:" + "\n\n» ❌ __Mesajları Sil__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("Gerekli izin eksik:" + "\n\n» ❌ __Kullanıcı ekle__")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **Bu gruptan yasaklanmış** {m.chat.title}\n\n» **Lütfen yasağı kaldırın ve tekrar deneyin.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **Asistan gruba katılamadı**\n\n**reason**: `{e}`")
                return
        else:
            try:
                user_id = (await user.get_me()).id
                link = await c.export_chat_invite_link(chat_id)
                if "+" in link:
                    link_hash = (link.replace("+", "")).split("t.me/")[1]
                    await ubot.join_chat(link_hash)
                await c.promote_member(chat_id, user_id)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **Asistan gruba katılamadı**\n\n**reason**: `{e}`"
                )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **Müzik indiriliyor...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{}",
                    caption=f"💡 **Şarkı listeye eklendi »** `{pos}`\n\n🏷 **İsim:** [{songname}]({link})\n💭 **Chat:** `{chat_id}`\n🎧 **Talep eden:** {m.from_user.mention()}",
                    reply_markup=keyboard,
                )
            else:
             try:
                await suhu.edit("🔄 **Katılıyor...**")
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{}",
                    caption=f"💡 **Müzik yayını başladı.**\n\n🏷 **İsim:** [{songname}]({link})\n💭 **Chat:** `{chat_id}`\n💡 **Durumu:** `Çalıyor`\n🎧 **Talep eden:** {requester}",
                    reply_markup=keyboard,
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f"🚫 error:\n\n» {e}")
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» Çalmam için  **Müzik Dosyası** ver **yada çalmam için isim yada link belirle..**"
                )
            else:
                suhu = await c.send_message(chat_id, "🔎 **Aranıyor...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("❌ **Arama başarısız.**")
                else:
                    songname = search[0]
                    url = search[1]
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{}",
                                caption=f"💡 **Müzik listeye eklendi »** `{pos}`\n\n🏷 **İsim:** [{songname}]({url})\n💭 **Chat:** `{chat_id}`\n🎧 **Talep eden:** {requester}",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await suhu.edit("🔄 **Katılıyor...**")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=f"{}",
                                    caption=f"💡 **Müzik yayını başlatıldı.**\n\n🏷 **İsim:** [{songname}]({url})\n💭 **Chat:** `{chat_id}`\n💡 **Durumu:** `Oynuyor`\n🎧 **Talep eden:** {requester}",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await suhu.delete()
                                await m.reply_text(f"🚫 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» Çalmam için **Müzik Dosyası** ver **yada çalmam için isim yada link belirle.**"
            )
        else:
            suhu = await c.send_message(chat_id, "🔎 **Aranıyor...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("❌ **Arama başarısız.**")
            else:
                songname = search[0]
                url = search[1]
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=f"{}",
                            caption=f"💡 **Müzik listeye eklendi »** `{pos}`\n\n🏷 **İsim:** [{songname}]({url})\n💭 **Chat:** `{chat_id}`\n🎧 **Talep eden:** {requester}",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await suhu.edit("🔄 **Katılıyor...**")
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{}",
                                caption=f"💡 **Müzik yayını başladı.**\n\n🏷 **İsim:** [{songname}]({url})\n💭 **Chat:** `{chat_id}`\n💡 **Durum:** `Oynuyor`\n🎧 **Talep eden:** {requester}",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"🚫 error: `{ep}`")


# stream is used for live streaming only


@Client.on_message(command(["yayın", f"yayın@{BOT_USERNAME}"]) & other_filters)
async def stream(c: Client, m: Message):
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="• Menü", callback_data="cbmenu"),
                InlineKeyboardButton(text="• Kapat", callback_data="cls"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("Sen __Anonim yöneticisin__ !\n\n» Lütfen anonim hesaptan çık.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 Beni mullanmak için  **Yönetici** konumuna yükselt ve şu   **İzinleri**:\n\n» ❌ __Mesajları silme__\n» ❌ __Kullanıcıları ekleme__\n» ❌ __Sesli sohbetleri yönetme__\n\nver ve **Güncelle**  müziğin keyfini çıkartabilirsin**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "Gerekli izin eksik:" + "\n\n» ❌ __Sesli sohbetleri yönetme__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "Gerekli izin eksik:" + "\n\n» ❌ __Mesajları silme__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("Gerekli izin eksim:" + "\n\n» ❌ __Kullanıcıları ekleme__")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **Asistan gruptan yasaklanmış** {m.chat.title}\n\n» **Kullanabilmek için lütfen yasağı kaldırın sonra tekrar deneyin.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **Asistan sohbete katılamadı**\n\n**reason**: `{e}`")
                return
        else:
            try:
                user_id = (await user.get_me()).id
                link = await c.export_chat_invite_link(chat_id)
                if "+" in link:
                    link_hash = (link.replace("+", "")).split("t.me/")[1]
                    await ubot.join_chat(link_hash)
                await c.promote_member(chat_id, user_id)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **Asistan sohbete katılamadı**\n\n**reason**: `{e}`"
                )

    if len(m.command) < 2:
        await m.reply("» Lütfen canlı olarak oynatabileceğim kanalın linkini belirtiniz Youtube için geçerlidi-.")
    else:
        link = m.text.split(None, 1)[1]
        suhu = await c.send_message(chat_id, "🔄 **Akış işleniyor...**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await suhu.edit(f"❌ yt-dl issues detected\n\n» `{livelink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Radio", livelink, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{}",
                    caption=f"💡 **Müzik listeye eklendi »** `{pos}`\n\n💭 **Chat:** `{chat_id}`\n🎧 **Talep eden:** {requester}",
                    reply_markup=keyboard,
                )
            else:
                try:
                    await suhu.edit("🔄 **Katılıyor...**")
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(
                            livelink,
                        ),
                        stream_type=StreamType().live_stream,
                    )
                    add_to_queue(chat_id, "Radio", livelink, link, "Audio", 0)
                    await suhu.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=f"{}",
                        caption=f"💡 **[Music live]({link}) Yayın başladı.**\n\n💭 **Chat:** `{chat_id}`\n💡 **Durum:** `Oynuyor`\n🎧 **Talep eden:** {requester}",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await suhu.delete()
                    await m.reply_text(f"🚫 error: `{ep}`")
