import discord
from discord.ext import commands
import os

#note: 
#when bot responds to commands, it previously used ctx.send.
#this will be changed to ctx.reply to make the commands much easier to see,
#especially in crowded channels.

#function used to make the command prefix case-insensitive
def mixedCase(*args):
  total = []
  import itertools

  for string in args:
    a = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in string)))
    for x in list(a): total.append(x)

  return list(total)

#declares the bot, also uses the previously defined function
#case_insensitive is set to True to make commands case-insensitive
client = commands.Bot(case_insensitive=True, command_prefix=mixedCase("trs-" ))

#removes some built in commands so that they won't contradict with defined ones
client.remove_command('help')
client.remove_command('load')

#command to load/reload cogs
#makes testing much easier as you don't need to constantly restart the bot
@client.command(aliases=['reload','load'])
async def _load(ctx, extension):
  try: #unloads the extension and the reloads it again
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
  except: #if the extension is already unloaded, it will simply be loaded
    client.load_extension(f'cogs.{extension}')

  #sends a confirmation message to both discord and the console
  await ctx.reply(f"Extension '{extension}' has been reloaded.")
  print(f"Extension '{extension}' has been reloaded.")

#command to unload an extension
@client.command(aliases=['unload'])
async def _unload(ctx, extension):
  try: #unloads the extension and sends confirmation to both discord and console
    client.unload_extension(f"cogs.{extension}")
    await ctx.reply(f"Extension '{extension}' has been unloaded.")
    print(f"Extension '{extension}' has been unloaded.")
  except: #if the ext is already unloaded or doesn't exist, an error message will be sent
    await ctx.reply(f"The extension '{extension}' either does not exist or is already unloaded.")

#command to reload all extensions
@client.command(aliases=['reboot'])
async def _reboot(ctx):
  for filename in os.listdir('./cogs'): #the program will look for every file in the cog folder
    if filename.endswith('.py'):        #that ends in '.py'
      try:                              #files will then be loaded/reloaded.
        client.unload_extension(f'cogs.{filename[:-3]}')
        client.load_extension(f'cogs.{filename[:-3]}')
      except:
        client.load_extension(f'cogs.{filename[:-3]}')
  
  #confirm msg to discord+console
  await ctx.send("All extensions have been reloaded.")
  print("All extensions have been reloaded.")

#does the same thing as reboot cmd
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#token is hidden so the sneaky raccoons won't get to it
client.run(os.getenv('TOKEN'))
