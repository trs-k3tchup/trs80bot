import discord
from discord.ext import commands
import random

#ext contains code for autoresponses
#most code is in the @commnds.Cog.listener witch triggers everytime a message is sent

#variables
suswords = [
  'sus',
  'suspicious',
  'impostor',
  'imposter',
  'eject',
  'ejected',
  'vote',
  'voted',
  'among',
  'among us',
  'amogus',
  'sabotage',
  'crewmate',
  'task',
  'tasks',
  'meeting',
]

class Auto(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_message(self, message):
    #clean_content ignores all user/channel mentions, but not links or emojis :(
    msg = message.clean_content
    cntnt = message.content

    #makes it so that the bot will not trigger it's own autoresponse
    if message.author == self.client.user:
      return
    
    #dadbot responses are to be added here as soon as i figure them out

    #responds to sus words
    if any (word in msg for word in suswords):
      responses = [
        'When the impostor is sus! :flushed:',
        'amogus',
        'haha like in among us!!',
        "That's kinda sussy bro :flushed:",
        'kinda sus, ngl',
        "ooh you're so sussy I know you took my fortnite card"
      ]

      #reacts to message with emoji
      await message.add_reaction('<:sus:822657346467659776>')
      
      #has a 66% chance to reply with a randomly generated response
      x = random.randint(1,3)
      if x <= 2:
        await message.reply(random.choice(responses))
      
      return

def setup(client):
  client.add_cog(Auto(client))