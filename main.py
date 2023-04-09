import os
from typing import Optional
import random
import aiohttp

import dotenv
import hikari
import lightbulb
from hikari import Intents
import asyncio

from util_read_csv import build_db

dotenv.load_dotenv()

def test_N5():
    file_name = 'N5_Kanji.csv'
    db = build_db(file_name)
    candidate = random.sample(db.keys(), 10)

INTENTS = Intents.GUILD_MEMBERS | Intents.GUILDS

bot = lightbulb.BotApp(
    os.environ["BOT_TOKEN"],
    intents=hikari.Intents.ALL_MESSAGES,
    banner=None,
)

@bot.command
@lightbulb.command("test", description="Do the N5 test.")
@lightbulb.implements(lightbulb.SlashCommand)
async def test(ctx: lightbulb.SlashContext) -> None:
    file_name = 'N5_Kanji.csv'
    db = build_db(file_name)
    candidate = random.sample(db.keys(), 10)
    question = "Please answer following question." + "\n" + candidate[0]
    await ctx.respond(question)

    # 要使用回覆功能才會讀到
    event = await ctx.bot.wait_for(hikari.MessageEvent, timeout=60, predicate=lambda e: e.content != None)
    print(event.content)

    


if __name__ == "__main__":
    bot.run()