import discord
from discord.ext import commands
from discord import app_commands
import datetime

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
    """"
    # TODO 
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member, *,reason=None ):
        try:
            async with ctx.typing():
                banned_users =  ctx.guild.bans()

                async for banentry in banned_users:
                    user = banentry.user
                    if (user.name) == (member):
                        await ctx.guild.unban(user,reason)
                        embed = discord.Embed(color=discord.Color.blue(), title="",description="")
                        embed.add_field(name="Unbanned", value=f"The user {user} has been unbanned")
                        await ctx.reply(embed=embed)
                        return
                ctx.send("The user was not found on the banned list")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
        except:
            await ctx.send("error")

    """

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

    """
    @commands.command()
    @commands.has_permissions(moderate_members=True)  # Ensure the command user has the correct permissions
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason: str = None):
        try:
            duration = datetime.timedelta(minutes=minutes)
            await member.timeout_for(duration, reason=reason)
            
            await ctx.send(f'{member.mention} has been timed out for {minutes} minutes. Reason: {reason}')
        except discord.Forbidden:
            await ctx.send('I do not have permission to time out this member.')
        except discord.HTTPException as e:
            await ctx.send(f'An error occurred while trying to time out the member: {e}')
            
    """
async def setup(bot):
    await bot.add_cog(mod(bot))