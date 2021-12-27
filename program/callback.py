# Copyright (C) 2021 By Yasak Krallik

from driver.queues import QUEUE
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Hoşgeldiniz [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**\n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) Ban yetkisi gerekmeden grubunuzda güvenli şekilde çalıştırabilirsiniz olası durumlarda Asistanı elle eklemeniz gerekebilir!**

💡 **Bot komutlarını öğrenmek için komutlar bölümüne tıklayın » 📚 Komutlar Butonu!**

🔖 **Bot hakkında bilgi almak için lütfen kılavuzu okuyun » ❓ Temel Kılavuz!**""",
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
                    InlineKeyboardButton("❤ Sahip", url=f"https://t.me/Dnztrmn"),
                ],
                [
                    InlineKeyboardButton(
                        "👥 Sohbet Grubu", url=f"https://t.me/Keyfialemsohbet"
                    ),
                    InlineKeyboardButton(
                        "📣 Kanal", url=f"https://t.me/Yalnzadmlr"
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


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ **Temel Kılavuz:**

1.) **İlk önce beni grubuna eile.**
2.) **Beni yönetici konumuna yükselt.**
3.) **Daha sonra /reload komutu ile admin listesini yenile .**
3.) **Grubuna @{ASSISTANT_NAME} Asistanını /davetet komutu ile davet et aksi takdirde bot çalışmaz**
4.) **Sonra müzik/video nun keyfini çıkarabilirsiniz.**
5.) **Olası durumlarda /reload komutu ile sorunu gidermeye çalışın sorun düzelmezse Destek grubumuzdan yada kişisel olarak bizimle iletişime geçin.**

📌 **Asistanı grubunuzdan çıkarmak için /ugurla komutunu kullanın eklenek içinse  /davetet komutunu kullanabilirsiniz.**

💡 **Sorularınız ve önerileriniz için sohbet grubumuza bekleriz : @{GROUP_SUPPORT}**

⚡ __Destekleyen {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri Dön", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Merhaba [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**

» **Bot hakkında gereken bilgiler ve komutları okumanız ve bilgi sahibi olmanız önerilir  !**

⚡ __Destekleyen {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👷🏻 Admin Komutları", callback_data="cbadmin"),
                    InlineKeyboardButton("🧙🏻 Yetkili Komutları", callback_data="cbsudo"),
                ],[
                    InlineKeyboardButton("📚 Basit Komutlar", callback_data="cbbasic")
                ],[
                    InlineKeyboardButton("🔙 Geri Dön", callback_data="cbstart")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 Bot kullanım komutları:

» /oynat (şarkı ismi/link) - komutu ile şarkınızı oynatın
» /yayin (sorgu/link) - Radyo canlı yayını dinlemenize ve izlemenize olanak tanır
» /izlet (video ismi/link) - video oynatırsınız
» /vyayın - Video canlı yayıni  izlemenize olanak tanır Youtube için geçerlidir
» /liste - Çalma listesini gösterir
» /video (Sorgu) - Video indirebilirsiniz
» /indir (Sorgu) - Müzik indirebilirsiniz
» /sözler (Sorgu) - Şarkı sözlerini ögrenirsiniz
» /ara (sorgu) - Aradığınız müziğin yada klibin birden fazla sorgusunu ekrana getirir link olarak Youtube için geçerlidir

» /ping - Ping durumunu gösterir
» /uptime - Çalışma süresi
» /alive -  Çalışma durumunu gösterir (Grup içi)

⚡️ __Destekleyen {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri Dön", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 Admin Komutları:

» /dur - Yayını durdur
» /devam - Yayına devam et
» /gec -  Geç
» /son - Bitir
» /sustur - Asistanı sustur
» /sesac - Asistanın sesini af
» /ses `1-200` - Asistanın sesini ayarla  (Admin olmanız gerekiyor)
» /reload - Admin listesini günceller
» /davetet - Asistanı davet eder
» /ugurla - Asistanı grubunuzdan atar

⚡️ __Destekleyen {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri Dön", callback_data="cbcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 Bot sorumlusu komutları:

» /rmw - Önbellek temizler
» /rmd - İndirilenleri temizler
» /sysinfo -  Sistem bilgisi gösterir
» /update - Güncelleme durumu gösterir
» /restart - Botu resetler
» /toplucik - Asistanı tüm gruplardan çıkarır

⚡ __Destekleyen {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri Dön", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Anonim hesapsınız !\n\n» Lütfen Anonim hesaptan çıkın.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Burayı kullanmanız için admin olmanız gerekiyor !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
          await query.edit_message_text(
              f"⚙️ **Yönetim paneli** {query.message.chat.title}\n\n⏸ : Durdur stream\n▶️ : Devam et\n🔇 : Sustur\n🔊 : Sesini aç\n⏹ : Bitir",
              reply_markup=InlineKeyboardMarkup(
                  [[
                      InlineKeyboardButton("⏹", callback_data="cbstop"),
                      InlineKeyboardButton("⏸", callback_data="cbpause"),
                      InlineKeyboardButton("▶️", callback_data="cbresume"),
                  ],[
                      InlineKeyboardButton("🔇", callback_data="cbmute"),
                      InlineKeyboardButton("🔊", callback_data="cbunmute"),
                  ],[
                      InlineKeyboardButton("🗑 Kapat", callback_data="cls")],
                  ]
             ),
         )
    else:
        await query.answer("❌ Akış bulunamadı", show_alert=True)


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Burayı kullanmanız için admin olmanız gerekiyor  !", show_alert=True)
    await query.message.delete()
