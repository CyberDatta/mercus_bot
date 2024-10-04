from discord.ext import commands, tasks
import discord
from discord.ui import Button,View
from dataclasses import dataclass
import datetime

MAX_SESSION_TIME_MINUTES = 1
BOT_TOKEN = 'MTI4NTk1NzM3ODIzNTE3NDkyMw.GrcXBB.F01tUJZRQIzKbsEMGqFHcKWdzXM9Hdmkt1q5yE'
CHANNEL_ID = 732450603627839582


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("hello what is up")
    channel = bot.get_channel(CHANNEL_ID)
    # await channel.send("horray this works")




@bot.command()
async def blackjack(ctx):
    cost=100
    # await ctx.send("Start Command Template")
    cards = ['2', '3', '4', '5','6','7','8','9','10','J','Q','K','A']
    value_table={'2':2, '3':3, '4':4, '5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10,'A':[1,11]}
    
    start_game="🃏"
    button1=Button(label="Get Dealt a Hand (costs 100)",style=discord.ButtonStyle.green,emoji=start_game)    
    
    exit_game="🇱"
    button2=Button(label="Run away like a coward (costs your dignity)",style=discord.ButtonStyle.danger,emoji=exit_game)
    
    
    view=View()
    view.add_item(button1)
    view.add_item(button2)
    await ctx.send(view=view)
bot.run(BOT_TOKEN)