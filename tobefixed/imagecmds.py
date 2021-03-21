import discord
from discord.ext import commands

import asyncio

import PIL
from PIL import Image, ImageFont, ImageDraw

from io import BytesIO

import os

import random

poglist = os.listdir('./images/poggers')
flist = os.listdir('images/respect')

class ImageCmd(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases=['poggers', 'pogchamp'])
  async def pog(self, ctx):

    pog = random.choice(poglist)
		
    await ctx.send('Poggers')
    await ctx.send(file=discord.File(f'./images/poggers/{pog}'))
  
  @commands.command(aliases=['bigf'])
  async def respect(self, ctx):

    fpic = random.choice(flist)
    
    await ctx.send('F')
    await ctx.send(file=discord.File(f'./images/respect/{fpic}'))
  
  @commands.command(aliases=['pfp', 'ava'])
  async def avatar(self, ctx, *,  user : discord.Member=None):

    if user == None:
      user = ctx.author
    userAvatarUrl = user.avatar_url

    embed=discord.Embed(title=f"{user}'s avatar", color=0xff6f00)
    embed.set_image(url = userAvatarUrl)
    await ctx.send(embed=embed)
  
  @commands.command()
  async def chocolate(self, ctx):
		
    await ctx.send('Chocolate? Did you say chocolate?')
    await ctx.send(file=discord.File('./images/chocolate.gif'))
  
  @commands.command(aliases=['bounty'])
  async def wanted(self, ctx, user: discord.Member = None):
    if user == None:
      user = ctx.author
    
    wanted = Image.open("./images/wanted.jpg")
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((245, 245))
    wanted.paste(pfp,(118,251))

    wanted.save("./images/profile.jpg")

    await ctx.send(file = discord.File("./images/profile.jpg"))

  @commands.command()
  async def woosh(self, ctx, user: discord.Member = None):
    if user == None:
      user = ctx.author
    
    woosh = Image.open("./images/woosh.jpg")
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((87, 85))
    woosh.paste(pfp,(178, 197))

    woosh.save("./images/profile.jpg")

    await ctx.send(file = discord.File("./images/profile.jpg"))
  
  @commands.command()
  async def gun(self, ctx, user: discord.Member = None):
    
    if user == None:
      user = ctx.author

    gun = Image.open("./images/gun.png")
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((100, 100))
    gun = gun.resize((34, 56))
    pfp.paste(gun,(66, 44))

    pfp.save("./images/profile.jpg")
    await ctx.send(file = discord.File("./images/profile.jpg"))

def setup(client):
  client.add_cog(ImageCmd(client))