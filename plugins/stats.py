"""Estatísticas do usuário no Telegram"""

# Originalmente do USERGE-X / Adaptado para o AppleBot
# Criador a partir de: https://github.com/kantek/.../kantek/plugins/private/stats.py
# Módulo criado por: github/code-rgb [TG - @DeletedUser420]


import asyncio
import time

from pyrogram.errors import FloodWait, UserNotParticipant
from userge import Message, userge
from userge.utils import mention_html, time_formatter


@userge.on_cmd(
    "stats",
    about={
        "título": "Suas informações no Telegram sobre grupos, canais e etc.",
        "como usar": "{tr}stats",
    },
)
async def get_stats_(message: Message):
    """Obtenha informações sobre sua conta no Telegram"""
    start = time.time()
    await message.edit(
        "📂 `Coletando informações de sua conta no Telegram, aguarde...`\n"
        "<b>Esse processo pode levar um tempinho.</b>"
    )
    owner = await userge.get_me()
    u_mention = mention_html(owner.id, owner.first_name)
    unread_mentions = 0
    unread_msg = 0
    private_chats = 0
    bots = 0
    users_ = 0
    groups = 0
    groups_admin = 0
    groups_creator = 0
    channels = 0
    channels_admin = 0
    channels_creator = 0
    try:
        async for dialog in userge.iter_dialogs():
            unread_mentions += dialog.unread_mentions_count
            unread_msg += dialog.unread_messages_count
            chat_type = dialog.chat.type
            if chat_type in ["bot", "private"]:
                private_chats += 1
                if chat_type == "bot":
                    bots += 1
                else:
                    users_ += 1
            else:
                try:
                    is_admin = await admin_check(dialog.chat.id, owner.id)
                    is_creator = dialog.chat.is_creator
                except UserNotParticipant:
                    is_admin = False
                    is_creator = False
                if chat_type in ["group", "supergroup"]:
                    groups += 1
                    if is_admin:
                        groups_admin += 1
                    if is_creator:
                        groups_creator += 1
                else:  # Channel
                    channels += 1
                    if is_admin:
                        channels_admin += 1
                    if is_creator:
                        channels_creator += 1
    except FloodWait as e:
        await asyncio.sleep(e.x + 5)

    results = f"""
📊 <b><u>Suas Estatísitas do Telegram</u></b>
👤 Usuário:  <b>{u_mention}</b>

<b>Conversas Privadas:</b> <code>{private_chats}</code><code>
    Com usuários: {users_}
    com bots: {bots}</code>
<b>Grupos:</b> <code>{groups}</code>
<b>Canais:</b> <code>{channels}</code>
<b>Admin de <code>{groups_admin}</code> grupos
    - Você criou: {groups_creator}
    • Como Admin em: {groups_admin - groups_creator}</code>
<b>Admin de</b> <code>{channels_admin}</code> canais
    - Você criou: {channels_creator}
    • Como Admin: {channels_admin - channels_creator}</code>
<b>Mensagens que você nem ao menos leu:</b> <code>{unread_msg}</code>
<b>Mencionaram você e tu nem viu:</b> <code>{unread_mentions}</code>
"""
    end = time.time()
    results += f"\n <i>Tempo deste processo foi: {time_formatter(end - start)}.</i>"
    await message.edit(results)

#  https://git.colinshark.de/PyroBot/PyroBot/src/branch
#  /master/pyrobot/modules/admin.py#L69
async def admin_check(chat_id: int, user_id: int) -> bool:
    check_status = await userge.get_chat_member(chat_id, user_id)
    admin_strings = ["creator", "administrator"]
    return check_status.status in admin_strings
