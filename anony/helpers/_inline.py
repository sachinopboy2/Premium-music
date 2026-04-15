# Copyright (c) 2025 AnonymousX1025

from pyrogram import types

from anony import app, config, lang
from anony.core.lang import lang_codes

EMOJI = '<tg-emoji emoji-id="5395513379534170509"></tg-emoji>'


class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton
        
        self.START_TEXT = (
            f"{EMOJI} <b>ɢʀᴇᴇᴛɪɴɢs {{mention}} !</b> {EMOJI}\n\n"
            f"{EMOJI} <b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {{bot_name}}</b> {EMOJI}\n\n"
            "──────────────────────────────\n"
            f"{EMOJI} <b>ɪ ᴀᴍ ᴛʜᴇ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ</b>\n"
            "<b>ᴡɪᴛʜ ᴜʟᴛʀᴀ-ʜɪɢʜ ǫᴜᴀʟɪᴛʏ ᴀᴜᴅɪᴏ sᴜᴘᴘᴏʀᴛ.</b>\n\n"
            f"{EMOJI} <b>ᴘʟᴀʏ sᴏɴɢs ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ & sᴘᴏᴛɪғʏ</b>\n"
            f"{EMOJI} <b>ʟᴀɢ-ғʀᴇᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴇxᴘᴇʀɪᴇɴᴄᴇ</b>\n"
            f"{EMOJI} <b>ᴀᴅᴍɪɴ ᴄᴏɴᴛʀᴏʟs & ᴍᴜʟᴛɪ-ʟᴀɴɢᴜᴀɢᴇ</b>\n"
            "──────────────────────────────\n\n"
            f"{EMOJI} <b>ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ sᴛᴀʀᴛ</b>\n"
            f"<b>ᴇɴᴊᴏʏɪɴɢ ᴛʜᴇ ᴍᴜsɪᴄ ᴡɪᴛʜ ʏᴏᴜʀ ғʀɪᴇɴᴅs!</b> {EMOJI}"
        )

    def cancel_dl(self, text):
        return self.ikm(
            [[self.ikb(text=f"{EMOJI} {text}", callback_data="cancel_dl")]]
        )

    def controls(self, chat_id, status=None, timer=None, remove=False):
        keyboard = []

        if status:
            keyboard.append(
                [self.ikb(text=f"{EMOJI} {status}", callback_data=f"controls status {chat_id}")]
            )
        elif timer:
            keyboard.append(
                [self.ikb(text=f"{EMOJI} {timer}", callback_data=f"controls status {chat_id}")]
            )

        if not remove:
            keyboard.append(
                [
                    self.ikb(f"{EMOJI}", callback_data=f"controls resume {chat_id}"),
                    self.ikb(f"{EMOJI}", callback_data=f"controls pause {chat_id}"),
                    self.ikb(f"{EMOJI}", callback_data=f"controls replay {chat_id}"),
                    self.ikb(f"{EMOJI}", callback_data=f"controls skip {chat_id}"),
                    self.ikb(f"{EMOJI}", callback_data=f"controls stop {chat_id}"),
                ]
            )

        return self.ikm(keyboard)

    def help_markup(self, _lang, back=False):
        if back:
            rows = [
                [
                    self.ikb(text=f"{EMOJI} ʙᴀᴄᴋ", callback_data="help back"),
                    self.ikb(text=f"{EMOJI} ᴄʟᴏsᴇ", callback_data="help close"),
                ]
            ]
        else:
            cbs = ["admins", "auth", "blist", "lang", "ping", "play", "queue", "stats", "sudo"]
            buttons = [
                self.ikb(text=f"{EMOJI} {_lang[f'help_{i}'].upper()}", callback_data=f"help {cb}")
                for i, cb in enumerate(cbs)
            ]
            rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]

        return self.ikm(rows)

    def lang_markup(self, _lang):
        langs = lang.get_languages()

        buttons = [
            self.ikb(
                text=f"{name} {'✓' if code == _lang else ''}",
                callback_data=f"lang_change {code}",
            )
            for code, name in langs.items()
        ]

        rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
        return self.ikm(rows)

    def ping_markup(self, text):
        support = str(config.SUPPORT_CHAT)
        url = support if "t.me" in support or "tg://" in support else f"tg://user?id={support}"
        return self.ikm(
            [[self.ikb(text=f"{EMOJI} {text}", url=url)]]
        )

    def play_queued(self, chat_id, item_id, _text):
        return self.ikm(
            [[self.ikb(text=f"{EMOJI} {_text}", callback_data=f"controls force {chat_id} {item_id}")]]
        )

    def queue_markup(self, chat_id, _text, playing):
        action = "pause" if playing else "resume"
        return self.ikm(
            [[self.ikb(text=f"{EMOJI} {_text}", callback_data=f"controls {action} {chat_id} q")]]
        )

    def settings_markup(self, lang, admin_only, cmd_delete, language, chat_id):
        return self.ikm(
            [
                [
                    self.ikb(f"{EMOJI} {lang['play_mode']}", callback_data="settings"),
                    self.ikb(text=f"{'🔒' if admin_only else '🔓'}", callback_data="settings play"),
                ],
                [
                    self.ikb(f"{EMOJI} {lang['cmd_delete']}", callback_data="settings"),
                    self.ikb(text=f"{'✅' if cmd_delete else '❌'}", callback_data="settings delete"),
                ],
                [
                    self.ikb(f"{EMOJI} {lang['language']}", callback_data="settings"),
                    self.ikb(text=f"🚩 {lang_codes[language]}", callback_data="language"),
                ],
            ]
        )
