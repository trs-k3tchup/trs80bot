import discord
from discord.ext import commands, tasks
from itertools import cycle

#possible statuses that will be cycled through
status = cycle(['Team Fortress 2', 'Minecraft', 'Plants vs Zombies', 'Terraria', 'Sonic Forces', 'Undertale', 'Cuphead', 'Counter Strike: Global Offensive', 'Among Us', "Five Nights at Freddy's","Friday Night Funkin'"])

class Startup(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    #print mesage to console when up and running
    print(f'Bot is online. Logged in as {self.client.user.name}')

    #set status to online and start the task to change status
    await self.client.change_presence(status=discord.Status.online)
    self.change_status.start()
  
  #cycles through status list and yeah it does that
  @tasks.loop(hours=1)
  async def change_status(self):
    await self.client.change_presence(activity=discord.Game(f'{next(status)} [trs-help]'))

def setup(client):
  client.add_cog(Startup(client))