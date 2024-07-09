import discord
from discord.ext import commands

class generic(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
    
    
    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You must be in a voice channel to run this command")

    @commands.command()
    async def leave(self,ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send("Voice channel left")
        else:
            await ctx.send("You must be in a voice channel to run this command")

    @commands.command()
    async def say(self,ctx, *, text: str):
        await ctx.message.delete()
        await ctx.send(text)

    @commands.command()
    async def hello(self, ctx):
        embed = discord.Embed(color=discord.Color.blue(), title="",description="")
        embed.add_field(name ="Hello!", value ='I am C00per, I am a bot created by U4rn4, I am here to help you with anything you need. \nWrite .help to see the commands I have available. \nMy prefix is "." ')
        await ctx.reply(embed=embed)

    @commands.command()
    async def hi(self, ctx):
        embed = discord.Embed(color=discord.Color.blue(), title="",description="")
        embed.add_field(name ="Hello!", value ='I am C00per, I am a bot created by U4rn4, I am here to help you with anything you need. \nWrite .help to see the commands I have available. \nMy prefix is "." ')
        await ctx.reply(embed=embed)
    
    # Evento que indica que el bot está listo
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot listo. Conectado como {self.bot.user}')

async def setup(bot):
    await bot.add_cog(generic(bot))