import discord
from discord.ext import commands
import random
import asyncio
import datetime

#ext contains all the general commands

class Commands(commands.Cog):
  def __init__(self, client):
    self.client = client

  #ping command
  @commands.command(aliases=['ping'])
  async def _ping(self, ctx):
    await ctx.reply(f"Ping, Pong, Ding, Dong! Your request took {round(self.client.latency*1000)} milliseconds.")

  #simple random number generator
  @commands.command(aliases=['rand','rng'])
  async def _rand(self, ctx, x, y):
    try:
      x = int(x)
      y = int(y)
    except:
      await ctx.send("Please only input integer values.")
      return
    
    if x >= y:
      await ctx.send("Please make sure your first number is larger than your second number.")
      return
    
    value = random.randint(x, y)

    embed=discord.Embed(title="Random number generated. ",color=0xff6f00)
    embed.add_field(name="Paramaters:", value=f"{x}, {y}", inline=True)
    embed.add_field(name="Resut:", value=value, inline=True)
    await ctx.reply(embed=embed)
  
  #8ball command, pulls randomly from list of responses
  @commands.command(aliases=['8ball'])
  async def _8ball(self, ctx, *, question):
    responses = [
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes - definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful.",
    "lol no"
    ]

    embed=discord.Embed(title=" ",color=0xff6f00)
    embed.add_field(name=f"{ctx.author.display_name}'s Question: '{question}'", value=f"Answer: {random.choice(responses)}", inline=True)
    await ctx.reply(embed=embed)

  #command to dm another user thru the bot
  @commands.command(aliases=['dm','pm','msg'])
  async def _dm(self, ctx, member: discord.Member, *, message):
    try:
      await member.send(f"{ctx.author} from {ctx.message.guild.name} says '{message}'")
      await ctx.reply('DM sent.')
    except:
      await ctx.reply(f"Could not send message. {member.mention}'s dms are closed.")

  #random rating generator
  @commands.command(aliases=['rate'])
  async def _rate(self, ctx, *, thing):
    rating = [
      '1/10 just terrible',
      '2/10 would not recommend',
      '3/10 kinda sucked ngl',
      '4/10 very bad',
      '5/10 no comment',
      '6/10 could be better',
      '7/10 very cool',
      '8/10 would recommend',
      '9/10 breathtaking'
      '10/10 simply perfect'
    ]
    
    embed=discord.Embed(title=" ",color=0xff6f00)
    embed.add_field(name=f"Rating for '{thing}'", value=random.choice(rating), inline=True)
    await ctx.reply(embed=embed)

  #quick y/n poll command
  @commands.command(aliases=['quickpoll','qpoll'])
  async def _quickpoll(self, ctx, *, question):
    await ctx.channel.purge(limit=1) #deletes the original message for convenience

    #creates an embed with the question and reacts with a check and x emoji
    embed=discord.Embed(color=0xff6f00)
    embed.add_field(name=f"{ctx.author.display_name} asks:\n'{question}'", value="✅ for Yes, ❎ for No", inline=False)
    message = await ctx.send(embed=embed)

    await message.add_reaction("✅")
    await message.add_reaction("❎")
  
  #coin flipper
  @commands.command(aliases=['flip','cf'])
  async def _flip(self, ctx):
    choice = [
      "Heads.",
      "Tails."
    ]

    await ctx.reply(random.choice(choice))
  
  #replaces all spaces in a message with :clap:
  @commands.command(aliases=['clapify','clap'])
  async def _clap(self, ctx, *, message):
    text = str(message)
    text = text.replace(" ",":clap:")

    await ctx.channel.purge(limit=1) #deletes the original message for convenience
    await ctx.send(f":clap:{text}:clap:")

  #command to choose at random from given choices
  @commands.command(aliases=['choose','choice'])
  async def _choose(self, ctx, *choices):
    await ctx.send(f'{ctx.author.mention} I choose {random.choice(choices)}.')

  #uses a webhook to impersonate another user
  @commands.command(aliases=['impersonate','copy'])
  async def _impersonate(self, ctx, user: discord.Member, *, message):
    await ctx.channel.purge(limit=1) #deletes the original message for convenience

    #creates a webhook with the name and avatar of the victim
    webhook = await ctx.channel.create_webhook(name=user.name) 
    await webhook.send(
      str(message), username=user.display_name, avatar_url=user.avatar_url)

    #deletes webhook when done
    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
      await webhook.delete()

  #random epic rating
  @commands.command(aliases=['howepic','epicrate'])
  async def _epicrate(self, ctx):
    rating = random.randint(1,100)

    if rating <= 25:
      msg = "Not epic."
    elif rating <= 50:
      msg = "Not so epic."
    elif rating <= 75:
      msg = "Epic."
    elif rating <= 99:
      msg = "Very epic :sunglasses:"
    elif rating == 100:
      msg = "You are a very epic bro :sunglasses:"

    embed=discord.Embed(title=" ",color=0xff6f00)
    embed.add_field(name=f"{ctx.author.display_name} is {rating}% epic!", value=msg, inline=True)
    await ctx.reply(embed=embed)
  
  #displays info on an emoji
  @commands.command(aliases=['getemoji','emoji'])
  async def _getemoji(self, ctx, emoji: discord.Emoji):
    await ctx.reply(f"Emoji: {emoji}\nEmoji name: {emoji.name}\nEmoji ID: {emoji.id}")

  #displays current gmt time
  @commands.command(aliases=['time','date'])
  async def _time(self, ctx):
    today = datetime.datetime.now()
    hour = int(today.strftime("%I"))
    minute = today.strftime("%M")
    ampm = today.strftime("%p")
    wd = today.strftime("%A")
    month = today.strftime("%B")
    day = int(today.strftime("%d"))
    year = today.strftime("%Y")

    await ctx.send(f"It is currently {hour}:{minute} {ampm} GMT this {wd}, {month} {day}, {year}.")

  #polling command, code was taken from github lol
  @commands.command(aliases=['poll'])
  async def _poll(self, ctx, question, *options: str):
      #must have 2-10 optins
      if len(options) <= 1:
        await ctx.send('You need more than one option to make a poll!')
        return
      if len(options) > 10:
          await ctx.send('You cannot make a poll for more than 10 things!')
          return

      #if there are 2 options and they are 'yes' and 'no', then react with check and x
      if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
          reactions = ['✅', '❌']
      else: #else, react with number emojis
          reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

      #i don't know how the rest works lmao
      description = []
      for x, option in enumerate(options):
          description += '\n {} {}'.format(reactions[x], option)
      embed = discord.Embed(title=f"{ctx.author.display_name} asks '{question}'",color=0xff6f00, description=''.join(description))
      react_message = await ctx.send(embed=embed)
      for reaction in reactions[:len(options)]:
          await react_message.add_reaction(reaction)
      embed.set_footer(text='Poll ID: {}'.format(react_message.id))
      await react_message.edit(embed=embed)

def setup(client):
  client.add_cog(Commands(client))