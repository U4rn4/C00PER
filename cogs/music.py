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
    async def play(self, ctx,*,search = None):

        embed = discord.Embed(color=discord.Color.blue(), title="",description="")
        if search==None and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            embed.add_field(name ="", value ="Song resumed")
            await ctx.reply(embed=embed) 
            return
        elif search == None:
            embed.add_field(name ="", value ="You must send a song with this command")
            await ctx.reply(embed=embed)
            return
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            embed.add_field(name ="", value ="You must be in a voice channel")
            return await ctx.reply(embed=embed) 
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
                if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                    embed = discord.Embed(color=discord.Color.blue(), title="",description="")
                    embed.add_field(name ="", value =f"Added to queue: {title}")
                    await ctx.reply(embed=embed)
            if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                await self.play_next(ctx)

    async def play_next(self, ctx):
            if self.queues:
                url, title = self.queues.pop(0)
                source = await discord.FFmpegOpusAudio.from_probe(url, **ffmpeg_options)
                ctx.voice_client.play(source, after = lambda _: self.bot.loop.create_task(self.play_next(ctx)))
                embed = discord.Embed(color=discord.Color.blue(), title="",description="")
                embed.add_field(name ="", value =f"Now playing {title}")
                await ctx.send(embed=embed)
            
    @commands.command()
    async def skip(self, ctx):
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                embed = discord.Embed(color=discord.Color.blue(), title="",description="")
                embed.add_field(name ="", value ="Skipped")
                await ctx.reply(embed=embed)
            elif ctx.voice_client:
                embed = discord.Embed(color=discord.Color.blue(), title="",description="")
                embed.add_field(name ="", value ="There is no song to skip")
                await ctx.reply(embed=embed)
            else:
                embed = discord.Embed(color=discord.Color.blue(), title="",description="")
                embed.add_field(name ="", value ="You must be in a voice channel with music to run this command")
                await ctx.reply(embed=embed)


    @commands.command(name='pause', help='Pausa la canción')
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            embed = discord.Embed(color=discord.Color.blue(), title="",description="")
            embed.add_field(name ="", value ="Song paused")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(color=discord.Color.blue(), title="",description="")
            embed.add_field(name ="", value ="No song is playing")
            await ctx.reply(embed=embed)

    @commands.command(name='resume', help='Reanuda la canción')
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            embed = discord.Embed(color=discord.Color.blue(), title="",description="")
            embed.add_field(name ="", value ="Song resumed")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(color=discord.Color.blue(), title="",description="")
            embed.add_field(name ="", value ="The song is not paused")
            await ctx.reply(embed=embed)

    @commands.command(name='stop', help='Detiene la canción')
    async def stop(self, ctx):
        self.queues.clear()
        ctx.voice_client.stop()
        embed = discord.Embed(color=discord.Color.blue(), title="",description="")
        embed.add_field(name ="", value ="Bot Stopped")
        await ctx.reply(embed=embed)

    @commands.command()
    async def queue(self, ctx):
        async with ctx.typing():
            if not ctx.author.voice: 
                embed = discord.Embed(color=discord.Color.blue(), title="",description="")
                embed.add_field(name="You must be in a voice channel", value="")
                await ctx.reply(embed=embed)
            elif not ctx.voice_client:
                embed = discord.Embed(color=discord.Color.blue(), title="",description="")
                embed.add_field(name="The bot is not in a voice channel", value="")
                await ctx.reply(embed=embed)
            elif self.queues:
                embed = discord.Embed(color=discord.Color.blue(), title="",description="")
                message = ""
                for i in self.queues:
                    message += i[1] + "\n"
                embed.add_field(name="This is the queue:", value=message)
                await ctx.reply(embed = embed)
            else:
                embed = discord.Embed(color=discord.Color.blue(), title="",description="")
                embed.add_field(name="The queue is empty", value="")
                await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(music(bot))

