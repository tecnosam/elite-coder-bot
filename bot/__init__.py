# bot.py
import asyncio
import os

import discord
from dotenv import load_dotenv

from bot.events import news_aggregator

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(news_aggregator.send_to_channel(client), loop)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    if ('asimo:' == msg[:6]):
        await message.channel.send( 
                "Hello. the admin is still working on my friendly AI he'll message you on updates and even more cool commands. Thanks"
        )
    
    if ('!news' == msg[:5]):
        await message.channel.send("Working on the news")
