import discord
from discord.ext import commands
import json
import os
import random

class Eco(commands.Cog):
  def __init__(self, client):
    self.client = client

  #loads bank data 
  async def getbankdata(self):

    with open("./json/bank.json", "r") as f:
      users = json.load(f)

    return users

  #opens an account for the user if they don't already have one
  async def open_account(self, user):

    users = await self.getbankdata()
    user = user
    if str(user.id) in users:
      return False
    else:
      users[str(user.id)] = {}
      users[str(user.id)]["wallet"] = 0
      users[str(user.id)]["bank"] = 300
      users[str(user.id)]["streak"] = 0

    with open("./json/bank.json", "w") as f:
      json.dump(users, f)
      
    return True

  #adds money to a user's bank/wallet and also loads a user's bank info very epic
  async def updatebank(self, user, amt, categ="wallet", mode="add"):
    
    users = await self.getbankdata()

    try:
      amt = int(amt)
    except:
      pass

    if mode == "add":
      users[str(user.id)][categ] += amt
    elif mode == "subtract":
      users[str(user.id)][categ] -= amt
    elif mode == "set":
      users[str(user.id)][categ] = amt

    with open("./json/bank.json", "w") as f:
      json.dump(users, f)
    
    bal = [users[str(user.id)]["wallet"]], [users[str(user.id)]["bank"]]
    return bal

  @commands.command(aliases=['bal','balance','bank'])
  async def _balance(self, ctx):

    user = ctx.author
      
    await self.open_account(user)
    users = await self.getbankdata()
    wallet = users[str(user.id)]["wallet"]
    bank = users[str(user.id)]["bank"]
    streak = users[str(user.id)]["streak"]

    embed=discord.Embed(title=" ",color=0xff6f00)

    embed.set_author(name=f"{user.display_name}'s bank")

    embed.add_field(name="Wallet", value=f":coin:{wallet}", inline=True)
    embed.add_field(name="Bank", value=f":coin:{bank}", inline=True)

    embed.add_field(name="Total", value=f":moneybag:{wallet+bank}", inline=False)

    embed.add_field(name="Daily Streak", value=f"{streak}", inline=False)

    await ctx.send(embed=embed)

  @commands.command(aliases=['rps'])
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def _rps(self, ctx):

    user = ctx.author
    await self.open_account(user)
    win = random.randint(50, 200)
    lose = random.randint(50, 100)
    users = await self.getbankdata()

    if int(users[str(user.id)]["wallet"]) < 100:
      await ctx.send(f"{user.mention} You need at least 100 gold in your wallet to use this command.")
      return

    await ctx.send("Rock, Papers, Scissors!\n`type '1' for rock, '2' for paper, or '3' for scissors. You have 15 seconds to respond.`")
    
    def check(m):
      return m.channel == ctx.channel

    msg = await self.client.wait_for("message", check=check, timeout=15)

    try:
      msg = int(msg.content)
    except:
      await ctx.send("You may only reply with `1`, `2`, or `3`.")
      return

    if msg > 3 or msg < 1:
      await ctx.send("You may only reply with `1`, `2`, or `3`.")
      return
    
    bot = random.randint(1, 3)
    if bot == 1:
      send = 'Rock'
    elif bot == 2:
      send = 'Paper'
    else:
      send = 'Scissors'
    
    if msg == 1:
      send2 = 'Rock'
    elif msg == 2:
      send2 = 'Paper'
    else:
      send2 = 'Scissors'

    if msg == bot:
      x = None

    if msg == 1 and bot == 2 or msg == 2 and bot == 3 or msg == 3 and bot == 1:
      x = False

    if msg == 1 and bot == 3 or msg == 2 and bot == 1 or msg == 3 and bot == 2:
      x = True
    
    embed=discord.Embed(title="Rock Paper Scissors", color=0xff6f00)

    if x == True:

      embed.add_field(name=user.display_name, value=send2, inline=True)
      embed.add_field(name="Bot", value=send, inline=True)
      embed.set_footer(text=f"You won {win} coins!")
      await ctx.send(embed=embed)

      await self.updatebank(user, win)

    elif x == False:

      embed.add_field(name=user.display_name, value=send2, inline=True)
      embed.add_field(name="Bot", value=send, inline=True)
      embed.set_footer(text=f"You lost {lose} coins!")
      await ctx.send(embed=embed)

      await self.updatebank(user, -1*lose)
    
    else:

      embed.add_field(name=user.display_name, value=send2, inline=True)
      embed.add_field(name="Bot", value=send, inline=True)
      embed.set_footer(text="Draw!")
      await ctx.send(embed=embed)

  @commands.command(aliases=['deposit','dep'])
  async def _deposit(self, ctx, amt = None):

    user = ctx.author
    await self.open_account(user)
    users = await self.getbankdata()

    if amt.lower() == 'all':
      amt = int(users[str(user.id)]["wallet"])

    amt = int(amt)
    if amt > int(users[str(user.id)]["wallet"]):
      await ctx.send(f"{user.mention} You don't have that much money in your wallet.")
      return
    if amt <= 0:
      await ctx.send("What are you trying to do? :thinking:")
      return
    
    await self.updatebank(user, -1*amt)
    await self.updatebank(user, amt, "bank")

    await ctx.send(f"{user.mention} {amt} coins have been deposited into your bank.")

  @commands.command(aliases=['withdraw','with'])
  async def _withdraw(self, ctx, amt = None):

    user = ctx.author
    await self.open_account(user)
    users = await self.getbankdata()

    if amt.lower() == 'all':
      amt = int(users[str(user.id)]["bank"])

    amt = int(amt)
    if amt > int(users[str(user.id)]["bank"]):
      await ctx.send(f"{user.mention} You don't have that much money in your bank.")
      return
    if amt <= 0:
      await ctx.send("What are you trying to do? :thinking:")
      return
    
    await self.updatebank(user, amt)
    await self.updatebank(user, -1*amt, "bank")

    await ctx.send(f"{user.mention} {amt} coins have been withdrawn from your bank.")

  @commands.command(aliases=['steal','rob'])
  @commands.cooldown(1, 30, commands.BucketType.user)
  async def _steal(self, ctx, victim: discord.Member):

    user = ctx.author
    await self.open_account(user)
    users = await self.getbankdata()

    if victim.bot:
      await ctx.send("You can't rob a bot")
      return

    if str(victim.id) == "798358756466753546":
      await ctx.send("Nah")
      return

    if int(users[str(victim.id)]["wallet"]) < 200:
      await ctx.send(f"{user.mention} Your victim doesn't have at least 200 gold in their wallet.")
      return
    if int(users[str(user.id)]["wallet"]) < 200:
      await ctx.send(f"{user.mention} You need at least 200 gold in your wallet to rob someone.")
      return

    rand = random.randint(1, 5)
    if rand <= 2:
      loss = (int(users[str(user.id)]["wallet"])) * 0.5
      loss = int(loss)
      await ctx.send(f"{user.mention} You were caught! You paid {loss} gold to your victim.")
      await self.updatebank(user, -1*loss)
      await self.updatebank(victim, loss)
      return
    
    rand = random.randint(1, 100)
    if rand <= 50:
      gain = (int(users[str(victim.id)]["wallet"])) * 0.25
      gain = int(gain)
      await ctx.send(f"{user.mention} You successfully stole {gain} coins from {victim.display_name}'s wallet.")
    elif rand <= 75:
      gain =(int(users[str(victim.id)]["wallet"])) * 0.5
      gain = int(gain)
      await ctx.send(f"{user.mention} You successfully stole {gain} coins from {victim.display_name}'s wallet.")
    elif rand <= 99:
      gain =(int(users[str(victim.id)]["wallet"])) * 0.75
      gain = int(gain)
      await ctx.send(f"{user.mention} You successfully stole {gain} coins from {victim.display_name}'s wallet.")
    elif rand == 100:
      gain =int(users[str(victim.id)]["wallet"])
      await ctx.send(f"{user.mention} Jackpot! You stole everything from {victim.display_name}'s wallet.")

    await self.updatebank(user, gain)
    await self.updatebank(victim, -1*gain)

  @commands.command(aliases=['beg'])
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def _beg(self, ctx):

    user = ctx.author
    await self.open_account(user)

    rand = random.randint(1, 3)
    if rand == 1:
      await ctx.send(f"{user.mention} No one gave you anything.")
      return
    
    earn = random.randint(50, 175)
    await ctx.send(f"{user.mention} You were given {earn} coins.")
    await self.updatebank(user, earn)
  
  @commands.command(aliases=['double','bet','5050'])
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def _double(self, ctx, amt):

    user = ctx.author
    await self.open_account(user)
    users = await self.getbankdata()

    try:
      amt = int(amt)
    except:
      await ctx.send(f"{user.mention} You need to provide a valid amount.")
      return
    
    if amt > int(users[str(user.id)]["wallet"]) or amt <= 0:
      await ctx.send(f"{user.mention} You need to provide a valid amount.")
      return

    rand = random.randint(1, 2)
    if rand == 1:
      await ctx.send(f"{user.mention} Success! You gained {amt} coins!")
      await self.updatebank(user, amt)
    else:
      await ctx.send(f"{user.mention} You lost {amt} coins. Too bad!")
      await self.updatebank(user, -1*amt)

  @commands.command(aliases=['give'])
  async def _give(self, ctx, victim: discord.Member, amt):

    user = ctx.author
    await self.open_account(user)
    users = await self.getbankdata()

    if victim.bot:
      await ctx.send("You can't give money to a bot")
      return

    try:
      amt = int(amt)
    except:
      await ctx.send(f'{user.mention} Please provide an integer value.')
      return
    
    if amt > int(users[str(user.id)]["wallet"]):
      await ctx.send(f"{user.mention} You don't have that much money in your wallet.")
      return
    
    if amt <= 0:
      await ctx.send(f"{user.mention} {amt} is an invalid amount.")
      return
    
    await self.updatebank(user, -1*amt)
    await self.updatebank(victim, amt)

    embed=discord.Embed(title="", color=0xff6f00)
    embed.add_field(name=f"You gave {victim.display_name} {amt} coins.", value=f"Now you have {(int(users[str(user.id)]['wallet']))-amt} and they have {int(users[str(user.id)]['wallet'])}", inline=True)
    await ctx.send(embed=embed)

  @commands.command(aliases=['daily'])
  @commands.cooldown(1, 60*60*18, commands.BucketType.user)
  async def _daily(self, ctx):
    user = ctx.author
    await self.open_account(user)
    users = await self.getbankdata()

    await self.updatebank(user, 1, "streak")

    multiplier = 1 + int(users[str(user.id)]["streak"]) * 0.25
    earning = 1000 * multiplier
    earning = round(earning)

    await self.updatebank(user, earning, "bank")
    
    await ctx.send(f"{user.mention} Your daily coins ({round(earning)}) have been deposited into your bank. You are now on a daily streak of {users[str(user.id)]['streak'] + 1}. Your next daily reward can be claimed in 16h.")

def setup(client):
  client.add_cog(Eco(client))