# purpose of this doc is to create a json db to get data from
from discord.ext import commands, tasks
import discord
import os
import db_interaction as db

BOT_TOKEN = 'MTI4NTk1NzM3ODIzNTE3NDkyMw.GrcXBB.F01tUJZRQIzKbsEMGqFHcKWdzXM9Hdmkt1q5yE'
CHANNEL_ID = 1285960250754727988

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    await load_extensions()
    pay_weekly_bonus.start()
    pay_monthly_tax.start()
    print("the fallen leaves tell a story")

@tasks.loop(hours=168)
async def pay_weekly_bonus():
    if pay_weekly_bonus.current_loop == 0:
        return
    # Replace with your desired channel ID
    channel = bot.get_channel(CHANNEL_ID)

    users = await db.load_users()
    for user in users:
        if(users[user]["rank"] in db.HOSD):
            users[user]["mewros"] = users[user]["mewros"]+3500
        elif(users[user]["rank"] in db.HOSG):
            users[user]["mewros"] = users[user]["mewros"]+2450
        elif(users[user]["rank"] in db.HOSS):
            users[user]["mewros"] = users[user]["mewros"]+1750
        elif(users[user]["rank"] in db.CF):
            users[user]["mewros"] = users[user]["mewros"]+1575
        elif(users[user]["rank"] in db.PERSONALITY):
            users[user]["mewros"] = users[user]["mewros"]+1050        
        else:
            users[user]["mewros"] = users[user]["mewros"]+0

    await db.dump_users(users)

    await channel.send("Hello Folks, enjoy your weekly bonus of offered mewros")


@tasks.loop(hours=730)
async def pay_monthly_tax():
    if pay_monthly_tax.current_loop == 0:
        return
    tax_rate = 0.25
    # Replace with your desired channel ID
    channel = bot.get_channel(CHANNEL_ID)
    users = await db.load_users()
    for user in users:
        users[user]["mewros"] = int(
            users[user]["mewros"]-users[user]["mewros"]*tax_rate)
    await db.dump_users(users)
    await channel.send("Taxman is here to take your money!!!! HAHAHA")


@bot.event
async def on_message(message):
    
    await bot.process_commands(message)

    words = message.content.split()
    if (len(words) < 30):
        return False

    user = message.author

    await db.open_account(message, message.author, True)

    users = await db.load_users()

    users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]+15

    await db.dump_users(users)


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"{ctx.author.mention} try again, you committed error: {error}")

async def load_extensions():
    for filename in os.listdir(os.path.join(os.getcwd(),"cogs")):
        if filename.endswith(".py"): 
            if(filename=="db_interaction.py" or filename=="__init__.py"):
                continue
            cog_name = filename[:-3]  # Remove the '.py' extension
            cog = f"cogs.{cog_name}"
            try:
                await bot.load_extension(cog)
            except commands.ExtensionError as e:
                print(f"Failed to load extension {cog}: {e}")
                continue
            print(f"Successfully loaded extension {cog}")



bot.run(BOT_TOKEN)
