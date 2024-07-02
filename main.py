import discord
from discord.ext import commands
from apikeys import *
import yt_dlp as youtube_dl  # Cambia youtube_dl por yt_dlp
import asyncio

# Inicializa los intents
intents = discord.Intents.default()
intents.message_content = True  # Necesario para recibir el contenido de los mensajes

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

@bot.command(pass_context = True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You must be in a voice channel to run this command")

@bot.command(pass_context = True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Voice channel left")
    else:
        await ctx.send("You must be in a voice channel to run this command")


# Suppress noise about console usage from errors
# Configuración de opciones para yt_dlp
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
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


@bot.command(name='play', help='Reproduce una canción desde YouTube')
async def play(ctx, url):
    if not ctx.voice_client:  # Si el bot no está en un canal de voz, se une
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("¡Debes estar en un canal de voz para reproducir música!")
            return

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print('Error en el reproductor: %s' % e) if e else None)

    await ctx.send('Reproduciendo: {}'.format(player.title))

@bot.command(name='pause', help='Pausa la canción')
async def pause(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Canción pausada")
    else:
        await ctx.send("No hay ninguna canción reproduciéndose")

@bot.command(name='resume', help='Reanuda la canción')
async def resume(ctx):
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Canción reanudada")
    else:
        await ctx.send("La canción no está pausada")

@bot.command(name='stop', help='Detiene la canción')
async def stop(ctx):
    ctx.voice_client.stop()
    await ctx.send("Canción detenida")


# Evento que indica que el bot está listo
@bot.event
async def on_ready():
    print(f'Bot listo. Conectado como {bot.user}')

#  token del bot
bot.run(BOTTOKEN) 