import discord
from discord.ext import commands
from apikeys import *
import yt_dlp  
import asyncio # For the bot tokken and other private things

# Inicializa los intents
intents = discord.Intents.default()
intents.message_content = True  # Necesario para recibir el contenido de los mensajes
intents.voice_states = True

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn',  # Esta opción deshabilita la salida de video, es adecuada para reproducción de audio
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'

}

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

# Suppress noise about console usage from errors
# Configuración de opciones para yt_dlp

queues = []

@bot.command()
async def play(ctx,*,search):
    voice_channel = ctx.author.voice.channel if ctx.author.voice else None
    if not voice_channel:
           return await ctx.send("You must be in a voice channel")
    if not ctx.voice_client:
       await voice_channel.connect()

    async with ctx.typing():
        
        with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
            if "youtube.com" in search or "youtu.be" in search: info = ydl.extract_info(search, download=False)
            else: info = ydl.extract_info(f"ytsearch:{search}", download=False)
            if "entries" in info:
                info = info["entries"][0]
            url = info["url"]
            title = info["title"]   
            queues.append((url, title))
            if ctx.voice_client.is_playing(): await ctx.send(f"Added to queue: {title}")
        if not ctx.voice_client.is_playing():
            await play_next(ctx)

async def play_next(ctx):
        if queues:
            url, title = queues.pop(0)
            source = await discord.FFmpegOpusAudio.from_probe(url, **ffmpeg_options)
            ctx.voice_client.play(source, after = lambda _: bot.loop.create_task(play_next(ctx)))
            await ctx.send(f"Now playing {title}")
        
@bot.command()
async def skip(ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped")


@bot.command(name='pause', help='Pausa la canción')
async def pause(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Song paused")
    else:
        await ctx.send("No song is playing")

@bot.command(name='resume', help='Reanuda la canción')
async def resume(ctx):
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Song resumed")
    else:
        await ctx.send("The song is not paused")

@bot.command(name='stop', help='Detiene la canción')
async def stop(ctx):
    queues.clear()
    ctx.voice_client.stop()
    await ctx.send("Bot stopped")

@bot.command()
async def queue(ctx):
    async with ctx.typing():
        message = "### This is the queue: \n```"
        for i in queues:
            message +=  i[1] + "\n"
        message += "```"
    await ctx.send(message)

# Evento que indica que el bot está listo
@bot.event
async def on_ready():
    print(f'Bot listo. Conectado como {bot.user}')

#  token del bot
bot.run(BOTTOKEN) 