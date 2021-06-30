import discord
from discord.ext import commands
import json
import os
import random

class Eco(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #function to load a user's bank data
    async def getbankdata(self):
        with open("./json/bank.json","r") as f:
            users = json.load(f)
    
        return users
    
    #function to check if a user has an account
    async def checkuser(self, user):
        users = await self.getbankdata(user)

        if str(user.id) in users:
            return True
        else:
            return False
    
    #function to battle user with NPC
    async def npcBattle(self, user, eHP, eSTR, eDEF, eDEX):
        users = await self.getbankdata
        
        h = users[str(user.id)]["health"]
        s = users[str(user.id)]["strength"]
        df = users[str(user.id)]["defense"]
        dx = users[str(user.id)]["dexterity"]

        bob = 0

        uChance = round((dx / eDEF) * 100)
        if uChance > 100:
            uChance = 100
        
        eChance = round((eDEX / df) * 100)
        if eChance > 100:
            eChance = 100

        uDmg = s - eDEF
        eDmg = eSTR - df

        while bob <= 30:
            num = random.randint(1, 100)
            if num <= uChance:
                eHP -= uDmg
            if eHP <= 0:
                break
            
            if num <= uChance:
                h -= eDmg
            if h <= 0:
                break
            
            bob += 1
        
        if eHP <= 0:
            return "win"
        elif h <= 0:
            return "lose"
        else:
            return "draw"
    
    #command to create an account for the user
    @commands.command(aliases=["rpgstart"])
    async def _start(self, ctx):
        user = ctx.author
        users = await self.getbankdata()

        #returns error if the user already has an account, else create account
        if str(user.id) in users:
            await ctx.reply("You already have an account!")
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["health"] = 100
            users[str(user.id)]["maxHealth"] = 100
            users[str(user.id)]["exp"] = 0
            users[str(user.id)]["maxExp"] = 100
            users[str(user.id)]["level"] = 1
            users[str(user.id)]["wallet"] = 50
            users[str(user.id)]["strength"] = 10
            users[str(user.id)]["defense"] = 10
            users[str(user.id)]["dexterity"] = 10
            users[str(user.id)]["statPoint"] = 1
        
        #dump all the new data in the json file
        with open("./json/bank.json", "w") as f:
            json.dump(users, f)
        
        await ctx.reply("Your account has been successfully created!")
    
    #command to check your profile
    @commands.command(aliases=["rpgme"])
    async def _rpgme(self, ctx):
        user = ctx.author
        users = await self.getbankdata()
        check = await self.checkuser(user)
        if not check:
            await ctx.reply("You do not have an account yet! Create one with `trs-rpgstart`")
            return
        
        h = users[str(user.id)]["health"]
        mh = users[str(user.id)]["maxHealth"]
        l = users[str(user.id)]["level"]
        ex = users[str(user.id)]["exp"]
        mex = users[str(user.id)]["maxExp"]
        m = users[str(user.id)]["wallet"]
        s = users[str(user.id)]["strength"]
        df = users[str(user.id)]["defense"]
        dx = users[str(user.id)]["dexterity"]
        sp = users[str(user.id)]["statPoint"]

        embed=discord.Embed(color=0xff6f00)
        embed.set_author(name=f"{user.diplay_name}'s RPG Info")
        embed.add_field(name="Level", value=f"{l}", inline=True)
        embed.add_field(name="Exp", value=f"{ex}/{mex}", inline=True)
        embed.add_field(name="Health", value=f"{h}/{mh}", inline=False)
        embed.add_field(name="Money", value=f"{m}", inline=False)
        embed.add_field(name="STR", value=f"{s}", inline=True)
        embed.add_field(name="DEF", value=f"{df}", inline=True)
        embed.add_field(name="DEX", value=f"{dx}", inline=True)
        embed.add_field(name="Stat Points", value=f"{sp}", inline=False)
        await ctx.send(embed=embed)

    #hunt command yes yes
    @commands.command(aliases=["hunt"])
    async def _hunt(self, ctx):
        user = ctx.author
        users = await self.getbankdata()
        check = await self.checkuser(user)
        if not check:
            await ctx.reply("You do not have an account yet! Create one with `trs-rpgstart`")
            return
        
        h = users[str(user.id)]["health"]
        mh = users[str(user.id)]["maxHealth"]
        l = users[str(user.id)]["level"]
        ex = users[str(user.id)]["exp"]
        mex = users[str(user.id)]["maxExp"]
        m = users[str(user.id)]["wallet"]
        s = users[str(user.id)]["strength"]
        df = users[str(user.id)]["defense"]
        dx = users[str(user.id)]["dexterity"]
        sp = users[str(user.id)]["statPoint"]

        #ENEMY GENERATION
        #an enemy is generated with a level
        #at most 5 lvls above player 
        #and at least 10 lvls below.
        
        if l <= 10:
            enemyLvl = random.randint(1, l +1)
        else:
            enemyLvl = random.randint(l - 10, l + 5)
        
        enemySP = 30 + enemyLvl
        enemyDEF = random.randint(10, dx)
        enemySTR = round((enemySP - enemyDEF) * random.randint(1, 100) * 0.01)
        enemyDEX = enemySP - (enemyDEF + enemySTR)
        enemyHealth = 100 + (enemyLvl * 10)

        embed=discord.Embed(color=0xff6f00)
        embed.set_author(name="You encountered an enemy!")
        embed.add_field(name="Level", value="{enemyLvl}", inline=False)
        embed.add_field(name="Health", value="{enemyHealth}", inline=False)
        embed.add_field(name="STR", value="{enemySTR}", inline=True)
        embed.add_field(name="DEF", value="{enemyDEF}", inline=True)
        embed.add_field(name="DEX", value="{enemyDEX}", inline=True)
