from pyrogram import filters
from pyrogram.types import Message
from X.helpers.basic import edit_or_reply
from .help import *

the_regex = r"^r\/([^\s\/])+"

f = filters.chat([])


@Client.on_message(f)
async def auto_read(bot: Client, message: Message):
    await X.read_history(message.chat.id)
    message.continue_propagation()


@Client.on_message(filters.command("autoscroll", ".") & filters.me)
async def add_to_auto_read(bot: Client, message: Message):
    if message.chat.id in f:
        f.remove(message.chat.id)
        await message.edit("Autoscroll deactivated")
    else:
        f.add(message.chat.id)
        await message.edit("Autoscroll activated")


add_command_help(
    "autoscroll",
    [
        [
            ".autoscroll",
            "Send .autoscroll in any chat to automatically read all sent messages until you call "
            "autoscroll again. This is useful if you have Telegram open on another screen.",
        ],
    ],
)
