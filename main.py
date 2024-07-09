import discord
from discord.ext import commands
from apikeys import *
import asyncio # For the bot tokken and other private things
import os

# Inicializa los intents
intents = discord.Intents.default()
intents.message_content = True  # Necesario para recibir el contenido de los mensajes
intents.voice_states = True
intents.guilds = True

vprefix = "."

# Inicializa el bot con el prefijo '!' y los intents
bot = commands.Bot(command_prefix=vprefix, intents=intents)


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(BOTTOKEN) 

asyncio.run(main())
