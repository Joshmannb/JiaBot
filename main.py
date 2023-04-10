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
    option_enum = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
    db = build_db(file_name)
    candidate = random.sample(db.keys(), 16) # 10題，每題4個選項
    question_num = len(candidate)//4
    correct_count = 0

    await ctx.respond("Choose the correct definition, a, b, c or d.")
    for i in range(question_num):
        option_list = [db[candidate[i*4]], db[candidate[i*4+1]], db[candidate[i*4+2]], db[candidate[i*4+3]]]
        random.shuffle(option_list)

        question = candidate[i*4] + " means" + "\n" \
                   + "a) " + option_list[0] + "\nb) " + option_list[1] + "\nc) " + option_list[2] + "\nd) " + option_list[3]
        await ctx.respond(question)

        try:
            # 要使用回覆功能才會讀到
            event = await ctx.bot.wait_for(hikari.MessageEvent, timeout=20, predicate=lambda e: e.content != None)
            # print(event.content)
        except asyncio.TimeoutError:
            await ctx.respond("Timeout!!")
        else:
            ans = event.content
            if ans in option_enum.keys():
                if option_list[option_enum[ans]] == db[candidate[i*4]]:
                    await ctx.respond("Nice Job!!")
                    correct_count += 1
                else:
                    await ctx.respond("You are wrong, the answer is ---> " + db[candidate[i*4]])
            else:
                await ctx.respond("Not valid answer")
    
    comment = ""
    if correct_count <= question_num//4:
        comment = "You are suck!"
    elif correct_count >= (question_num*3)//4:
        comment = "You are great!"
    else:
        comment = "You are not bad~"
    
    await ctx.respond(comment + "\nYour final score is " + str(correct_count) + "/" + str(question_num))

if __name__ == "__main__":
    bot.run()