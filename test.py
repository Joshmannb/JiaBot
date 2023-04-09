import os
from typing import Optional
import random

import dotenv
import hikari
import lightbulb
from hikari import Intents
import asyncio

ANIMALS = {
    "Bird": "🐦",
    "Cat": "🐱",
    "Dog": "🐶",
    "Fox": "🦊",
    "Kangaroo": "🦘",
    "Koala": "🐨",
    "Panda": "🐼",
    "Raccoon": "🦝",
    "Red Panda": "🐼", 
}

INTENTS = Intents.GUILD_MEMBERS | Intents.GUILDS

bot = lightbulb.BotApp(
    os.environ["BOT_TOKEN"],
    intents=hikari.Intents.ALL_MESSAGES,
    banner=None,
)

@bot.listen()
async def on_starting(_: hikari.StartingEvent) -> None:
    bot.d.client_session = aiohttp.ClientSession()

@bot.listen()
async def on_stopping(_: hikari.StoppingEvent) -> None:
    await bot.d.client_session.close()

@bot.command
@lightbulb.command("animal", "Get a fact & picture of a cute animal :3")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def animal_subcommand(ctx: lightbulb.SlashContext) -> None:
    select_menu = (
        ctx.bot.rest.build_message_action_row()
        .add_select_menu(hikari.ComponentType.TEXT_SELECT_MENU, "animal_select")
        .set_placeholder("Pick an animal")
    )

    for name, emoji in ANIMALS.items():
        select_menu.add_option(
            name,  # the label, which users see
            name.lower().replace(" ", "_"),  # the value, which is used by us later
        ).set_emoji(emoji).add_to_menu()

    resp = await ctx.respond(
        "Pick an animal from the dropdown :3",
        component=select_menu.add_to_container(),
    )
    msg = await resp.message()

    try:
        event = await ctx.bot.wait_for(
            hikari.InteractionCreateEvent,
            timeout=60,
            predicate=lambda e: isinstance(e.interaction, hikari.ComponentInteraction)
            and e.interaction.user.id == ctx.author.id
            and e.interaction.message.id == msg.id
            and e.interaction.component_type == hikari.ComponentType.TEXT_SELECT_MENU,
        )
    except asyncio.TimeoutError:
        await msg.edit("The menu timed out :c", components=[])
    else:
        animal = event.interaction.values[0]
        async with ctx.bot.d.client_session.get(
            f"https://some-random-api.ml/animal/{animal}"
        ) as res:
            if not res.ok:
                await msg.edit(f"API returned a {res.status} status :c", components=[])
                return

            data = await res.json()
            embed = hikari.Embed(description=data["fact"], colour=0x3B9DFF)
            embed.set_image(data["image"])

            animal = animal.replace("_", " ")

            await msg.edit(f"Here's a {animal} for you! :3", embed=embed, components=[])

if __name__ == "__main__":
    bot.run()