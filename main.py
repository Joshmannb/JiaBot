# This example requires the 'message_content' intent.

import discord
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('meow!')
        
    if (message.content) == '!roll':
        await message.channel.send(str(random.randint(0, 100)))

client.run('MTA5MjQyMzg2NTU1NDE3Mzk4Mg.GBL3n9.fb-FJL_UahyoosH-hXe_u3enFJvUtKJHIFcous')
