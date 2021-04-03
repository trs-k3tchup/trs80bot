import discord
from discord.ext import commands

class ModCommands(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  #command to mass delete messages
  @commands.command(aliases=['clear', 'purge', 'delete'])
  @commands.has_permissions(manage_messages = True)
  async def _clear(self, ctx, amount=1):
    await ctx.channel.purge(limit=amount)

  #command to kick members from the server
  @commands.command()
  @commands.has_permissions(kick_members = True)
  async def kick(self, ctx, member: discord.Member, *, reason=None):
    #returns if target is the user, you can't kick yourself
    if member == ctx.author:
      await ctx.reply("You can't kick yourself :thinking:")
      return
    
    try:
      await member.kick(reason=reason)
      await ctx.reply(f'Member {member.mention} has been kicked.')
      try:
        #sends dm to kicked member
        await member.send(f'You have been kicked from {ctx.message.guild.name}.\nReason given: {reason}')
      except:
        #error msg if user's dms are closed
        await ctx.reply("Could not send confirmation dm to member.")
    except:
      #error message for missing perms
      embed=discord.Embed(color=0xff6f00)
      embed.add_field(name="<:trserror:808530900454998026> Missing Permissions", value="It seems the bot doesn't have the permissions to perform this action.", inline=False)
      await ctx.reply(embed=embed)
  
  #command to ban user from server
  @commands.command(aliases=['block','ban'])
  @commands.has_permissions(ban_members = True)
  async def _ban(self, ctx, member: discord.Member, *, reason=None):
    #returns if target is the user, you can't ban yourself
    if member == ctx.author:
      await ctx.send("You can't ban yourself :thinking:")
      return

    try:
      await member.ban(reason=reason)
      await ctx.send(f'Member {member.mention} has been banned.')
      try:
        await member.send(f'You have been banned from {ctx.message.guild.name}.\nReason given: {reason}')
      except:
        await ctx.send(f'Could not send confirmation dm to {member.mention}')
    except:
      embed=discord.Embed(color=0xff6f00)
      embed.add_field(name="<:trserror:808530900454998026> Missing Permissions", value="It seems the bot doesn't have the permissions to perform this action.", inline=False)
      await ctx.send(embed=embed)

  @commands.command(aliases=['unblock'])
  @commands.has_permissions(ban_members = True)
  async def unban(self, ctx, *, member):

    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
      user = ban_entry.user

      if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.send(f'Unbanned {user.mention}. Welcome back!')
        return

def setup(client):
  client.add_cog(ModCommands(client))