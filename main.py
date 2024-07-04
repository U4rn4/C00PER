import discord
from discord.ext import commands
from apikeys import *
import yt_dlp  
import asyncio # For the bot tokken and other private things
import os

# Inicializa los intents
intents = discord.Intents.default()
intents.message_content = True  # Necesario para recibir el contenido de los mensajes
intents.voice_states = True

# Inicializa el bot con el prefijo '!' y los intents
bot = commands.Bot(command_prefix='.', intents=intents)

# Archivo donde se almacenará el valor del contador
COUNTER_FILE = 'counter.txt'

# Función para leer el contador del archivo
def read_counter():
    try:
        with open(COUNTER_FILE, 'r') as file:
            return int(file.read())
    except FileNotFoundError: 
        return 0

# Función para escribir el contador en el archivo
def write_counter(counter):
    with open(COUNTER_FILE, 'w') as file:
        file.write(str(counter))

# Comando para incrementar el contador
@bot.command()
async def count(ctx):
    counter = read_counter() + 1
    write_counter(counter)
    await ctx.send(counter)

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You must be in a voice channel to run this command")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Voice channel left")
    else:
        await ctx.send("You must be in a voice channel to run this command")

@bot.command()
async def max(ctx):
    await ctx.send("El max es un friki con nombre de perro")

@bot.command()
async def say(ctx, *, text: str):
    await ctx.message.delete()
    await ctx.send(text)


# Evento que indica que el bot está listo
@bot.event
async def on_ready():
    print(f'Bot listo. Conectado como {bot.user}')

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(BOTTOKEN) 

asyncio.run(main())
