import discord
from discord.ext import commands
import yt_dlp  
import asyncio # For the bot tokken and other private things

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

class music(commands.Cog):

    queues = []

    def __init__(self, bot):
       self.bot = bot 


    @commands.command()
    async def play(self, ctx,*,search):
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
                self.queues.append((url, title))
                if ctx.voice_client.is_playing() or ctx.voice_client.is_paused(): await ctx.send(f"Added to queue: {title}")
            if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                await self.play_next(ctx)

    async def play_next(self, ctx):
            if self.queues:
                url, title = self.queues.pop(0)
                source = await discord.FFmpegOpusAudio.from_probe(url, **ffmpeg_options)
                ctx.voice_client.play(source, after = lambda _: self.bot.loop.create_task(self.play_next(ctx)))
                await ctx.send(f"Now playing {title}")
            
    @commands.command()
    async def skip(self, ctx):
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await ctx.send("Skipped")


    @commands.command(name='pause', help='Pausa la canción')
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Song paused")
        else:
            await ctx.send("No song is playing")

    @commands.command(name='resume', help='Reanuda la canción')
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Song resumed")
        else:
            await ctx.send("The song is not paused")

    @commands.command(name='stop', help='Detiene la canción')
    async def stop(self, ctx):
        self.queues.clear()
        ctx.voice_client.stop()
        await ctx.send("Bot stopped")

    @commands.command()
    async def queue(self, ctx):
        async with ctx.typing():
            if self.queues:
                message = "### This is the queue: \n```"
                for i in self.queues:
                    message +=  i[1] + "\n"
                message += "```"
                await ctx.send(message)
            else:
                await ctx.send("### The queue is empty")

async def setup(bot):
    await bot.add_cog(music(bot))