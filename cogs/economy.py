import discord
from discord.ext import commands
import json
import os
import random

#ext contains code economy sytem, will be re-done in the future

class Eco(commands.Cog):
  def __init__(self, client):
    self.client = client

  #function to load bank data 
  async def getbankdata(self):
    with open("./json/bank.json", "r") as f: #just opens the json file and returns info
      users = json.load(f)

    return users

  #function that opens an account for the user if they don't already have one
  async def open_account(self, user):
    #uses previous function to load bankdata
    users = await self.getbankdata()
    user = user
    #if user is already registered, return
    if str(user.id) in users:
      return False
    #if not, create an account for them
    else:
      users[str(user.id)] = {}
      users[str(user.id)]["wallet"] = 0
      users[str(user.id)]["bank"] = 300
      users[str(user.id)]["streak"] = 0

    #dump all new data in json
    with open("./json/bank.json", "w") as f:
      json.dump(users, f)
      
    return True

  #function that adds money to a user's bank/wallet and also loads a user's bank info very epic
  async def updatebank(self, user, amt, categ="wallet", mode="add"):  
    users = await self.getbankdata()

    #idk why this is here
    #basically passes even if amt is invalid
    try:
      amt = int(amt)
    except:
      pass

    #checks the inputted mode and does the corresponding action
    if mode == "add":
      users[str(user.id)][categ] += amt
    elif mode == "subtract":
      users[str(user.id)][categ] -= amt
    elif mode == "set":
      users[str(user.id)][categ] = amt

    #dump data
    with open("./json/bank.json", "w") as f:
      json.dump(users, f)
    
    #return bankdata because yes
    bal = [users[str(user.id)]["wallet"]], [users[str(user.id)]["bank"]]
    return bal

  #cmd to check bank balance 
  @commands.command(aliases=['bal','balance','bank'])
  async def _balance(self, ctx):
    user = ctx.author
    
    #open account if none yet
    await self.open_account(user)
    users = await self.getbankdata()

    #gather data in variables
    wallet = users[str(user.id)]["wallet"]
    bank = users[str(user.id)]["bank"]
    streak = users[str(user.id)]["streak"]

    #set an embed
    embed=discord.Embed(title=" ",color=0xff6f00)

    embed.set_author(name=f"{user.display_name}'s bank")

    embed.add_field(name="Wallet", value=f":coin:{wallet}", inline=True)
    embed.add_field(name="Bank", value=f":coin:{bank}", inline=True)
    embed.add_field(name="Total", value=f":moneybag:{wallet+bank}", inline=False)

    embed.add_field(name="Daily Streak", value=f"{streak}", inline=False)

    await ctx.reply(embed=embed)

  #rock papers scissors command
  @commands.command(aliases=['rps'])
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def _rps(self, ctx):
    user = ctx.author
    await self.open_account(user)

    #sets amounts to be won or lost
    win = random.randint(50, 200)
    lose = random.randint(50, 100)

    users = await self.getbankdata()

    #check if user has at least 100 in wallet. if not, return
    if int(users[str(user.id)]["wallet"]) < 100:
      await ctx.send(f"{user.mention} You need at least 100 gold in your wallet to use this command.")
      return

    await ctx.reply("Rock, Papers, Scissors!\n`type '1' for rock, '2' for paper, or '3' for scissors. You have 15 seconds to respond.`")
    
    #sets a check and waits for user input
    def check(m):
      return m.channel == ctx.channel

    msg = await self.client.wait_for("message", check=check, timeout=15)

    #error handler is input is not an integer
    try:
      msg = int(msg.content)
    except:
      await ctx.reply("You may only reply with `1`, `2`, or `3`.")
      return
    #error handler is input is not 1-3
    if msg > 3 or msg < 1:
      await ctx.reply("You may only reply with `1`, `2`, or `3`.")
      return
    
    #sets bot to random number
    bot = random.randint(1, 3)

    #uses a simple switcher dictionary to convert number to rps
    switcher = {
      1: 'Rock',
      2: 'Paper',
      3: 'Scissor',
    }

    send = switcher.get(bot)
    send2 = switcher.get(msg)

    #checks for win, lose, or draw conditions
    if msg == bot:
      x = None

    if msg == 1 and bot == 2 or msg == 2 and bot == 3 or msg == 3 and bot == 1:
      x = False

    if msg == 1 and bot == 3 or msg == 2 and bot == 1 or msg == 3 and bot == 2:
      x = True
    
    embed=discord.Embed(title="Rock Paper Scissors", color=0xff6f00)

    #sends everything in an embed and updates bank
    if x == True:
      embed.add_field(name=user.display_name, value=send2, inline=True)
      embed.add_field(name="Bot", value=send, inline=True)
      embed.set_footer(text=f"{user.display_name} won {win} coins!")
      await ctx.send(embed=embed)

      await self.updatebank(user, win)

    elif x == False:
      embed.add_field(name=user.display_name, value=send2, inline=True)
      embed.add_field(name="Bot", value=send, inline=True)
      embed.set_footer(text=f"{user.display_name} lost {lose} coins!")
      await ctx.send(embed=embed)

      await self.updatebank(user, -1*lose)
    
    else:
      embed.add_field(name=user.display_name, value=send2, inline=True)
      embed.add_field(name="Bot", value=send, inline=True)
      embed.set_footer(text=f"{user.display_name} had a draw!")
      await ctx.send(embed=embed)

  #command to deposit money to bank
  @commands.command(aliases=['deposit','dep'])
  async def _deposit(self, ctx, amt = None):
    user = ctx.author
    await self.open_account(user)
    users = await self.getbankdata()

    #if user entered "all" as the amount, set amt to whatever is in the wallet
    if amt.lower() == 'all':
      amt = int(users[str(user.id)]["wallet"])

    #makes sure the entered amount isn't none, negative, or more than wallet amount
    amt = int(amt)
    if amt > int(users[str(user.id)]["wallet"]):
      await ctx.reply("You don't have that much money in your wallet.")
      return
    if amt <= 0:
      await ctx.reply("What are you trying to do? :thinking:")
      return
    
    #subtracts amount from wallet and add amount to bank
    await self.updatebank(user, -1*amt)
    await self.updatebank(user, amt, "bank")

    #conf message
    await ctx.reply(f"{amt} coins have been deposited into your bank.")

  #withdraw from bank
  #essentially the same process as deposit but the other way around
  @commands.command(aliases=['withdraw','with'])
  async def _withdraw(self, ctx, amt = None):
    user = ctx.author
    await self.open_account(user)
    users = await self.getbankdata()

    if amt.lower() == 'all':
      amt = int(users[str(user.id)]["bank"])

    amt = int(amt)
    if amt > int(users[str(user.id)]["bank"]):
      await ctx.reply("You don't have that much money in your bank.")
      return
    if amt <= 0:
      await ctx.reply("What are you trying to do? :thinking:")
      return
    
    await self.updatebank(user, amt)
    await self.updatebank(user, -1*amt, "bank")

    await ctx.reply(f"{amt} coins have been withdrawn from your bank.")

  #command to steal money from another user
  @commands.command(aliases=['steal','rob'])
  @commands.cooldown(1, 30, commands.BucketType.user)
  async def _steal(self, ctx, victim: discord.Member):
    user = ctx.author
    await self.open_account(user)
    users = await self.getbankdata()

    #checks if victim is trs-80
    if str(victim.id) == "798358756466753546":
      await ctx.reply("Nah")
      return

    #checks if the victim is a bot
    #you can't rob a bot
    if victim.bot:
      await ctx.reply("You can't rob a bot")
      return

    #checks if both user and victim have at least 200 gold in wallet
    if int(users[str(victim.id)]["wallet"]) < 200:
      await ctx.reply(f"Your victim doesn't have at least 200 gold in their wallet.")
      return
    if int(users[str(user.id)]["wallet"]) < 200:
      await ctx.reply(f"You need at least 200 gold in your wallet to rob someone.")
      return

    #2/5 chance to fail
    #upon failure, 50% of user wallet is sent to victim
    rand = random.randint(1, 5)
    if rand <= 2:
      loss = (int(users[str(user.id)]["wallet"])) * 0.5
      loss = int(loss)
      await ctx.reply(f"You were caught! You paid {loss} gold to your victim.")
      await self.updatebank(user, -1*loss)
      await self.updatebank(victim, loss)
      return

    rand = random.randint(1, 100)
    #50% chance to steal 1/4 of victim wallet
    if rand <= 50:
      gain = (int(users[str(victim.id)]["wallet"])) * 0.25
      gain = int(gain)
      await ctx.reply(f"You successfully stole {gain} coins from {victim.display_name}'s wallet.")
    #25% chance to steal half of victim wallet
    elif rand <= 75:
      gain =(int(users[str(victim.id)]["wallet"])) * 0.5
      gain = int(gain)
      await ctx.reply(f"You successfully stole {gain} coins from {victim.display_name}'s wallet.")
    #24% chance to steal 3/4 of victim wallet
    elif rand <= 99:
      gain =(int(users[str(victim.id)]["wallet"])) * 0.75
      gain = int(gain)
      await ctx.reply(f"You successfully stole {gain} coins from {victim.display_name}'s wallet.")\
    #1% chance to steal everything
    elif rand == 100:
      gain =int(users[str(victim.id)]["wallet"])
      await ctx.reply(f"Jackpot! You stole everything from {victim.display_name}'s wallet.")

    await self.updatebank(user, gain)
    await self.updatebank(victim, -1*gain)

  #beg command
  @commands.command(aliases=['beg'])
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def _beg(self, ctx):
    user = ctx.author
    await self.open_account(user)

    #1/4 chance to not get anything
    rand = random.randint(1, 4)
    if rand == 1:
      await ctx.reply(f"No one gave you anything.")
      return
    
    #random earning from 50-75
    earn = random.randint(50, 175)
    await ctx.reply(f"You were given {earn} coins.")
    await self.updatebank(user, earn)
  
  #50/50 command
  @commands.command(aliases=['double','5050'])
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def _double(self, ctx, amt):
    user = ctx.author
    await self.open_account(user)
    users = await self.getbankdata()

    if amt.lower() == 'all':
      amt = int(users[str(user.id)]["wallet"])

    #return if invalid amount
    try:
      amt = int(amt)
    except:
      await ctx.reply(f"{user.mention} You need to provide a valid amount.")
      return
    
    if amt > int(users[str(user.id)]["wallet"]) or amt <= 0:
      await ctx.reply(f"{user.mention} You need to provide a valid amount.")
      return

    rand = random.randint(1, 2)
    if rand == 1:
      await ctx.reply(f"Success! You gained {amt} coins!")
      await self.updatebank(user, amt)
    else:
      await ctx.reply(f"You lost {amt} coins. Too bad!")
      await self.updatebank(user, -1*amt)

  #command to give money to another user
  @commands.command(aliases=['give'])
  async def _give(self, ctx, victim: discord.Member, amt):
    user = ctx.author
    await self.open_account(user)
    users = await self.getbankdata()

    #you can't give money to a bot
    if victim.bot:
      await ctx.reply("You can't give money to a bot")
      return

    #return if invalid amount
    try:
      amt = int(amt)
    except:
      await ctx.reply(f'Please provide an integer value.')
      return
    
    if amt > int(users[str(user.id)]["wallet"]):
      await ctx.reply(f"You don't have that much money in your wallet.")
      return
    
    if amt <= 0:
      await ctx.reply(f"{amt} is an invalid amount.")
      return
    
    await self.updatebank(user, -1*amt)
    await self.updatebank(victim, amt)

    embed=discord.Embed(title="", color=0xff6f00)
    #had to subtract amt from user wallet in the embed bc it doesn't show the updated version for some reason
    embed.add_field(name=f"You gave {victim.display_name} {amt} coins.", value=f"Now you have {(int(users[str(user.id)]['wallet']))-amt} and they have {int(users[str(user.id)]['wallet'])}", inline=True)
    await ctx.reply(embed=embed)

  #daily coins command
  #i would love if it reset at like midnight gmt
  #but idk how to do that yet so for now it's just a really long cooldown
  @commands.command(aliases=['daily'])
  @commands.cooldown(1, 60*60*18, commands.BucketType.user)
  async def _daily(self, ctx):
    user = ctx.author
    await self.open_account(user)
    users = await self.getbankdata()

    #update streak
    await self.updatebank(user, 1, "streak")

    #multiplier is 1 + streak*0.25
    #multiply 1000 by multiplier
    multiplier = 1 + int(users[str(user.id)]["streak"]) * 0.25
    earning = 1000 * multiplier
    earning = round(earning)

    await self.updatebank(user, earning, "bank")
    
    await ctx.reply(f"Your daily coins ({round(earning)}) have been deposited into your bank. You are now on a daily streak of {users[str(user.id)]['streak'] + 1}. Your next daily reward can be claimed in 16h.")

def setup(client):
  client.add_cog(Eco(client))