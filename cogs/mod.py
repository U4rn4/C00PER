import discord
from discord.ext import commands
from discord import app_commands

class mod(commands.Cog):
    
    def __init__(self , bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self,ctx, member:discord.Member, *, reason=None):
        await ctx.message.delete()
        async with ctx.typing():
            await ctx.guild.ban(member, reason=reason)
            embed = discord.Embed(color=discord.Color.blue(), title="",description="")
            if reason == None:
                embed.add_field(name="Banned", value=f"User {member} has been banned") 
                await ctx.send(embed=embed)
            else: 
                embed.add_field(name="Banned", value=f"User {member} has been banned for {reason}")
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self,ctx, member:discord.Member, *, reason=None):
        async with ctx.typing():
            await ctx.guild.kick(member, reason=reason)
            await ctx.message.delete()
            if reason == None: 
                
                embed = discord.Embed(color=discord.Color.blue(), title="",description="")
                embed.add_field(name="Kick", value=f"User {member} has been kicked")
                await ctx.send(embed=embed)
            else: 
                
                embed = discord.Embed(color=discord.Color.blue(), title="",description="")
                embed.add_field(name="Kick", value=f"User {member} has been kick for {reason}")
                await ctx.send(embed=embed)
 
async def setup(bot):
    await bot.add_cog(mod(bot))