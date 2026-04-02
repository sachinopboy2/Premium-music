# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import types
from pyrogram.enums import ButtonStyle

from anony import app, config, lang
from anony.core.lang import lang_codes


class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton
        
        # --- PREMIMUM START MESSAGE ---
        self.START_TEXT = (
            "✨ **ɢʀᴇᴇᴛɪɴɢs {mention} !** ✨\n\n"
            "🎵 **ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {bot_name}** 🚀\n\n"
            "──────────────────────────────\n"
            "🎧 **ɪ ᴀᴍ ᴛʜᴇ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ**\n"
            "**ᴡɪᴛʜ ᴜʟᴛʀᴀ-ʜɪɢʜ ǫᴜᴀʟɪᴛʏ ᴀᴜᴅɪᴏ sᴜᴘᴘᴏʀᴛ.**\n\n"
            "🔹 **ᴘʟᴀʏ sᴏɴɢs ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ & sᴘᴏᴛɪғʏ**\n"
            "🔹 **ʟᴀɢ-ғʀᴇᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴇxᴘᴇʀɪᴇɴᴄᴇ**\n"
            "🔹 **ᴀᴅᴍɪɴ ᴄᴏɴᴛʀᴏʟs & ᴍᴜʟᴛɪ-ʟᴀɴɢᴜᴀɢᴇ**\n"
            "──────────────────────────────\n\n"
            "📢 **ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ sᴛᴀʀᴛ**\n"
            "**ᴇɴᴊᴏʏɪɴɢ ᴛʜᴇ ᴍᴜsɪᴄ ᴡɪᴛʜ ʏᴏᴜʀ ғʀɪᴇɴᴅs!** 🎉"
        )

    def cancel_dl(self, text) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [[self.ikb(text=f"✕ {text}", callback_data="cancel_dl", style=ButtonStyle.DANGER)]]
        )

    def controls(self, chat_id: int, status: str = None, timer: str = None, remove: bool = False):
        keyboard = []

        if status:
            keyboard.append(
                [self.ikb(text=f"📊 {status}", callback_data=f"controls status {chat_id}", style=ButtonStyle.DEFAULT)]
            )
        elif timer:
            keyboard.append(
                [self.ikb(text=f"⏳ {timer}", callback_data=f"controls status {chat_id}", style=ButtonStyle.DEFAULT)]
            )

        if not remove:
            # Stylish Cropped Symbols for Music Controls
            keyboard.append(
                [
                    self.ikb("▶️", callback_data=f"controls resume {chat_id}", style=ButtonStyle.SUCCESS),
                    self.ikb("⏸", callback_data=f"controls pause {chat_id}", style=ButtonStyle.PRIMARY),
                    self.ikb("🔄", callback_data=f"controls replay {chat_id}", style=ButtonStyle.DEFAULT),
                    self.ikb("⏭", callback_data=f"controls skip {chat_id}", style=ButtonStyle.PRIMARY),
                    self.ikb("⏹", callback_data=f"controls stop {chat_id}", style=ButtonStyle.DANGER),
                ]
            )

        return self.ikm(keyboard)

    def help_markup(self, _lang: dict, back: bool = False):
        if back:
            rows = [
                [
                    self.ikb(text="🔙 ʙᴀᴄᴋ", callback_data="help back", style=ButtonStyle.PRIMARY),
                    self.ikb(text="🗑️ ᴄʟᴏsᴇ", callback_data="help close", style=ButtonStyle.DANGER),
                ]
            ]
        else:
            cbs = ["admins", "auth", "blist", "lang", "ping", "play", "queue", "stats", "sudo"]
            buttons = [
                self.ikb(text=f"🔹 {_lang[f'help_{i}'].upper()}", callback_data=f"help {cb}", style=ButtonStyle.PRIMARY)
                for i, cb in enumerate(cbs)
            ]
            rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]

        return self.ikm(rows)

    def lang_markup(self, _lang: str):
        langs = lang.get_languages()

        buttons = [
            self.ikb(
                text=f"{name} {'✓' if code == _lang else ''}",
                callback_data=f"lang_change {code}",
                style=ButtonStyle.SUCCESS if code == _lang else ButtonStyle.PRIMARY
            )
            for code, name in langs.items()
        ]

        rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
        return self.ikm(rows)

    def ping_markup(self, text: str):
        return self.ikm(
            [[self.ikb(text=f"🌐 {text}", url=config.SUPPORT_CHAT, style=ButtonStyle.SUCCESS)]]
        )

    def play_queued(self, chat_id: int, item_id: str, _text: str):
        return self.ikm(
            [[self.ikb(text=f"▶️ {_text}", callback_data=f"controls force {chat_id} {item_id}", style=ButtonStyle.SUCCESS)]]
        )

    def queue_markup(self, chat_id: int, _text: str, playing: bool):
        action = "pause" if playing else "resume"
        icon = "⏸" if playing else "▶️"
        return self.ikm(
            [[self.ikb(text=f"{icon} {_text}", callback_data=f"controls {action} {chat_id} q", style=ButtonStyle.PRIMARY)]]
        )

    def settings_markup(self, lang: dict, admin_only: bool, cmd_delete: bool, language: str, chat_id: int):
        return self.ikm(
            [
                [
                    self.ikb(f"🛠️ {lang['play_mode']}", callback_data="settings", style=ButtonStyle.DEFAULT),
                    self.ikb(text=f"{'🔒' if admin_only else '🔓'}", callback_data="settings play", style=ButtonStyle.SUCCESS),
                ],
                [
                    self.ikb(f"🗑️ {lang['cmd_delete']}", callback_data="settings", style=ButtonStyle.DEFAULT),
                    self.ikb(text=f"{'✅' if cmd_delete else '❌'}", callback_data="settings delete", style=ButtonStyle.PRIMARY),
                ],
                [
                    self.ikb(f"🌐 {lang['language']}", callback_data="settings", style=ButtonStyle.DEFAULT),
                    self.ikb(text=f"🚩 {lang_codes[language]}", callback_data="language", style=ButtonStyle.SUCCESS),
                ],
            ]
        )

    def start_key(self, lang: dict, private: bool = False):
        # Cropped aesthetic buttons
        rows = [
            [
                self.ikb(
                    text="➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕",
                    url=f"https://t.me/{app.username}?startgroup=true",
                    style=ButtonStyle.SUCCESS,
                )
            ],
            [
                self.ikb(text="📜 ʜᴇʟᴘ", callback_data="help", style=ButtonStyle.PRIMARY),
                self.ikb(text="👤 ᴅᴇᴠ", url=config.OWNER_ID, style=ButtonStyle.PRIMARY),
            ],
            [
                self.ikb(text="✨ sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT, style=ButtonStyle.DEFAULT),
                self.ikb(text="📢 ᴜᴘᴅᴀᴛᴇs", url=config.SUPPORT_CHANNEL, style=ButtonStyle.DEFAULT),
            ],
        ]

        if private:
            rows.append(
                [
                    self.ikb(
                        text="❄️ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ❄️",
                        url="https://t.me/link_buyer",
                        style=ButtonStyle.DANGER,
                    )
                ]
            )
        else:
            rows.append(
                [
                    self.ikb(
                        text="🌍 ʟᴀɴɢᴜᴀɢᴇ",
                        callback_data="language",
                        style=ButtonStyle.SUCCESS,
                    )
                ]
            )

        return self.ikm(rows)

    def yt_key(self, link: str):
        return self.ikm(
            [
                [
                    self.ikb(text="✂️ ᴄᴏᴘʏ ʟɪɴᴋ", copy_text=link, style=ButtonStyle.PRIMARY),
                    self.ikb(text="📺 ᴡᴀᴛᴄʜ ᴏɴ ʏᴛ", url=link, style=ButtonStyle.DANGER),
                ]
            ]
        )
