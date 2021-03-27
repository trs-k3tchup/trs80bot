import discord
from discord.ext import commands
import os

#i honestly don't know what to put here

class Hidden(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  async def hidden_message(self,ctx):
    await ctx.author.send('You have found one of several hidden commands! :shushing_face:\nCan you find them all? :thinking:')
  
  @commands.command(aliases=['requiem','truth','goldexperience'])
  async def _requiem(self, ctx):
    await ctx.author.send('*Korega Requiem Da*\nYou will never reach the truth!')

    await self.hidden_message(ctx)

  @commands.command(aliases=['80'])
  async def _80(self, ctx, *, cc='None'):
    if cc.lower() == 'color computer':
      await ctx.message.add_reaction('🖥️')
      await self.hidden_message(ctx)
    else:
      await ctx.message.add_reaction('🤔')

def setup(client):
  client.add_cog(Hidden(client))