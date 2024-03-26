import asyncio
import random

import requests
from pyrogram import *
from pyrogram import Client, filters
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.types import *
from pyrogram.types import Message

from config import CMD_HANDLER
from X.helpers.basic import edit_or_reply, get_text
from X.helpers.constants import MEMES

from .help import *

DEFAULTUSER = "Man"


NOBLE = [
    "╲╲╲┏━━┓╭━━━╮╱╱╱\n╲╲╲┗┓┏┛┃╭━╮┃╱╱╱\n╲╲╲╲┃┃┏┫┃╭┻┻┓╱╱\n╱╱╱┏╯╰╯┃╰┫┏━╯╱╱\n╱╱┏┻━┳┳┻━┫┗┓╱╱╱\n╱╱╰━┓┃┃╲┏┫┏┛╲╲╲\n╱╱╱╱┃╰╯╲┃┃┗━╮╲╲\n╱╱╱╱╰━━━╯╰━━┛╲╲",
    "┏━╮\n┃▔┃▂▂┏━━┓┏━┳━━━┓\n┃▂┣━━┻━╮┃┃▂┃▂┏━╯\n┃▔┃▔╭╮▔┃┃┃▔┃▔┗━┓\n┃▂┃▂╰╯▂┃┗╯▂┃▂▂▂┃\n┃▔┗━━━╮┃▔▔▔┃▔┏━╯\n┃▂▂▂▂▂┣╯▂▂▂┃▂┗━╮\n┗━━━━━┻━━━━┻━━━┛",
    "┏┓┏━┳━┳━┳━┓\n┃┗┫╋┣┓┃┏┫┻┫\n┗━┻━┛┗━┛┗━┛\n────­­­­­­­­­YOU────",
    "╦──╔╗─╗╔─╔ ─\n║──║║─║║─╠ ─\n╚═─╚╝─╚╝─╚ ─\n╦─╦─╔╗─╦╦   \n╚╦╝─║║─║║ \n─╩──╚╝─╚╝",
    "╔══╗....<3 \n╚╗╔╝..('\../') \n╔╝╚╗..( •.• ) \n╚══╝..(,,)(,,) \n╔╗╔═╦╦╦═╗ ╔╗╔╗ \n║╚╣║║║║╩╣ ║╚╝║ \n╚═╩═╩═╩═╝ ╚══╝",
    "░I░L░O░V░E░Y░O░U░",
    "┈┈╭━╱▔▔▔▔╲━╮┈┈┈\n┈┈╰╱╭▅╮╭▅╮╲╯┈┈┈\n╳┈┈▏╰┈▅▅┈╯▕┈┈┈┈\n┈┈┈╲┈╰━━╯┈╱┈┈╳┈\n┈┈┈╱╱▔╲╱▔╲╲┈┈┈┈\n┈╭━╮▔▏┊┊▕▔╭━╮┈╳\n┈┃┊┣▔╲┊┊╱▔┫┊┃┈┈\n┈╰━━━━╲╱━━━━╯┈╳",
    "╔ღ═╗╔╗\n╚╗╔╝║║ღ═╦╦╦═ღ\n╔╝╚╗ღ╚╣║║║║╠╣\n╚═ღ╝╚═╩═╩ღ╩═╝",
    "╔══╗ \n╚╗╔╝ \n╔╝(¯'v'¯) \n╚══'.¸./\n╔╗╔═╦╦╦═╗ ╔╗╔╗ \n║╚╣║║║║╩╣ ║╚╝║ \n╚═╩═╩═╩═╝ ╚══╝",
    "╔╗ \n║║╔═╦═╦═╦═╗ ╔╦╗ \n║╚╣╬╠╗║╔╣╩╣ ║║║ \n╚═╩═╝╚═╝╚═╝ ╚═╝ \n╔═╗ \n║═╬═╦╦╦═╦═╦═╦═╦═╗ \n║╔╣╬║╔╣╩╬╗║╔╣╩╣╔╝ \n╚╝╚═╩╝╚═╝╚═╝╚═╩╝",
    "╔══╗ \n╚╗╔╝ \n╔╝╚╗ \n╚══╝ \n╔╗ \n║║╔═╦╦╦═╗ \n║╚╣║║║║╚╣ \n╚═╩═╩═╩═╝ \n╔╗╔╗ ♥️ \n║╚╝╠═╦╦╗ \n╚╗╔╣║║║║ \n═╚╝╚═╩═╝",
    "╔══╗╔╗  ♡ \n╚╗╔╝║║╔═╦╦╦╔╗ \n╔╝╚╗║╚╣║║║║╔╣ \n╚══╝╚═╩═╩═╩═╝\n­­­─────­­­­­­­­­YOU─────",
    "╭╮╭╮╮╭╮╮╭╮╮╭╮╮ \n┃┃╰╮╯╰╮╯╰╮╯╰╮╯ \n┃┃╭┳━━┳━╮╭━┳━━╮ \n┃┃┃┃╭╮┣╮┃┃╭┫╭╮┃ \n┃╰╯┃╰╯┃┃╰╯┃┃╰┻┻╮ \n╰━━┻━━╯╰━━╯╰━━━╯",
    "┊┊╭━╮┊┊┊┊┊┊┊┊┊┊┊ \n━━╋━╯┊┊┊┊┊┊┊┊┊┊┊ \n┊┊┃┊╭━┳╮╭┓┊╭╮╭━╮ \n╭━╋━╋━╯┣╯┃┊┃╰╋━╯ \n╰━╯┊╰━━╯┊╰━┛┊╰━━",
]

R = "❤️"
W = "🤍"

heart_list = [
    W * 9,
    W * 2 + R * 2 + W + R * 2 + W * 2,
    W + R * 7 + W,
    W + R * 7 + W,
    W + R * 7 + W,
    W * 2 + R * 5 + W * 2,
    W * 3 + R * 3 + W * 3,
    W * 4 + R + W * 4,
    W * 9,
]
joined_heart = "\n".join(heart_list)
heartlet_len = joined_heart.count(R)
SLEEP = 0.1


async def _wrap_edit(message, text: str):
    """Floodwait-safe utility wrapper for edit"""
    try:
        await message.edit(text)
    except FloodWait as fl:
        await asyncio.sleep(fl.x)


async def phase1(message):
    """Big scroll"""
    BIG_SCROLL = "🧡💛💚💙💜🖤🤎"
    await _wrap_edit(message, joined_heart)
    for heart in BIG_SCROLL:
        await _wrap_edit(message, joined_heart.replace(R, heart))
        await asyncio.sleep(SLEEP)


async def phase2(message):
    """Per-heart randomiser"""
    ALL = ["❤️"] + list("🧡💛💚💙💜🤎🖤")  # don't include white heart

    format_heart = joined_heart.replace(R, "{}")
    for _ in range(5):
        heart = format_heart.format(*random.choices(ALL, k=heartlet_len))
        await _wrap_edit(message, heart)
        await asyncio.sleep(SLEEP)


async def phase3(message):
    """Fill up heartlet matrix"""
    await _wrap_edit(message, joined_heart)
    await asyncio.sleep(SLEEP * 2)
    repl = joined_heart
    for _ in range(joined_heart.count(W)):
        repl = repl.replace(W, R, 1)
        await _wrap_edit(message, repl)
        await asyncio.sleep(SLEEP)


async def phase4(message):
    """Matrix shrinking"""
    for i in range(7, 0, -1):
        heart_matrix = "\n".join([R * i] * i)
        await _wrap_edit(message, heart_matrix)
        await asyncio.sleep(SLEEP)


@Client.on_message(filters.command(["heart", "love"], cmd) & filters.me)
async def hearts(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    await message.edit("❤️ I")
    await asyncio.sleep(0.5)
    await message.edit("❤️ I Love")
    await asyncio.sleep(0.5)
    await message.edit("❤️ I Love You")
    await asyncio.sleep(3)
    await message.edit("❤️ I Love You <3")


@Client.on_message(
    filters.me & (filters.command(["loveyou"], cmd) | filters.regex("^loveyou "))
)
async def _(client: Client, message: Message):
    noble = random.randint(1, len(NOBLE) - 2)
    reply_text = NOBLE[noble]
    await edit_or_reply(message, reply_text)


@Client.on_message(filters.command("wink", cmd) & filters.me)
async def wink(client: Client, message: Message):
    hmm_s = "https://some-random-api.ml/animu/wink"
    r = requests.get(url=hmm_s).json()
    image_s = r["link"]
    await client.send_video(message.chat.id, image_s)
    await message.delete()


@Client.on_message(filters.command("hug", cmd) & filters.me)
async def hug(client: Client, message: Message):
    hmm_s = "https://some-random-api.ml/animu/hug"
    r = requests.get(url=hmm_s).json()
    image_s = r["link"]
    await client.send_video(message.chat.id, image_s)
    await message.delete()


@Client.on_message(filters.command("pat", cmd) & filters.me)
async def pat(client: Client, message: Message):
    hmm_s = "https://some-random-api.ml/animu/pat"
    r = requests.get(url=hmm_s).json()
    image_s = r["link"]
    await client.send_video(message.chat.id, image_s)
    await message.delete()


@Client.on_message(filters.command("pikachu", cmd) & filters.me)
async def pikachu(client: Client, message: Message):
    hmm_s = "https://some-random-api.ml/img/pikachu"
    r = requests.get(url=hmm_s).json()
    image_s = r["link"]
    await client.send_video(message.chat.id, image_s)
    if image_s.endswith(".png"):
        await client.send_photo(message.chat.id, image_s)
        return
    if image_s.endswith(".jpg"):
        await client.send_photo(message.chat.id, image_s)
        return
    await message.delete()


@Client.on_message(filters.command("hmm", cmd) & filters.me)
async def hello_world(client: Client, message: Message):
    mg = await edit_or_reply(
        message,
        "┈┈╱▔▔▔▔▔╲┈┈┈HM┈HM\n┈╱┈┈╱▔╲╲╲▏┈┈┈HMMM\n╱┈┈╱━╱▔▔▔▔▔╲━╮┈┈\n▏┈▕┃▕╱▔╲╱▔╲▕╮┃┈┈\n▏┈▕╰━▏▊▕▕▋▕▕━╯┈┈\n╲┈┈╲╱▔╭╮▔▔┳╲╲┈┈┈\n┈╲┈┈▏╭━━━━╯▕▕┈┈┈\n┈┈╲┈╲▂▂▂▂▂▂╱╱┈┈┈\n┈┈┈┈▏┊┈┈┈┈┊┈┈┈╲\n┈┈┈┈▏┊┈┈┈┈┊▕╲┈┈╲\n┈╱▔╲▏┊┈┈┈┈┊▕╱▔╲▕\n┈▏┈┈┈╰┈┈┈┈╯┈┈┈▕▕\n┈╲┈┈┈╲┈┈┈┈╱┈┈┈╱┈╲\n┈┈╲┈┈▕▔▔▔▔▏┈┈╱╲╲╲▏\n┈╱▔┈┈▕┈┈┈┈▏┈┈▔╲▔▔\n┈╲▂▂▂╱┈┈┈┈╲▂▂▂╱┈ ",
    )


@Client.on_message(
    filters.me & (filters.command(["ahh"], cmd) | filters.regex("^ahh "))
)
async def hello_world(client: Client, message: Message):
    mg = await edit_or_reply(message, "ahh")
    await asyncio.sleep(0.2)
    await mg.edit("aahh")
    await asyncio.sleep(0.2)
    await mg.edit("aahhh")
    await asyncio.sleep(0.2)
    await mg.edit("aahhhh")
    await asyncio.sleep(0.2)
    await mg.edit("aahhhhh")
    await asyncio.sleep(0.2)
    await mg.edit("aahhhhhh")
    await asyncio.sleep(0.2)
    await mg.edit("aahhhhhhh")
    await asyncio.sleep(0.2)
    await mg.edit("aaahhhhhhhh")


@Client.on_message(filters.command("brain", cmd) & filters.me)
async def pijtau(client: Client, message: Message):
    if message.forward_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 14)
    await message.edit("brain")
    animation_chars = [
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠         <(^_^ <)🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠       <(^_^ <)  🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠     <(^_^ <)    🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠   <(^_^ <)      🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠 <(^_^ <)        🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠<(^_^ <)         🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n(> ^_^)>🧠         🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n  (> ^_^)>🧠       🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n    (> ^_^)>🧠     🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n      (> ^_^)>🧠   🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n        (> ^_^)>🧠 🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n          (> ^_^)>🧠🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n           (> ^_^)>🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n           <(^_^ <)🗑",
    ]
    for i in animation_ttl:

        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 14])


@Client.on_message(filters.command("bomb", cmd) & filters.me)
async def gahite(client: Client, message: Message):
    if message.forward_from:
        return
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await message.edit("💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n")
    await asyncio.sleep(1)
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💥💥💥💥 \n")
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💥💥💥💥 \n💥💥💥💥 \n")
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n😵😵😵😵 \n")
    await asyncio.sleep(0.5)
    await message.edit("`RIP PLOXXX......`")
    await asyncio.sleep(2)


@Client.on_message(filters.command("call", cmd) & filters.me)
async def hajqag(client: Client, message: Message):
    if message.forward_from:
        return
    animation_interval = 3
    animation_ttl = range(0, 18)
    await message.edit("Calling Pavel Durov (ceo of telegram)......")
    animation_chars = [
        "`Connecting To Telegram Headquarters...`",
        "`Call Connected.`",
        "`Telegram: Hello This is Telegram HQ. Who is this?`",
        f"`Me: Yo this is` {DEFAULTUSER} ,`Please Connect me to my lil bro,Pavel Durov `",
        "`User Authorised.`",
        "`Calling Saitama`  `At +916969696969`",
        "`Private  Call Connected...`",
        "`Me: Hello Sir, Please Ban This Telegram Account.`",
        "`Saitama : May I Know Who Is This?`",
        f"`Me: Yo Brah, I Am` {DEFAULTUSER} ",
        "`Saitama : OMG!!! Long time no see, Wassup cat...\nI'll Make Sure That Guy Account Will Get Blocked Within 24Hrs.`",
        "`Me: Thanks, See You Later Brah.`",
        "`Saitama : Please Don't Thank Brah, Telegram Is Our's. Just Gimme A Call When You Become Free.`",
        "`Me: Is There Any Issue/Emergency???`",
        "`Saitama : Yes Sur, There Is A Bug In Telegram v69.6.9.\nI Am Not Able To Fix It. If Possible, Please Help Fix The Bug.`",
        "`Me: Send Me The App On My Telegram Account, I Will Fix The Bug & Send You.`",
        "`Saitama : Sure Sur \nTC Bye Bye :)`",
        "`Private Call Disconnected.`",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 18])


@Client.on_message(filters.command("kill", cmd) & filters.me)
async def gahah(client: Client, message: Message):
    if message.forward_from:
        return
    await message.edit("Ｆｉｉｉｉｉｒｅ")
    await asyncio.sleep(0.5)

@Client.on_message(filters.command("lol", cmd) & filters.me)
async def gahah(client: Client, message: Message):
    if message.forward_from:
        return
    await message.edit("😂😂😂😂😂")
    await asyncio.sleep(0.2)
    await message.edit("🤣🤣🤣🤣🤣")
    await asyncio.sleep(0.2)
    await message.edit("🤣😂😂😂😂")
    await asyncio.sleep(0.2)
    await message.edit("😂🤣😂😂😂")
    await asyncio.sleep(0.2)
    await message.edit("😂😂🤣😂😂")
    await asyncio.sleep(0.2)
    await message.edit("😂😂😂🤣😂⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠")
    await asyncio.sleep(0.2)
    await message.edit("😂😂😂😂🤣")
    await asyncio.sleep(0.2)
    await message.edit("😂😂😂🤣😂")
    await asyncio.sleep(0.2)
    await message.edit("😂😂🤣😂😂")
    await asyncio.sleep(0.2)
    await message.edit("😂🤣😂😂😂")
    await asyncio.sleep(0.2)
    await message.edit("🤣😂😂😂😂")
    await asyncio.sleep(0.2)
    await message.edit("🤣😂🤣😂🤣")
    await asyncio.sleep(0.2)
    await message.edit("😂🤣😂🤣😂")
    await asyncio.sleep(0.2)
    await message.edit("ye sahi thaa 🤣😂")
@Client.on_message(filters.command("wtf", cmd) & filters.me)
async def gagahkah(client: Client, message: Message):
    if message.forward_from:
        return
    animation_interval = 0.8
    animation_ttl = range(0, 5)
    await message.edit("wtf")
    animation_chars = [
        "What",
        "What The",
        "What The F",
        "What The F Brah",
        "[𝗪𝗵𝗮𝘁 𝗧𝗵𝗲 𝗙 𝗕𝗿𝗮𝗵](https://telegra.ph//file/f3b760e4a99340d331f9b.jpg)",
    ]
    for i in animation_ttl:

        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 5])


@Client.on_message(filters.command("ding", cmd) & filters.me)
async def gkahgagw(client: Client, message: Message):
    animation_interval = 0.3
    animation_ttl = range(0, 30)
    animation_chars = [
        "🔴⬛⬛⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬛⬜⬜⬜\n🔴⬜⬜⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬜⬛⬜⬜\n⬜⬜🔴⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬜⬜⬛⬜\n⬜⬜⬜⬜🔴",
        "⬜⬜⬛⬛🔴\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬜⬜⬛⬜\n⬜⬜⬜⬜🔴",
        "⬜⬜⬛⬜⬜\n⬜⬜⬛⬜⬜\n⬜⬜🔴⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬛⬜⬜⬜\n🔴⬜⬜⬜⬜",
        "🔴⬛⬛⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
        "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜  [ DEVIL IS BEST](https://t.me/TryToLiveAlon) ⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜",
    ]
    if message.forward_from:
        return
    await message.edit("ding..dong..ding..dong ...")
    await asyncio.sleep(4)
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 10])


@Client.on_message(filters.command("hypo", cmd) & filters.me)
async def okihakga(client: Client, message: Message):
    if message.forward_from:
        return
    animation= range(0, 15)
    await message.edit("hypo....")
    animation_chars = [
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬛⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬛⬛⬛⬜⬜\n⬜⬜⬛⬜⬛⬜⬜\n⬜⬜⬛⬛⬛⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬛⬛⬛⬛⬛⬛",
        "⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛",
        "⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬛⬛⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬛⬛⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬛⬛⬛⬛⬛⬛",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬛⬛⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬛⬛⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬛⬛⬛⬛⬛⬛",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬛\n⬛⬜⬛⬜⬛\n⬛⬜⬜⬜⬛\n⬛⬛⬛⬛⬛",
        "⬜⬜⬜\n⬜⬛⬜\n⬜⬜⬜",
        "[👉🔴👈])",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 15])


@Client.on_message(filters.command(["gangsta", "gang", "gangstar"], cmd) & filters.me)
async def gajjajay(client: Client, message: Message):
    await message.edit("EVERyBOdy")
    await asyncio.sleep(0.3)
    await message.edit("iZ")
    await asyncio.sleep(0.2)
    await message.edit("GangSTur")
    await asyncio.sleep(0.5)
    await message.edit("UNtIL ")
    await asyncio.sleep(0.2)
    await message.edit("I")
    await asyncio.sleep(0.3)
    await message.edit("ArRivE")
    await asyncio.sleep(0.3)
    await message.edit("🔥🔥🔥")
    await asyncio.sleep(0.3)
    await message.edit("EVERyBOdy iZ GangSTur UNtIL I ArRivE 🔥🔥🔥")


@Client.on_message(filters.command("charging", cmd) & filters.me)
async def timer_blankx(client: Client, message: Message):
    txt = (
        message.text[10:]
        + "\n\n`Tesla Wireless Charging (beta) Started...\nDevice Detected: Nokia 1100\nBattery Percentage:` "
    )
    j = 10
    k = j
    for j in range(j):
        await message.edit(txt + str(k))
        k = k + 10
        await asyncio.sleep(1)
    await asyncio.sleep(1)
    await message.edit(
        "`Tesla Wireless Charging (beta) Completed...\nDevice Detected: Nokia 1100 (Space Grey Varient)\nBattery Percentage:` [100%](https://telegra.ph/file/a45aa7450c8eefed599d9.mp4) ",
        link_preview=True,
    )


@Client.on_message(filters.command(["koc", "kocok"], cmd) & filters.me)
async def kocok(client: Client, message: Message):
    e = await edit_or_reply(message, "8✊===D")
    await e.edit("8=✊==D")
    await e.edit("8==✊=D")
    await e.edit("8===✊D")
    await e.edit("8==✊=D")
    await e.edit("8=✊==D")
    await e.edit("8✊===D")
    await e.edit("8=✊==D")
    await e.edit("8==✊=D")
    await e.edit("8===✊D")
    await e.edit("8==✊=D")
    await e.edit("8=✊==D")
    await e.edit("8✊===D")
    await e.edit("8=✊==D")
    await e.edit("8==✊=D")
    await e.edit("8===✊D")
    await e.edit("8==✊=D")
    await e.edit("8=✊==D")
    await e.edit("8===✊D💦")
    await e.edit("8==✊=D💦💦")
    await e.edit("8=✊==D💦💦💦")
    await e.edit("8✊===D💦💦💦💦")
    await e.edit("8===✊D💦💦💦💦💦")
    await e.edit("8==✊=D💦💦💦💦💦💦")
    await e.edit("8=✊==D💦💦💦💦💦💦💦")
    await e.edit("8✊===D💦💦💦💦💦💦??💦")
    await e.edit("8===✊D💦💦💦💦💦💦💦💦💦")
    await e.edit("8==✊=D💦💦💦💦💦💦💦💦💦💦")
    await e.edit("8=✊==D That's why it's over?")
    await e.edit("😭😭😭😭")


@Client.on_message(filters.command(["fuck", "fucek"], cmd) & filters.me)
async def ngefuck(client: Client, message: Message):
    e = await edit_or_reply(message, ".                       /¯ )")
    await e.edit(".                       /¯ )\n                      /¯  /")
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ "
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              ("
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (\n              \\  "
    )


@Client.on_message(filters.command("hack", cmd) & filters.me)
async def hak(client: Client, message: Message):
    await message.edit_text("Looking for WhatsApp databases in targeted person...")
    await asyncio.sleep(2)
    await message.edit_text(
        " User online: True\nTelegram access: True\nRead Storage: True "
    )
    await asyncio.sleep(2)
    await message.edit_text(
        "Hacking... 0%\n[░░░░░░░░░░░░░░░░░░░░]\n`Looking for WhatsApp...`\nETA: 0m, 20s"
    )
    await asyncio.sleep(2)
    await message.edit_text(
        "Hacking... 11.07%\n[██░░░░░░░░░░░░░░░░░░]\n`Looking for WhatsApp...`\nETA: 0m, 18s"
    )
    await asyncio.sleep(2)
    await message.edit_text(
        "Hacking... 20.63%\n[███░░░░░░░░░░░░░░░░░]\n`Found folder C:/WhatsApp`\nETA: 0m, 16s"
    )
    await asyncio.sleep(2)
    await message.edit_text(
        "Hacking... 34.42%\n[█████░░░░░░░░░░░░░░░]\n`Found folder C:/WhatsApp`\nETA: 0m, 14s"
    )
    await asyncio.sleep(2)
    await message.edit_text(
        "Hacking... 42.17%\n[███████░░░░░░░░░░░░░]\n`Searching for databases`\nETA: 0m, 12s"
    )
    await asyncio.sleep(2)
    await message.edit_text(
        "Hacking... 55.30%\n[█████████░░░░░░░░░░░]\n`Found msgstore.db.crypt12`\nETA: 0m, 10s"
    )
    await asyncio.sleep(2)
    await message.edit_text(
        "Hacking... 64.86%\n[███████████░░░░░░░░░]\n`Found msgstore.db.crypt12`\nETA: 0m, 08s"
    )
    await asyncio.sleep(2)
    await message.edit_text(
        "Hacking... 74.02%\n[█████████████░░░░░░░]\n`Trying to Decrypt...`\nETA: 0m, 06s"
    )
    await asyncio.sleep(2)
    await message.edit_text(
        "Hacking... 86.21%\n[███████████████░░░░░]\n`Trying to Decrypt...`\nETA: 0m, 04s"
    )
    await asyncio.sleep(2)
    await message.edit_text(
        "Hacking... 93.50%\n[█████████████████░░░]\n`Decryption successful!`\nETA: 0m, 02s"
    )
    await asyncio.sleep(2)
    await message.edit_text(
        "Hacking... 100%\n[████████████████████]\n`Scanning file...`\nETA: 0m, 00s"
    )
    await asyncio.sleep(2)
    await message.edit_text("Hacking complete!\nUploading file...")
    await asyncio.sleep(2)
    await message.edit_text(
        "Targeted Account Hacked...!\n\n ✅ File has been successfully uploaded to my server.\nWhatsApp Database:\n`./DOWNLOADS/msgstore.db.crypt12`"
    )


@Client.on_message(filters.command(["kontol", "kntl"], cmd) & filters.me)
async def kontol(client: Client, message: Message):
    emoji = get_text(message)
    kontol = MEMES.CONTROL_IMAGE
    if emoji:
        kontol = kontol.replace("⡀", emoji)
    await message.edit(kontol)


@Client.on_message(filters.command(["penis", "dick"], cmd) & filters.me)
async def titid(client: Client, message: Message):
    emoji = get_text(message)
    titid = MEMES.TITS_IMAGE
    if emoji:
        titid = titid.replace("😋", emoji)
    await message.edit(titid)


@Client.on_message(filters.command("dino", cmd) & filters.me)
async def adadino(client: Client, message: Message):
    typew = await edit_or_reply(message, "`DIN DINNN.....`")
    await asyncio.sleep(1)
    await typew.edit("`DINOOOOSAURUSSSSS!!`")
    await asyncio.sleep(1)
    await typew.edit("`🏃                        🦖`")
    await typew.edit("`🏃                       🦖`")
    await typew.edit("`🏃                      🦖`")
    await typew.edit("`🏃                     🦖`")
    await typew.edit("`🏃   `Larius`         🦖`")
    await typew.edit("`🏃                   🦖`")
    await typew.edit("`🏃                  🦖`")
    await typew.edit("`🏃                 🦖`")
    await typew.edit("`🏃                🦖`")
    await typew.edit("`🏃               🦖`")
    await typew.edit("`🏃              🦖`")
    await typew.edit("`🏃             🦖`")
    await typew.edit("`🏃            🦖`")
    await typew.edit("`🏃           🦖`")
    await typew.edit("`🏃WORGH!   🦖`")
    await typew.edit("`🏃           🦖`")
    await typew.edit("`🏃            🦖`")
    await typew.edit("`🏃             🦖`")
    await typew.edit("`🏃              🦖`")
    await typew.edit("`🏃               🦖`")
    await typew.edit("`🏃                🦖`")
    await typew.edit("`🏃                 🦖`")
    await typew.edit("`🏃                  🦖`")
    await typew.edit("`🏃                   🦖`")
    await typew.edit("`🏃                    🦖`")
    await typew.edit("`🏃                     🦖`")
    await typew.edit("`🏃  Huh-Huh           🦖`")
    await typew.edit("`🏃                   🦖`")
    await typew.edit("`🏃                  🦖`")
    await typew.edit("`🏃                 🦖`")
    await typew.edit("`🏃                🦖`")
    await typew.edit("`🏃               🦖`")
    await typew.edit("`🏃              🦖`")
    await typew.edit("`🏃             🦖`")
    await typew.edit("`🏃            🦖`")
    await typew.edit("`🏃           🦖`")
    await typew.edit("`🏃          🦖`")
    await typew.edit("`🏃         🦖`")
    await typew.edit("`HE'S GETTING CLOSER!!!`")
    await asyncio.sleep(1)
    await typew.edit("`🏃       🦖`")
    await typew.edit("`🏃      🦖`")
    await typew.edit("`🏃     🦖`")
    await typew.edit("`🏃    🦖`")
    await typew.edit("`Just give up`")
    await asyncio.sleep(1)
    await typew.edit("`🧎🦖`")
    await asyncio.sleep(2)
    await typew.edit("`-ENDED-`")


@Client.on_message(filters.command(["sayang", "syg"], cmd) & filters.me)
async def zeyenk(client: Client, message: Message):
    e = await edit_or_reply(message, "I LOVEE YOUUU 💕")
    await e.edit("💝💘💓💗")
    await e.edit("💞💕💗💘")
    await e.edit("💝💘💓💗")
    await e.edit("💞💕💗💘")
    await e.edit("💘💞💗💕")
    await e.edit("💘💞💕💗")
    await e.edit("SAYANG KAMU 💝💖💘")
    await e.edit("💝💘💓💗")
    await e.edit("💞💕💗💘")
    await e.edit("💘💞💕💗")
    await e.edit("SAYANG")
    await e.edit("KAMU")
    await e.edit("SELAMANYA 💕")
    await e.edit("💘💘💘💘")
    await e.edit("SAYANG")
    await e.edit("KAMU")
    await e.edit("SAYANG")
    await e.edit("KAMU")
    await e.edit("I LOVE YOUUUU")
    await e.edit("MY BABY")
    await e.edit("💕💞💘💝")
    await e.edit("💘💕💞💝")
    await e.edit("SAYANG KAMU💞")


@Client.on_message(filters.command("gabut", cmd) & filters.me)
async def menggabut(client: Client, message: Message):
    e = await edit_or_reply(message, "`PERNAAHHHHH KAHHH KAUUU COUNTING`")
    await e.edit("`WHAT KKKKKK LOVE LOOKS LIKE`")
    await e.edit("`HAIRBUUUT WARNAAA WARNII`")
    await e.edit("`LIKE TOOTBALL`")
    await e.edit("`IMUUUTTTTT LUCUUU`")
    await e.edit("`ALTHOUGH IT'S NOT TOO HIGH`")
    await e.edit("`GW GABUUTTTT`")
    await e.edit("`EMMMM THE BACOT`")
    await e.edit("`GABUTTTT WOI GABUT`")
    await e.edit("🙈🙈🙈🙈")
    await e.edit("🙉🙉🙉🙉")
    await e.edit("🙈🙈🙈🙈")
    await e.edit("🙉🙉🙉🙉")
    await e.edit("`CILUUUKKK BAAAAA`")
    await e.edit("🙉🙉🙉🙉")
    await e.edit("🐢                       🚶")
    await e.edit("🐢                      🚶")
    await e.edit("🐢                     🚶")
    await e.edit("🐢                    🚶")
    await e.edit("🐢                   🚶")
    await e.edit("🐢                  🚶")
    await e.edit("🐢                 🚶")
    await e.edit("🐢                🚶")
    await e.edit("🐢               🚶")
    await e.edit("🐢              🚶")
    await e.edit("🐢             🚶")
    await e.edit("🐢            🚶")
    await e.edit("🐢           🚶")
    await e.edit("🐢          🚶")
    await e.edit("🐢         🚶")
    await e.edit("🐢        🚶")
    await e.edit("🐢       🚶")
    await e.edit("🐢      🚶")
    await e.edit("🐢     🚶")
    await e.edit("🐢    🚶")
    await e.edit("🐢   🚶")
    await e.edit("🐢  🚶")
    await e.edit("🐢 🚶")
    await e.edit("🐢🚶")
    await asyncio.sleep(1)
    await e.edit("🚶🐢")
    await e.edit("🚶 🐢")
    await e.edit("🚶  🐢")
    await e.edit("🚶   🐢")
    await e.edit("🚶    🐢")
    await e.edit("🚶     🐢")
    await e.edit("🚶      🐢")
    await e.edit("🚶       🐢")
    await e.edit("🚶        🐢")
    await e.edit("🚶         🐢")
    await e.edit("🚶          🐢")
    await e.edit("🚶           🐢")
    await e.edit("🚶            🐢")
    await e.edit("🚶             🐢")
    await e.edit("🚶              🐢")
    await e.edit("🚶               🐢")
    await e.edit("🚶                🐢")
    await e.edit("🚶                 🐢")
    await e.edit("🚶                  🐢")
    await e.edit("🚶                   🐢")
    await e.edit("🚶                    🐢")
    await e.edit("🚶                     🐢")
    await e.edit("🚶                      🐢")
    await e.edit("🚶                       🐢")
    await e.edit("🚶                        🐢")
    await e.edit("🚶                         🐢")
    await e.edit("🚶                          🐢")
    await e.edit("🚶                           🐢")
    await e.edit("🚶                            🐢")
    await e.edit("🚶                             🐢")
    await e.edit("🚶                              🐢")
    await e.edit("🚶                               🐢")
    await e.edit("🚶                                🐢")
    await e.edit("🚶                                 🐢")
    await e.edit("`AHHH MANTAP`")
    await e.edit("🙉")
    await e.edit("🙈")
    await e.edit("🙉")
    await e.edit("🙈")
    await e.edit("🙉")
    await e.edit("😂")
    await e.edit("🐢                       🚶")
    await e.edit("🐢                      🚶")
    await e.edit("🐢                     🚶")
    await e.edit("🐢                    🚶")
    await e.edit("🐢                   🚶")
    await e.edit("🐢                  🚶")
    await e.edit("🐢                 🚶")
    await e.edit("🐢                🚶")
    await e.edit("🐢               🚶")
    await e.edit("🐢              🚶")
    await e.edit("🐢             🚶")
    await e.edit("🐢            🚶")
    await e.edit("🐢           🚶")
    await e.edit("🐢          🚶")
    await e.edit("🐢         🚶")
    await e.edit("🐢        🚶")
    await e.edit("🐢       🚶")
    await e.edit("🐢      🚶")
    await e.edit("🐢     🚶")
    await e.edit("🐢    🚶")
    await e.edit("🐢   🚶")
    await e.edit("🐢  🚶")
    await e.edit("🐢 🚶")
    await e.edit("🐢🚶")
    await asyncio.sleep(1)
    await e.edit("🚶🐢")
    await e.edit("🚶 🐢")
    await e.edit("🚶  🐢")
    await e.edit("🚶   🐢")
    await e.edit("🚶    🐢")
    await e.edit("🚶     🐢")
    await e.edit("🚶      🐢")
    await e.edit("🚶       🐢")
    await e.edit("🚶        🐢")
    await e.edit("🚶         🐢")
    await e.edit("🚶          🐢")
    await e.edit("🚶           🐢")
    await e.edit("🚶            🐢")
    await e.edit("🚶             🐢")
    await e.edit("🚶              🐢")
    await e.edit("🚶               🐢")
    await e.edit("🚶                🐢")
    await e.edit("🚶                 🐢")
    await e.edit("🚶                  🐢")
    await e.edit("🚶                   🐢")
    await e.edit("🚶                    🐢")
    await e.edit("🚶                     🐢")
    await e.edit("🚶                      🐢")
    await e.edit("🚶                       🐢")
    await e.edit("🚶                        🐢")
    await e.edit("🚶                         🐢")
    await e.edit("🚶                          🐢")
    await e.edit("🚶                           🐢")
    await e.edit("🚶                            🐢")
    await e.edit("🚶                             🐢")
    await e.edit("🚶                              🐢")
    await e.edit("🚶                               🐢")
    await e.edit("🚶                                🐢")
    await asyncio.sleep(1)
    await e.edit("🐢                       🚶")
    await e.edit("🐢                      🚶")
    await e.edit("🐢                     🚶")
    await e.edit("🐢                    🚶")
    await e.edit("🐢                   🚶")
    await e.edit("🐢                  🚶")
    await e.edit("🐢                 🚶")
    await e.edit("🐢                🚶")
    await e.edit("🐢               🚶")
    await e.edit("🐢              🚶")
    await e.edit("🐢             🚶")
    await e.edit("🐢            🚶")
    await e.edit("🐢           🚶")
    await e.edit("🐢          🚶")
    await e.edit("🐢         🚶")
    await e.edit("🐢        🚶")
    await e.edit("🐢       🚶")
    await e.edit("🐢      🚶")
    await e.edit("🐢     🚶")
    await e.edit("🐢    🚶")
    await e.edit("🐢   🚶")
    await e.edit("🐢  🚶")
    await e.edit("🐢 🚶")
    await e.edit("🐢🚶")
    await asyncio.sleep(1)
    await e.edit("🚶🐢")
    await e.edit("🚶 🐢")
    await e.edit("🚶  🐢")
    await e.edit("🚶   🐢")
    await e.edit("🚶    🐢")
    await e.edit("🚶     🐢")
    await e.edit("🚶      🐢")
    await e.edit("🚶       🐢")
    await e.edit("🚶        🐢")
    await e.edit("🚶         🐢")
    await e.edit("🚶          🐢")
    await e.edit("🚶           🐢")
    await e.edit("🚶            🐢")
    await e.edit("🚶             🐢")
    await e.edit("🚶              🐢")
    await e.edit("🚶               🐢")
    await e.edit("🚶                🐢")
    await e.edit("🚶                 🐢")
    await e.edit("🚶                  🐢")
    await e.edit("🚶                   🐢")
    await e.edit("🚶                    🐢")
    await e.edit("🚶                     🐢")
    await e.edit("🚶                      🐢")
    await e.edit("🚶                       🐢")
    await e.edit("🚶                        🐢")
    await e.edit("🚶                         🐢")
    await e.edit("🚶                          🐢")
    await e.edit("🚶                           🐢")
    await e.edit("🚶                            🐢")
    await e.edit("🚶                             🐢")
    await e.edit("🚶                              🐢")
    await e.edit("🚶                               🐢")
    await e.edit("🚶                                🐢")
    await e.edit("`GABUT`")


@Client.on_message(filters.command(["ular"], cmd) & filters.me)
async def ular(client: Client, message: Message):
    await edit_or_reply(
        message,
        "░░░░▓\n"
        "░░░▓▓\n"
        "░░█▓▓█\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░░░██▓▓██\n"
        "░░░░██▓▓██\n"
        "░░░██▓▓██\n"
        "░░██▓▓██\n"
        "░░██▓▓██\n"
        "░░██▓▓██\n"
        "░░██▓▓██\n"
        "░░██▓▓██\n"
        "░░██▓▓██\n"
        "░░░██▓▓███\n"
        "░░░░██▓▓████\n"
        "░░░░░██▓▓█████\n"
        "░░░░░░██▓▓██████\n"
        "░░░░░░███▓▓███████\n"
        "░░░░░████▓▓████████\n"
        "░░░░█████▓▓█████████\n"
        "░░░█████░░░█████●███\n"
        "░░████░░░░░░░███████\n"
        "░░███░░░░░░░░░██████\n"
        "░░██░░░░░░░░░░░████\n"
        "░░░░░░░░░░░░░░░░███\n"
        "░░░░░░░░░░░░░░░░░░░\n",
    )


@Client.on_message(filters.command(["helikopter", "heli"], cmd) & filters.me)
async def helikopter(client: Client, message: Message):
    await edit_or_reply(
        message,
        "▬▬▬.◙.▬▬▬ \n"
        "═▂▄▄▓▄▄▂ \n"
        "◢◤ █▀▀████▄▄▄▄◢◤ \n"
        "█▄ █ █▄ ███▀▀▀▀▀▀▀╬ \n"
        "◥█████◤ \n"
        "══╩══╩══ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ \n"
        "╬═╬ Hello Everything :) \n"
        "╬═╬☻/ \n"
        "╬═╬/▌ \n"
        "╬═╬/ \\ \n",
    )


@Client.on_message(filters.command("tembak", cmd) & filters.me)
async def dornembak(client: Client, message: Message):
    await edit_or_reply(
        message,
        "_/﹋\\_\n" "(҂`_´)\n" "<,︻╦╤─ ҉\n" r"_/﹋\_" "\n**Do you want to be my girlfriend??!**",
    )


@Client.on_message(filters.command("bundir", cmd) & filters.me)
async def ngebundir(client: Client, message: Message):
    await edit_or_reply(
        message,
        "`Drugs Everything...`          \n　　　　　|"
        "\n　　　　　| \n"
        "　　　　　| \n"
        "　　　　　| \n"
        "　　　　　| \n"
        "　　　　　| \n"
        "　　　　　| \n"
        "　　　　　| \n"
        "　／￣￣＼| \n"
        "＜ ´･ 　　 |＼ \n"
        "　|　３　 | 丶＼ \n"
        "＜ 、･　　|　　＼ \n"
        "　＼＿＿／∪ _ ∪) \n"
        "　　　　　 Ｕ Ｕ\n",
    )

@Client.on_message(filters.command(["ange", "sange"], cmd) & filters.me)
async def kocok(client: Client, message: Message):
    e = await edit_or_reply(message, "Ayanggg 😖")
    await asyncio.sleep(2)
    await e.edit("Aku Ange 😫")
    await asyncio.sleep(2)
    await e.edit("Come on Pisces Yang 🤤")


@Client.on_message(filters.command(["lipkol", "sleepcall"], cmd) & filters.me)
async def lipkol(client: Client, message: Message):
    e = await edit_or_reply(message, "Ayanggg 😖")
    await asyncio.sleep(2)
    await e.edit("Kangeeen 👉👈")
    await asyncio.sleep(2)
    await e.edit("Pinkie's sleeping bag is Yang 🥺👉👈")
    

@Client.on_message(filters.command(["nakal", "bandel"], cmd) & filters.me)
async def nakal(client: Client, message: Message):
    e = await edit_or_reply(message, "Ayanggg ih🥺")
    await asyncio.sleep(2)
    await e.edit("Very naughty bro 🥺")
    await asyncio.sleep(2)
    await e.edit("I don't like Ayang 😠")
    await asyncio.sleep(2)
    await e.edit("Anyway, I don't like Ig 😠")


@Client.on_message(filters.command(["awk", "awikwok"], cmd) & filters.me)
async def awikwok(client: Client, message: Message):
    await edit_or_reply(
        message,
        "────██──────▀▀▀██\n"
        "──▄▀█▄▄▄─────▄▀█▄▄▄\n"
        "▄▀──█▄▄──────█─█▄▄\n"
        "─▄▄▄▀──▀▄───▄▄▄▀──▀▄\n"
        "─▀───────▀▀─▀───────▀▀\n`Awkwokwokwok..`",
    )


@Client.on_message(filters.command("y", cmd) & filters.me)
async def ysaja(client: Client, message: Message):
    await edit_or_reply(
        message,
        "‡‡‡‡‡‡‡‡‡‡‡‡▄▄▄▄\n"
        "‡‡‡‡‡‡‡‡‡‡‡█‡‡‡‡█\n"
        "‡‡‡‡‡‡‡‡‡‡‡█‡‡‡‡█\n"
        "‡‡‡‡‡‡‡‡‡‡█‡‡‡‡‡█\n"
        "‡‡‡‡‡‡‡‡‡█‡‡‡‡‡‡█\n"
        "██████▄▄█‡‡‡‡‡‡████████▄\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█████‡‡‡‡‡‡‡‡‡‡‡‡██\n"
        "█████‡‡‡‡‡‡‡██████████\n",
    )


@Client.on_message(filters.command("tank", cmd) & filters.me)
async def tank(client: Client, message: Message):
    await edit_or_reply(
        message,
        "█۞███████]▄▄▄▄▄▄▄▄▄▄▃ \n"
        "▂▄▅█████████▅▄▃▂…\n"
        "[███████████████████]\n"
        "◥⊙▲⊙▲⊙▲⊙▲⊙▲⊙▲⊙◤\n",
    )


@Client.on_message(filters.command("babi", cmd) & filters.me)
async def babi(client: Client, message: Message):
    await edit_or_reply(
        message,
        "┈┈┏━╮╭━┓┈╭━━━━╮\n"
        "┈┈┃┏┗┛┓┃╭┫Ngok ┃\n"
        "┈┈╰┓▋▋┏╯╯╰━━━━╯\n"
        "┈╭━┻╮╲┗━━━━╮╭╮┈\n"
        "┈┃▎▎┃╲╲╲╲╲╲┣━╯┈\n"
        "┈╰━┳┻▅╯╲╲╲╲┃┈┈┈\n"
        "┈┈┈╰━┳┓┏┳┓┏╯┈┈┈\n"
        "┈┈┈┈┈┗┻┛┗┻┛┈┈┈┈\n",
    )


@Client.on_message(filters.command(["ajg", "anjg"], cmd) & filters.me)
async def anjg(client: Client, message: Message):
    await edit_or_reply(
        message,
        "╥━━━━━━━━╭━━╮━━┳\n"
        "╢╭╮╭━━━━━┫┃▋▋━▅┣\n"
        "╢┃╰┫┈┈┈┈┈┃┃┈┈╰┫┣\n"
        "╢╰━┫┈┈┈┈┈╰╯╰┳━╯┣\n"
        "╢┊┊┃┏┳┳━━┓┏┳┫┊┊┣\n"
        "╨━━┗┛┗┛━━┗┛┗┛━━┻\n",
    )


@Client.on_message(filters.command("nah", cmd) & filters.me)
async def nahlove(client: Client, message: Message):
    typew = await edit_or_reply(
        message, "`\n(\\_/)`" "`\n(●_●)`" "`\n />💖 *This is for you`"
    )
    await asyncio.sleep(2)
    await typew.edit("`\n(\\_/)`" "`\n(●_●)`" "`\n💖<\\  *tap IB OO that one`")


@Client.on_message(filters.command("santet", cmd) & filters.me)
async def santet(client: Client, message: Message):
    typew = await edit_or_reply(message, "`Activates Witchcraft Commands Online....`")
    await asyncio.sleep(2)
    await typew.edit("`Search for This Person's Name...`")
    await asyncio.sleep(1)
    await typew.edit("`Online Witchcraft Performed Immediately`")
    await asyncio.sleep(1)
    await typew.edit("0%")
    number = 1
    await typew.edit(str(number) + "%   ▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████████")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████████▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████████▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████████▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████████▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████████▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████████")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████████▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████████▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████████▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████████▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████████▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████████")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████████▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████████▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████████▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████████▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████████▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████████")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████████▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████████▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████████▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████████▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████████▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████████████")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████████████▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████████████▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████████████▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████████████▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   █████████████▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████████████")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████████████▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████████████▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████████████▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████████████▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ██████████████▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████████████")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████████████▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████████████▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████████████▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████████████▊")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ███████████████▉")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████████████")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████████████▎")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████████████▍")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████████████▌")
    number += 1
    await asyncio.sleep(0.03)
    await typew.edit(str(number) + "%   ████████████████▌")
    await asyncio.sleep(1)
    await typew.edit("**Target Successfully Scammed Online 🥴**")

@Client.on_message(filters.command(["ror", "ah"], cmd) & filters.me)
async def hearts(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 1.5)
    await message.edit("Rooor")
    await asyncio.sleep(1)
    await message.edit("Rooor Aahh")
    await asyncio.sleep(1)
    await message.edit("Rooor Aahh Aahh")
    await asyncio.sleep(1)
    await message.edit("Rooor Aahh Aahh Aahh")


add_command_help(
    "─╼⃝𖠁 ᴀɴɪᴍᴀᴛɪᴏɴ",
    [
        ["fuck", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴛʜᴇ ᴍɪᴅᴅʟᴇ ғɪɴɢᴇʀ ᴀɴɪᴍᴀᴛɪᴏɴ."],
        ["ror", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴀ ʀᴏʀ ᴀɴɪᴍᴀᴛɪᴏɴ."],
        ["dino", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴀɴ ᴀɴɪᴍᴀᴛɪᴏɴ ᴏғ ʙᴇɪɴɢ ᴄʜᴀꜱᴇᴅ ʙʏ ᴀ ᴅɪɴᴏ."],
        ["santet", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴀɴ ᴏɴʟɪɴᴇ ʙʟᴀᴄᴋᴍᴀɪʟ ᴀɴɪᴍᴀᴛɪᴏɴ."],
        ["gabut", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴛʜᴇ ʟᴀᴛᴄʜ ᴀɴɪᴍᴀᴛɪᴏɴ."],
        ["sayang", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴀɴɪᴍᴀᴛɪᴏɴ ᴅᴀʀʟɪɴɢ."],
        ["hack", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴀ ғᴀᴋᴇ ᴋɪᴄᴋɪɴɢ ᴀɴɪᴍᴀᴛɪᴏɴ."],
        ["bomb", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴛʜᴇ Bᴏᴍʙ ᴀɴɪᴍᴀᴛɪᴏɴ."],
        ["brain", "Tᴏ ᴅɪꜱᴘʟᴀʏ Bʀᴀɪɴ ᴀɴɪᴍᴀᴛɪᴏɴ 🧠."],
        ["kontol", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴅɪᴄᴋ ᴀʀᴛ."],
        ["penis", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴘᴇɴɪꜱ ᴀʀᴛ ᴡɪᴛʜ ᴇᴍᴏɪɪꜱ."],
        ["tembak","Tᴏ ᴅɪꜱᴘʟᴀʏ ꜱʜᴏᴏᴛɪɴɢ ᴀʀᴛ."],
        ["bundir", "Tᴏ ᴅɪꜱᴘʟᴀʏ ʙᴜɴᴅɪʀ ᴀʀᴛ."],
        ["helikopter", "Tᴏ ᴅɪꜱᴘʟᴀʏ ʜᴇʟɪᴄᴏᴘᴛᴇʀ ᴀʀᴛ."],
        ["y", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴀʀᴛ ʏ ꜱɪ."],
        ["awk", "Fᴏʀ ᴅɪꜱᴘʟᴀʏꜱ ᴀʀᴛ ᴀᴏᴡᴋᴀᴏᴡᴋᴀᴏᴡᴋ."],
        ["ange", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴀʀᴛ ᴀɴɢᴇ."],
        ["lipkol", "Tᴏ ᴅɪꜱᴘʟᴀʏ Aʏᴀɴɢ'ꜱ ᴀʀᴛ."],
        ["nakal", "Tᴏ ᴅɪꜱᴘʟᴀʏ ɴᴀᴜɢʜᴛʏ ᴀʀᴛ."],
        ["nah", "Tᴏ ꜱʜᴏᴡ ᴀʀᴛ ʟᴏᴠᴇ."],
        ["ajg", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴅᴏɢ ᴀʀᴛ."],
        ["babi", "Tᴏ ᴅɪꜱᴘʟᴀʏ ᴘɪɢ ᴀʀᴛ."],
        ["hug", "Tᴏ ɢᴇᴛ A Hᴜɢ Gɪғꜱ ᴀɴɪᴍᴇ."],
        ["hmm", "Gᴇᴛ Rᴀɴᴅᴏᴍ Hᴍᴍᴍ."],
        ["wink", "Tᴏ Gᴇᴛ A Wɪɴᴋɪɴɢ Gɪғꜱ."],
        ["love", "Tᴏ Pʀᴏᴘᴏꜱᴇ Sᴏᴍᴇᴏɴᴇ."],
        ["loveyou", "Iᴛ Wɪʟʟ Sᴇɴᴅ Rᴀɴᴅᴏᴍ Eᴍᴏɪɪꜱ."],
        [
            "pat",
            "Tᴏ ɢᴇᴛ ᴀ ᴘᴀᴛ ɢɪғꜱ",
        ],
        [
            "pikachu",
            "ᴛᴏ ɢᴇᴛ ᴀ Pɪᴋᴀᴄʜᴜ Gɪғꜱ",
        ],
        [
            "kill",
            "Tᴏ ᴋɪʟʟ Sᴏᴍᴇᴏɴᴇ ʀᴀɴᴅᴏᴍʟʏ",
        ],
        [
            "wtf",
            "Wᴛғ ᴀɴɪᴍᴀᴛɪᴏɴ",
        ],
        [
            "ding",
            "Gᴇᴛ Dᴏɴɢ",
        ],
        [
            "ganstar",
            "Aɴɪᴍᴀᴛɪᴏɴ Gᴀɴɢꜱᴛᴇʀ",
        ],
        [
            "charge",
            " Tᴇꜱʟᴀ ᴀɴɪᴍᴀᴛɪᴏɴ ᴄʜᴀʀɢɪɴɢ",
        ],
    ],
) 
