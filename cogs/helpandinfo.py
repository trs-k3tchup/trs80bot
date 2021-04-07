import discord
from discord.ext import commands
from helpdata import helpdict

#contains code for info and help command

class Info(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['bot'])
  async def info(self,ctx):

    embed=discord.Embed(title="Bot info", description="This bot is @trashk3tchup's attempt to make a discord bot for the first time. Join the bot discord if you have any questions, suggestions, or just want to see the bot as it's being developed.", color=0xff6f00)

    embed.set_author(name="TRS-80 Color Computer Bot")

    embed.add_field(name="Official Discord",value="https://discord.gg/TVYPBMfJ9U", inline=True)
    embed.add_field(name="Invite to Server", value="https://bit.ly/3ifOWwn", inline=True)
    embed.add_field(name="My Creator's Website", value="https://trs-k3tchup.github.io/trashk3tchupweb/", inline=False)

    await ctx.send(embed=embed)
  
  @commands.command()
  async def help(self, ctx, cmd=None):

    if cmd == None:
      embed=discord.Embed(title=" ",color=0xff6f00)
      embed.set_author(name="Commands List")

      embed.add_field(name="Info", value="`help`, `info`, `hidden`", inline=False)      

      embed.add_field(name="General", value="`ping`, `rand`, `8ball`, `dm`, `rate`, `quickpoll`, `poll`, `flip`, `clapify`, `choose`, `impersonate`, `howgay`, `epicrate`, `getemoji`, `time`", inline=False)

      embed.add_field(name="Economy", value="`balance`, `deposit`, `withdraw`, `rps`, `rob`, `beg`, `double`, `daily`", inline=False)

      embed.add_field(name="Images", value="`pog`, `respect`, `chocolate`, `avatar`, `wanted`, `woosh`", inline=False)

      embed.add_field(name="Moderation", value="`clear`, `kick`, `ban`, `unban`", inline=False)

      embed.set_footer(text="for more info on a command, type trs-help [command]")

    
    else:
      try:
        cmddata = self.client.helpdict[cmd]
        cmdname = cmd
        descrpt = cmddata[0]
        usage = cmddata[1]
        aliases = cmddata[2]

        embed=discord.Embed(title=" ",color=0xff6f00)
        embed.add_field(name=f"{cmdname} command", value=f"{descrpt}", inline=False)
        embed.add_field(name="usage", value=f"`trs-{usage}`", inline=False)
        embed.add_field(name="aliases", value=f"{aliases}", inline=False)
      except:
        await ctx.send("That isn't a command. Please check `trs-help` for a list of commands.")

    await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Info(client))