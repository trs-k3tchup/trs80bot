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
gamerwords = [
  'game',
  'gamer',
  'gaming',
  'play',
  'mlg',
  'noscope',
  'high score',
  'new record'
]
fortnitewords = [
  'chug jug',
  'victory royal',
  'fortnite'
]
mcwords = [
  'minecraft',
  'creeper',
  'blocks',
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
        'ඞ Red sus. Red suuuus. I said red, sus, hahahahaha. Why arent you laughing? I just made a reference to the popular video game "Among Us"! How can you not laugh at it? Emergeny meeting! Guys, this here guy doesnt laugh at my funny Among Us memes! Lets beat him to death! Dead body reported! Skip! Skip! Vote blue! Blue was not an impostor. Among us in a nutshell hahahaha. What?! Youre still not laughing your ass off? I made SEVERAL funny references to Among Us and YOU STILL ARENT LAUGHING??!!! Bruh. Ya hear that? Wooooooosh. Whats woooosh? Oh, nothing. Just the sound of a joke flying over your head. Whats that? You think im annoying? Kinda sus, bro. Hahahaha! Anyway, yea, gotta go do tasks. Hahahaha!',
        'kinda sus, ngl'
      ]

      #reacts to message with emoji
      await message.add_reaction('<:sus:822657346467659776>')
      
      #has a 66% chance to reply with a randomly generated response
      x = random.randint(1,3)
      if x <= 2:
        await message.reply(random.choice(responses))
      
      return

    #responds to gamer words
    if any (word in msg for word in gamerwords):
      responses = [
        'What an epic gamer!',
        'You must have a really good gamer chair',
        'gaming',
        'I too am an epic gamer :sunglasses:',
        'I liek to play video gaem'
      ]

      #reacts to message with emoji
      await message.add_reaction('<:progamer:822668119649550356>')
      
      #has a 66% chance to reply with a randomly generated response
      x = random.randint(1,3)
      if x <= 2:
        await message.reply(random.choice(responses))
      
      return

    #responds to fortnite words
    if any (word in msg for word in fortnitewords):
      responses = [
        'Will you be my pro fortnite gamer?',
        'I play fortnite all night long',
        'Gotta get that victory royale'
      ]

      #reacts to message with emoji
      await message.add_reaction('<:fertnite:822804481166934046>')
      
      #has a 66% chance to reply with a randomly generated response
      x = random.randint(1,3)
      if x <= 2:
        await message.reply(random.choice(responses))
      
      return

    #responds to minecraft words
    if any (word in msg for word in mcwords):
      responses = [
        'creeper',
        'https://www.youtube.com/watch?v=ocMmjhe_C5g&t=38s',
        'i saw herobrine!! :flushed:',
        'cave update when?'
      ]

      #reacts to message with emoji
      await message.add_reaction('<:stevedab:822806828143476738>')
      
      #has a 66% chance to reply with a randomly generated response
      x = random.randint(1,3)
      if x <= 2:
        await message.reply(random.choice(responses))
      
      return

def setup(client):
  client.add_cog(Auto(client))