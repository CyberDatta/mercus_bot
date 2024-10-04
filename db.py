# purpose of this doc is to create a json db to get data from
from discord.ui import Button, View
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import json
import os
import random
import functools
import time
import datetime
import pytz

HOSD = []
HOSG = []
HOSS = []
CF = []
PERSONALITY = []

BLACKJACK=[]
SLOTS=[]
RACING=[]

BOT_TOKEN = 'MTI4NTk1NzM3ODIzNTE3NDkyMw.GrcXBB.F01tUJZRQIzKbsEMGqFHcKWdzXM9Hdmkt1q5yE'
CHANNEL_ID = 1285960250754727988

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("the fallen leaves tell a story")
    pay_weekly_bonus.start()
    pay_monthly_tax.start()


@tasks.loop(hours=168)
async def pay_weekly_bonus():
    if pay_weekly_bonus.current_loop == 0:
        return
    # Replace with your desired channel ID
    channel = bot.get_channel(CHANNEL_ID)

    users = await load_users()
    for user in users:
        if(users[user]["rank"] in HOSD):
            users[user]["mewros"] = users[user]["mewros"]+3500
        elif(users[user]["rank"] in HOSG):
            users[user]["mewros"] = users[user]["mewros"]+2450
        elif(users[user]["rank"] in HOSS):
            users[user]["mewros"] = users[user]["mewros"]+1750
        elif(users[user]["rank"] in CF):
            users[user]["mewros"] = users[user]["mewros"]+1575
        elif(users[user]["rank"] in PERSONALITY):
            users[user]["mewros"] = users[user]["mewros"]+1050        
        else:
            users[user]["mewros"] = users[user]["mewros"]+0

    await dump_users(users)

    await channel.send("Hello Folks, enjoy your weekly bonus of offered mewros")


@tasks.loop(hours=730)
async def pay_monthly_tax():
    if pay_monthly_tax.current_loop == 0:
        return
    tax_rate = 0.25
    # Replace with your desired channel ID
    channel = bot.get_channel(CHANNEL_ID)
    users = await load_users()
    for user in users:
        users[user]["mewros"] = int(
            users[user]["mewros"]-users[user]["mewros"]*tax_rate)
    await dump_users(users)
    await channel.send("Taxman is here to take your money!!!! HAHAHA")


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    words = message.content.split()
    if (len(words) < 30):
        return False

    user = message.author

    await open_account(message, message.author, True)

    users = await load_users()

    users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]+15

    await dump_users(users)


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"{ctx.author.mention} try again, you committed error: {error}")


@bot.command()
@commands.has_permissions(administrator=True)
async def remove_mewros(ctx, user: discord.Member, amount):
    amount = int(amount)
    await open_account(ctx, ctx.author)
    await open_account(ctx, user)

    users = await load_users()

    if (amount > users[str(user.id)]["mewros"]):
        await ctx.send(f"{user.name} does not have that many mewros")
        return False

    users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]-amount

    await dump_users(users)

    await ctx.send(f"{ctx.author.mention} removed {amount} mewros from {user.mention}")


@bot.command()
@commands.has_permissions(administrator=True)
async def add_mewros(ctx, user: discord.Member, amount):
    amount = int(amount)
    await open_account(ctx, ctx.author)
    await open_account(ctx, user)

    users = await load_users()

    users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]+amount

    await dump_users(users)

    await ctx.send(f"{ctx.author.mention} gifted {amount} mewros to {user.mention}")


@bot.command()
@commands.cooldown(1,3600,commands.BucketType.user)
async def crime(ctx):
    slash_chance = 20
    slashing_rates = [100, 170]
    earning_rates = [350, 600]
    fee = 15

    await open_account(ctx, ctx.author)
    users = await load_users()
    user = ctx.author

    if (users[str(user.id)]["mewros"] < fee):
        await ctx.send("you are a broke boi")
        return False

    users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]-fee

    earnings = 0
    slashings = 0
    slash_status = random.randint(0, 100)
    if (slash_status <= slash_chance):
        slashings = random.randint(slashing_rates[0], slashing_rates[1])
        message = f"{user.mention} pursued crime and lost {slashings}"
    else:
        earnings = random.randint(earning_rates[0], earning_rates[1])
        message = f"{user.mention} pursued crime and earned {earnings}"

    users[str(user.id)]["mewros"] = users[str(
        user.id)]["mewros"]+earnings-slashings

    await dump_users(users)
    await ctx.send(message)


@bot.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def slut(ctx):
    slash_chance = 35
    slashing_rates = [200, 350]
    earning_rates = [400, 900]
    fee = 10

    await open_account(ctx, ctx.author)
    users = await load_users()
    user = ctx.author

    if (users[str(user.id)]["mewros"] < fee):
        await ctx.send("you are a broke boi")
        return False

    users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]-fee

    earnings = 0
    slashings = 0
    slash_status = random.randint(0, 100)
    if (slash_status <= slash_chance):
        slashings = random.randint(slashing_rates[0], slashing_rates[1])
        message = f"{user.mention} was a slut and lost {slashings}"
    else:
        earnings = random.randint(earning_rates[0], earning_rates[1])
        message = f"{user.mention} was a slut and earned {earnings}"

    users[str(user.id)]["mewros"] = users[str(
        user.id)]["mewros"]+earnings-slashings
    await dump_users(users)
    await ctx.send(message)


@bot.command()
@commands.cooldown(1,3600,commands.BucketType.user)
async def rob(ctx, victim: discord.Member):

    await open_account(ctx, ctx.author)
    await open_account(ctx, victim)

    users = await load_users()
    user = ctx.author

    victim_balance = users[str(victim.id)]["mewros"]
    user_balance = users[str(user.id)]["mewros"]



    fail_prob = int((user_balance*100)/(victim_balance+user_balance))
    
    if(user_balance > victim_balance):
        robbed_value=(1-fail_prob/100)*victim_balance
        users[str(user.id)]["mewros"] = users[str(victim.id)]["mewros"]-robbed_value
        await ctx.send(f"{user.mention} tried to rob {victim.mention}, but lost {robbed_value}")
        return False

    fail_status = random.randint(0, 100)
    if (fail_status <= fail_prob):
        robbed_value = 0
    else:
        robbed_value = (1-fail_prob/100)*victim_balance

    users[str(victim.id)]["mewros"] = users[str(
        victim.id)]["mewros"]-robbed_value
    users[str(user.id)]["mewros"] = users[str(
        ctx.author.id)]["mewros"]+robbed_value

    await dump_users(users)

    await ctx.send(f"{user.mention} tried to rob {victim.mention} and earned {robbed_value}")


@bot.command()
@commands.cooldown(1,4*3600,commands.BucketType.user)
async def work(ctx):
    earning_rates = [400, 900]
    fee = 20
    await open_account(ctx, ctx.author)

    users = await load_users()
    user = ctx.author

    user_balance = users[str(user.id)]["mewros"]

    if (fee > user_balance):
        await ctx.send("you are a broke boi")
        return False
    earnings = random.randint(earning_rates[0], earning_rates[1])

    users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]+earnings

    await dump_users(users)

    await ctx.send(f"{user.mention} worked hard and earned {earnings} mewros")
    return True


@bot.command()
async def hello(ctx):
    user_roles = ctx.author.roles
    role_ids = [role.id for role in user_roles]
    role_names = [role.name for role in user_roles]

    response = f"Hello, {ctx.author.mention}!\nYour role IDs are: {role_ids}\nYour role names are: {role_names}"
    await ctx.send(response)


@bot.command()
async def slots(ctx):
    fee = 30
    reward = 1000

    user = ctx.author
    await open_account(ctx, user)
    users = await load_users()

    user_balance = users[str(user.id)]["mewros"]

    if (fee > user_balance):
        await ctx.send("you are a broke boi")
        return False
    users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]-fee
    symbols = ['🍒', '🍋', '🍊', '🔔']

    result = [random.choice(symbols) for _ in range(3)]

    if result[0] == result[1] == result[2]:
        users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]+reward
        await dump_users(users)
        await ctx.send(f"Jackpot! You won with {result[0]} - {result[1]} - {result[2]} and got {reward} mewros")
    else:
        await dump_users(users)
        await ctx.send(f"Sorry, you lost. Your result was {result[0]} - {result[1]} - {result[2]}")


async def find_race_winner(chance_array):

    stable = {}
    for i in range(0, len(chance_array)):
        stable[i] = chance_array[i]

    final_stable = []

    for i in range(0, 5):
        game = sum(stable.values())
        decision = random.randint(1, game)
        temp_sum = 0
        for j in stable:
            temp_sum = temp_sum + stable[j]
            if (temp_sum >= decision):
                final_stable.append(j)
                del stable[j]
                break
    return final_stable


@bot.command()
async def race(ctx):
    user = ctx.author

    await open_account(ctx, user)

    users = await load_users()
    items = await load_store("race_horse")

    check_shop = "🏪"
    check_shop_button = Button(
        label=f"Checkout the Shop", style=discord.ButtonStyle.green, emoji=check_shop)

    async def select_animal(interaction, id):
        await interaction.message.delete()

        if users[str(user.id)]["inventory"][id] == 1:
            del users[str(user.id)]["inventory"][id]
        else:
            users[str(user.id)]["inventory"][id] = users[str(
                user.id)]["inventory"][id]-1
        await dump_users(users)

        bot_racer_ids = random.sample(list(items.keys()), 4)

        user_racer = items[id]["name"]

        botracer1 = items[bot_racer_ids[0]]["name"]
        botracer2 = items[bot_racer_ids[1]]["name"]
        botracer3 = items[bot_racer_ids[2]]["name"]
        botracer4 = items[bot_racer_ids[3]]["name"]

        await interaction.response.send_message(f"Your {user_racer} competes against {botracer1}, {botracer2}, {botracer3}, and {botracer4}")

        positions = ['1st', '2nd', '3rd', '4th', '5th']

        stable = await find_race_winner([items[bot_racer_ids[0]]["rate"], items[bot_racer_ids[1]]["rate"], items[bot_racer_ids[2]]["rate"], items[bot_racer_ids[3]]["rate"], items[id]["rate"]])

        embed = discord.Embed(title="Race Results")
        time.sleep(5)
        for horse in range(0, 5):
            if (stable[horse] == 4):
                if (horse == 0):
                    users[str(user.id)]["mewros"] = users[str(
                        user.id)]["mewros"]+5*items[id]["cost"]
                    await dump_users(users)
                    await ctx.send(f"Congratulations! You won {5*items[id]['cost']} mewros")

                embed.add_field(
                    name=positions[horse], value=f"{user_racer} (player)", inline=True)
            else:
                botracer = items[bot_racer_ids[stable[horse]]]["name"]
                embed.add_field(
                    name=positions[horse], value=f"{botracer} (bot)", inline=True)

        await ctx.send(embed=embed)

    async def check_shop_callback(interaction):
        await interaction.message.delete()
        await shop(ctx, "race_horse")

    check_shop_button.callback = check_shop_callback

    initial_view = View()

    for item in users[str(user.id)]["inventory"]:
        if(items[item]["category"] !="race_horse"):
            break
        race_horse_name = items[item]["name"]

        animal = "🦑"
        animal_button = Button(
            label=f"{race_horse_name}", style=discord.ButtonStyle.green, emoji=animal)
        animal_button.callback = functools.partial(select_animal, id=item)
        initial_view.add_item(animal_button)
    initial_view.add_item(check_shop_button)

    await ctx.send("select your race horse:", view=initial_view)


@bot.command()
async def inventory(ctx, category="all"):

    user = ctx.author
    await open_account(ctx, user)
    users = await load_users()
    items = {}
    if (category != "all"):
        items = await load_store(category)
    else:
        items = await load_store()

    inventory = users[str(user.id)]["inventory"]

    embed = discord.Embed(title="Inventory")

    for item in inventory:
        if item in items:
            embed.add_field(name="ID", value=item, inline=True)
            embed.add_field(
                name="Name", value=items[item]["name"], inline=True)
            embed.add_field(name="Category",
                            value=items[item]["category"], inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def buy(ctx, item_id):
    user = ctx.author
    await open_account(ctx, user)

    users = await load_users()
    balance = users[str(user.id)]["mewros"]

    items = await load_store()
    item_name = items[item_id]["name"]
    cost = items[item_id]["cost"]

    if (cost > balance):
        await ctx.send("You are a broke boi")
        return False

    users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]-cost

    if item_id in users[str(user.id)]["inventory"]:
        users[str(user.id)]["inventory"][item_id] = users[str(
            user.id)]["inventory"][item_id]+3
    else:
        users[str(user.id)]["inventory"][item_id] = 3

    await dump_users(users)
    await ctx.send(f"Congratulations {user.mention} you are now the proud owner of a {item_name}")


@bot.command()
async def shop(ctx, category="all"):
    user = ctx.author
    await open_account(ctx, user)
    items = {}

    embed = discord.Embed(title="Shop")
    if (category != "all"):
        items = await load_store(category)
        embed = discord.Embed(title=category)
    else:
        items = await load_store()
    for item in items:
        embed.add_field(name="ID", value=item, inline=True)
        embed.add_field(name="Name", value=items[item]["name"], inline=True)
        embed.add_field(name="Cost", value=items[item]["cost"], inline=True)
        embed.add_field(name="Category",
                        value=items[item]["category"], inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def blackjack(ctx, pool):
    pool = int(pool)
    hidden_value = ["hidden"]

    user = ctx.author
    await open_account(ctx, user)
    
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    value_table = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                   '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': [1, 11]}

    start_game = "🃏"
    start_game_button = Button(
        label=f"Get Dealt a Hand (costs {pool})", style=discord.ButtonStyle.green, emoji=start_game)

    exit_game = "🇱"
    exit_game_button = Button(label="Run away (costs your dignity)",
                              style=discord.ButtonStyle.danger, emoji=exit_game)

    hit = "👊"
    hit_button = Button(
        label="Hit", style=discord.ButtonStyle.blurple, emoji=hit)

    bust = "😭"
    bust_button = Button(
        label="Bust", style=discord.ButtonStyle.gray, emoji=bust)

    cash_in = "💰"
    cash_in_button = Button(
        label="Stand", style=discord.ButtonStyle.gray, emoji=cash_in)

    def get_card_value(cards):
        value = 0
        aces = 0
        for card in cards:
            if (card == 'A'):
                aces += 1
            else:
                value += value_table[card]
        if (aces == 1):
            if (value+11 > 21):
                value += 1
            else:
                value += 11
        if (aces == 2):
            if (value+12 > 21):
                value += 2
            else:
                value += 12
        if (aces == 3):
            value = 13
        return value

    async def finale_callback(interaction):
        await interaction.message.delete()

        users = await load_users()

        user_cards = users[str(user.id)]["blackjack"][0]
        mercus_cards = users[str(user.id)]["blackjack"][1]

        user_value = get_card_value(user_cards)

        mercus_value = get_card_value(mercus_cards)
        if (mercus_value < 17):
            mercus_cards.append(random.choice(cards))
        mercus_value = get_card_value(mercus_cards)

        if (user_value > 21):
            await interaction.response.send_message(f"{user.mention} has these cards:{user_cards} Mercus-Bot has these cards:{mercus_cards}, You have lost!!!")
        elif (mercus_value > 21):
            await interaction.response.send_message(f"{user.mention} has these cards:{user_cards} Mercus-Bot has these cards:{mercus_cards}, You have Won {2*pool} mewros!!!")
            users[str(user.id)]["mewros"] = users[str(
                user.id)]["mewros"] + 2*pool
        elif (mercus_value >= user_value):
            await interaction.response.send_message(f"{user.mention} has these cards:{user_cards} Mercus-Bot has these cards:{mercus_cards}, You have lost!!!")
        else:
            await interaction.response.send_message(f"{user.mention} has these cards:{user_cards} Mercus-Bot has these cards:{mercus_cards}, You have Won {2*pool} mewros!!!")
            users[str(user.id)]["mewros"] = users[str(
                user.id)]["mewros"] + 2*pool
        users[str(user.id)]["blackjack"] = []

        await dump_users(users)

    async def hit_callback(interaction):
        users = await load_users()

        new_user_card = random.choice(cards)

        users[str(user.id)]["blackjack"][0].append(new_user_card)

        await dump_users(users)

        await finale_callback(interaction)

    async def start_game_callback(interaction):
        await interaction.message.delete()
        users = await load_users()

        if (users[str(user.id)]["mewros"] < pool):
            await interaction.response.send_message("You are a broke boi")
            return

        users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]-pool

        user_cards = [random.choice(cards) for _ in range(2)]
        mercus_cards = [random.choice(cards) for _ in range(2)]

        users[str(user.id)]["blackjack"] = [user_cards, mercus_cards]

        await dump_users(users)

        game_view = View()
        game_view.add_item(hit_button)
        game_view.add_item(bust_button)
        game_view.add_item(cash_in_button)

        await interaction.response.send_message(f"{user.mention} has these cards:{user_cards} Mercus-Bot has these cards:{hidden_value+mercus_cards[1:]}", view=game_view)

    async def exit_game_callback(interaction):
        await interaction.message.delete()
        users = await load_users()
        users[str(user.id)]["blackjack"] = []
        await dump_users(users)

        await interaction.response.send_message("see you later loser")

    exit_game_button.callback = exit_game_callback
    start_game_button.callback = start_game_callback
    hit_button.callback = hit_callback
    bust_button.callback = exit_game_callback
    cash_in_button.callback = finale_callback

    initial_view = View()
    initial_view.add_item(start_game_button)
    initial_view.add_item(exit_game_button)
    await ctx.send(view=initial_view)


@bot.command()
async def leaderboard(ctx):
    user = ctx.author

    await open_account(ctx, user)

    users = await load_users()

    sorted_items = sorted(
        users.items(), key=lambda x: x[1]['mewros'], reverse=True)
    sorted_values = [[item[0], item[1]["mewros"]] for item in sorted_items]

    leaderboard_message = "**Leaderboard**\n"
    
    limit=0
    for i in range(len(sorted_values)):
        if(limit==15):
            break
        limit=limit + 1
        if (users[sorted_values[i][0]]["visible"]=="False"):
            continue
        leaderboard_message += f"{i+1}. {users[sorted_values[i][0]]['name']}\n"
    await ctx.send(leaderboard_message)


@bot.command()
async def give_mewros(ctx, payee: discord.Member, amount):
    amount = int(amount)
    benefactor = ctx.author
    await open_account(ctx, benefactor)
    await open_account(ctx, payee)

    users = await load_users()

    benefactor_balance = users[str(benefactor.id)]["mewros"]

    if (benefactor_balance < amount):
        await ctx.send(f"Transaction from {benefactor.mention} to {payee.mention} for {amount} mewros rejected due to insufficient mewros")
        return False
    else:
        users[str(benefactor.id)]["mewros"] = benefactor_balance-amount
        users[str(payee.id)]["mewros"] = users[str(payee.id)]["mewros"]+amount
        await dump_users(users)
        await ctx.send(f"Transaction from {benefactor.mention} to {payee.mention} for {amount} mewros is successful")


@bot.command()
async def mewros(ctx):
    user = ctx.author
    await open_account(ctx, user)
    users = await load_users()
    balance = users[str(user.id)]["mewros"]
    em = discord.Embed(title=f"For {user.name}", color=discord.Color.red())
    em.add_field(name="Balance:", value=f"{str(balance)} mewros")

    await ctx.send(embed=em)


@bot.command()
async def pay_ubi(ctx):
    user = ctx.author
    await open_account(ctx, user)
    
    timezone = pytz.timezone(ctx.author.timezone)
    now = datetime.datetime.now(timezone)
    if now.hour < 20 or 21 < now.hour:
        await ctx.send("UBI is only available during 8 to 9 PM")
        return

    users = await load_users()

    users[str(user.id)]["mewros"] = users[user]["mewros"]+500
    await dump_users(users)
    await ctx.send(f"{user.mention} processed")

@bot.command()
async def gmintern(ctx):
    user = ctx.author
    await open_account(ctx, user, message_status=False,gmintern=True)
    await ctx.send(f"{user.mention} has unlocked mercus bot")
    
    
@bot.command()
async def visible(ctx):
    user = ctx.author
    await open_account(ctx, user, message_status=False,gmintern=True)
    
    users=await load_users()
    status="False"
    if(users[str(user.id)]["visible"] == "False"):
        users[str(user.id)]["visible"] = "True"
        status="True"
    else:
        users[str(user.id)]["visible"] = "False"
        status="False"
    
    await dump_users(users)
    await ctx.send(f"For {user.mention}, is visible on leaderboard: {status}")

    
@bot.command()
async def update_role(ctx):
    user = ctx.author
    await open_account(ctx, user, message_status=False,gmintern=True)
    
    users=await load_users()
    roles=user.roles
    role_ids = [role.id for role in roles]
        
    users[str(user.id)]["rank"] = 0
    if HOSD[0] in role_ids:
        users[str(user.id)]["rank"] = HOSD[0]
    elif HOSG[0] in role_ids:
        users[str(user.id)]["rank"] = HOSG[0]
    elif HOSS[0] in role_ids:
        users[str(user.id)]["rank"] = HOSS[0]
    elif CF[0] in role_ids:
        users[str(user.id)]["rank"] = CF[0]
    else:
        for person in PERSONALITY:
            if person in role_ids:
                users[str(user.id)]["rank"] = person
    await dump_users(users)
    await ctx.send("Rank Logged")

async def open_account(ctx, user, message_status=False,gmintern=True):
    if(gmintern==False):
        await ctx.send("You must use the gmintern command")        
    
    users = await load_users()
    
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["mewros"] = 500
        users[str(user.id)]["name"] = user.name
        users[str(user.id)]["visible"] = "True"
        users[str(user.id)]["inventory"] = {}
        
        roles=user.roles
        role_ids = [role.id for role in roles]
        
        users[str(user.id)]["rank"] = 0
        if HOSD[0] in role_ids:
            users[str(user.id)]["rank"] = HOSD[0]
        elif HOSG[0] in role_ids:
            users[str(user.id)]["rank"] = HOSG[0]
        elif HOSS[0] in role_ids:
            users[str(user.id)]["rank"] = HOSS[0]
        elif CF[0] in role_ids:
            users[str(user.id)]["rank"] = CF[0]
        else:
            for person in PERSONALITY:
                if person in role_ids:
                    users[str(user.id)]["rank"] = person

    await dump_users(users)
    if (message_status == False):
        await ctx.send(f"Opened a Mewro acccount for {user.mention}")
    else:
        await ctx.channel.send(f"Opened a Mewro acccount for {user.mention}")
    return True


async def load_users():
    filepath = os.path.join(os.getcwd(), "db/users.json")
    with open(filepath, "r") as f:
        users = json.load(f)
        return users


async def load_store(category="all"):
    filepath = os.path.join(os.getcwd(), "db/store.json")
    with open(filepath, "r") as f:
        store = json.load(f)
        if (category == "all"):
            return store
        else:
            section = {}
            for item in store:
                if (store[item]['category'] == category):
                    section[item] = store[item]
            return section


async def dump_users(users):
    filepath = os.path.join(os.getcwd(), "db/users.json")
    with open(filepath, "w") as f:
        json.dump(users, f)
    return True


bot.run(BOT_TOKEN)
