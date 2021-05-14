import discord
from discord.ext import commands, tasks

class Startup(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    #print mesage to console when up and running
    print(f'Bot is online. Logged in as {self.client.user.name}')

    #set status to online
    await self.client.change_presence(status=discord.Status.online)
    await self.client.change_presence(activity=discord.Game('Team Fortress 2 [trs-help]'))
    self.change_status.start()
    

def setup(client):
  client.add_cog(Startup(client))