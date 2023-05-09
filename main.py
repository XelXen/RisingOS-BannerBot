import pyrogram
from PIL import Image, ImageDraw, ImageFont
import os
from time import sleep

NAME = os.environ["BOT_NAME"]
API_ID = int(os.environ["BOT_API_ID"])
API_HASH = os.environ["BOT_API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
AUTH_USERS = [5724838961, 5186511686]

app = pyrogram.Client(name=NAME, api_id=API_ID, bot_token=BOT_TOKEN, api_hash=API_HASH, in_memory=True)

sleep(5)
print("Bot Started!\n")

def banner_gen(maintainer, codename):
    with Image.open(f'template.png') as image:
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("template.ttf", 22)

        a, b, c, d = draw.textbbox((0, 0), f"is up for <{codename} by {maintainer}> :D", font)
        text_width = c - a
        if text_width > 610:
            font = ImageFont.truetype("template.ttf", 18)

        draw.text((118, 149), f"is up for <{codename} by {maintainer}> :D", "#A6A6A6", font)
        image.save(f'{codename}.png')

@app.on_message(pyrogram.filters.command(["start"]))
def start(client, message):
    if message.from_user.id not in AUTH_USERS:
        message.reply_text("You are not authorized to use this bot!")
        return
    
    message.reply_text(f"Hi, I'm {NAME}. I can make banners for risingOS. Just send me a message such as /banner maintainer codename\n\nFor co-maintainers, use /banner co-maintainer co-maintainer codename\n\nYou can use your name, username or user ID as maintainer/co-maintainer")

@app.on_message(pyrogram.filters.command(["banner"]))
def banner(client, message):
    if message.from_user.id not in AUTH_USERS:
        message.reply_text("You are not authorized to use this bot!")
        return
    
    banner_reply = message.reply_text("Generating...")

    if len(message.command) == 3:
        maintainer = message.command[1]
        codename = message.command[2]

        try:
            banner_gen(maintainer, codename)
            message.reply_document(f"{codename}.png")
            banner_reply.edit("Done!")
            os.remove(f"{codename}.png")
        except:
            banner_reply.edit("Error! Please check your command.")

    elif len(message.command) == 4:
        maintainer = message.command[1] + " x " + message.command[2]
        codename = message.command[3]

        try:
            banner_gen(maintainer, codename)
            message.reply_document(f"{codename}.png")
            banner_reply.edit("Done!")
            os.remove(f"{codename}.png")
        except:
            banner_reply.edit("Error! Please check your command.")

    else:
        banner_reply.edit("Invalid command! Use /start to see how to use me.")

app.run()
