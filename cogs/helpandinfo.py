import discord
from discord.ext import commands

#contains code for info and help command

class Info(commands.Cog):
  def __init__(self, client):
    self.client = client

    self.client.helpdict = {
      'info': ['Displays bot info.', 'info', 'info, bot'],
      'bot': ['Displays bot info.', 'info', 'info, bot'],
      'help': ['Displays a list of commands/command usage.', 'help [command]', 'help'],

      'ping': ["Displays the bot's ping.", 'ping', 'ping'],
      'rand': ['Generates a random number.', 'rand [num1] [num2]', 'rand, rng'],
      'rng': ['Generates a random number.', 'rand [num1] [num2]', 'rand, rng'],
      '8ball': ['Generates a yes-or-no response.', '8ball [question]', '8ball'],
      'dm': ['Sends a DM to another user', 'dm [user] [message]', 'dm, pm, msg'],
      'pm': ['Sends a DM to another user', 'dm [user] [message]', 'dm, pm, msg'],
      'msg': ['Sends a DM to another user', 'dm [user] [message]', 'dm, pm, msg'],
      'rate': ['Generates a random rating out of 10.', 'rate [thing]', 'rate'],
      'poll': ['Creates a poll. Choices are seperated by spaces. For multi-word choices, use quotation marks.', 'poll "[question]" [choices]', 'poll'],
      'quickpoll': ['Creates a yes-or-no poll.', 'quickpoll [question]', 'quickpoll, qpoll'],
      'qpoll': ['Creates a yes-or-no poll.', 'quickpoll [question]', 'quickpoll, qpoll'],
      'flip': ['Flips a virtual coin.', 'flip', 'flip, cf'],
      'cf': ['Flips a virtual coin.', 'flip', 'flip, cf'],
      'clapify': ['Add some :clap: to your statement.', 'clapify [message]', 'clapify, clap'],
      'clap': ['Add some :clap: to your statement.', 'clapify [message]', 'clapify, clap'],
      'choose': ['Randomly chooses from 3 options. Choices are seperated by spaces. For multi-word choices, use quotation marks.', 'choose [choices]', 'choose, choice'],
      'choice': ['Randomly chooses from 3 options. Choices are seperated by spaces. For multi-word choices, use quotation marks.', 'choose [choices]', 'choose, choice'],
      'impersonate': ['Impersonates another user.', 'impersonate [user] [message]', 'impersonate, impostor'],
      'impostor': ['Impersonates another user.', 'impersonate [user] [message]', 'impersonate, impostor'],
      'howgay': ['How gay are you?:flushed:', 'howgay', 'howgay'],
      'epicrate': ['How epic are you?', 'epicrate', 'epicrate'],
      'getemoji': ["Returns the data for a custom emoji. Does not work with Discord's default emojis", 'getemoji [emoji]', 'getemoji, emoji'],
      'emoji': ["Returns the data for a custom emoji. Does not work with Discord's default emojis", 'getemoji [emoji]', 'getemoji, emoji'],
      'time': ['Returns the current GMT date and time.', 'time', 'time, date, datetime'],
      'date': ['Returns the current GMT date and time.', 'time', 'time, date, datetime'],

      'clear': ['Deletes messages from a channel.', 'clear [amount (default=1)]', 'clear, purge, delete'],
      'purge': ['Deletes messages from a channel.', 'clear [amount (default=1)]', 'clear, purge, delete'],
      'delete': ['Deletes messages from a channel.', 'clear [amount (default=1)]', 'clear, purge, delete'],
      'kick': ['Kicks a user from the server.', 'kick [user] [reason]', 'kick'],
      'ban': ['Bans a user from the server.', 'ban [user] [reason]', 'ban, block'],
      'block': ['Bans a user from the server.', 'ban [user] [reason]', 'ban, block'],
      'unban': ['Unbans a banned user.', 'unban [user]', 'unban, unblock'],
      'unblock': ['Unbans a banned user.', 'unban [user]', 'unban, unblock']
    }

  @commands.command(aliases=['info','bot'])
  async def _info(self,ctx):

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

      embed.add_field(name="Info", value="`help`, `info`", inline=False)      

      embed.add_field(name="General", value="`ping`, `rand`, `8ball`, `dm`, `rate`, `quickpoll`, `poll`, `flip`, `clapify`, `choose`, `impersonate`, `howgay`, `epicrate`, `getemoji`, `time`", inline=False)

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