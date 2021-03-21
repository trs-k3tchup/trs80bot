import discord
from discord.ext import commands

class ErrorMsg(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    #declares embed to contain error info
    embed=discord.Embed(color=0xff6f00)

    #react with question mark if command doesn't exist
    if isinstance(error, commands.CommandNotFound):
      await ctx.message.add_reaction('❓')

    #error if user does not have the required perms to call a command
    elif isinstance(error, commands.MissingPermissions):
      embed.add_field(name="<:trserror:808530900454998026> Missing Permissions", value="You are missing the required permissions to use this command.", inline=False)

      await ctx.reply(embed=embed)
      return
		
    #error if user did not enter all required arguments
    elif isinstance(error, commands.MissingRequiredArgument):
      embed.add_field(name="<:trserror:808530900454998026> Missing Required Arguments", value="You are missing one or more arguments to use this command. Type `trs-help` for a full list of commands and `trs-help [command]` for command usage.", inline=False)

      await ctx.reply(embed=embed)
      return
    
    #error if command is on cooldown, uses some tedious code to display time left
    elif isinstance(error, commands.CommandOnCooldown):
      s = error.retry_after
      if s < 1:
        s = None
        embed.add_field(name="<:trserror:808530900454998026> Command On Cooldown", value="You are doing that too quickly.", inline=False)
      elif s <= 60:
        s = round(s)
        embed.add_field(name="<:trserror:808530900454998026> Command On Cooldown", value=f"You are doing that too quickly. Try again in {s}s", inline=False)
      elif s <= 3600:
        m = s // 60
        s = s % 60
        m = round(m)
        s = round(s)
        embed.add_field(name="<:trserror:808530900454998026> Command On Cooldown", value=f"You are doing that too quickly. Try again in {m}m {s}s", inline=False)
      elif s > 3600:
        m = s // 60
        h = m // 60
        m = m % 60
        s = s % 3600
        h = round(h)
        m = round(m)
        s = round(s)
        embed.add_field(name="<:trserror:808530900454998026> Command On Cooldown", value=f"You are doing that too quickly. Try again in {h}h {m}m", inline=False)
      
      await ctx.send(embed=embed)
      return

    #error if invalid arguments or bug in the code
    else:
      embed.add_field(name="<:trserror:808530900454998026> Something Went Wrong", value="Either you entered invalid arguments, or there is an error in the code. If you are sure you called the command correcty, please contact the dev.", inline=False)
      await ctx.send(embed=embed)
      return

def setup(client):
  client.add_cog(ErrorMsg(client))