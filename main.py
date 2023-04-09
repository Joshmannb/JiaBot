import os

import dotenv
import hikari

dotenv.load_dotenv()

bot = hikari.GatewayBot(
    os.environ["BOT_TOKEN"],
    intents=hikari.Intents.ALL_MESSAGES,
)


@bot.listen()
async def on_message_create(event: hikari.GuildMessageCreateEvent) -> None:
    if not event.is_human or not event.content:
        return

    me = bot.get_me()
    if not me:
        return

    if event.content == f"<@{me.id}> ping":
        await event.message.respond(f"Pong! {bot.heartbeat_latency * 1000:.0f}ms.")


if __name__ == "__main__":
    bot.run()