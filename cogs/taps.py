import discord
from discord.ext import commands
import db_interaction as db
import random
from discord.ui import Button, View
import time
import datetime
import pytz
import functools

async def shop(ctx, category="all"):
    user = ctx.author
    await db.open_account(ctx, user)
    items = {}

    embed = discord.Embed(title="Shop")
    if (category != "all"):
        items = await db.load_store(category)
        embed = discord.Embed(title=category)
    else:
        items = await db.load_store()
    for item in items:
        embed.add_field(name="ID", value=item, inline=True)
        embed.add_field(name="Name", value=items[item]["name"], inline=True)
        embed.add_field(name="Cost", value=items[item]["cost"], inline=True)
        embed.add_field(name="Category",
                        value=items[item]["category"], inline=True)
    await ctx.send(embed=embed)

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

class taps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1,3600,commands.BucketType.user)
    async def crime(self,ctx):
        slash_chance = 20
        slashing_rates = [100, 170]
        earning_rates = [350, 600]
        fee = 15

        await db.open_account(ctx, ctx.author)
        users = await db.load_users()
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

        await db.dump_users(users)
        await ctx.send(message)
        
    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def slut(self,ctx):
        slash_chance = 35
        slashing_rates = [200, 350]
        earning_rates = [400, 900]
        fee = 10

        await db.open_account(ctx, ctx.author)
        users = await db.load_users()
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
        await db.dump_users(users)
        await ctx.send(message)
        
    @commands.command()
    @commands.cooldown(1,3600,commands.BucketType.user)
    async def rob(self,ctx, victim: discord.Member):
        await db.open_account(ctx, ctx.author)
        await db.open_account(ctx, victim)

        users = await db.load_users()
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

        await db.dump_users(users)
        await ctx.send(f"{user.mention} tried to rob {victim.mention} and earned {robbed_value}")

    @commands.command()
    @commands.cooldown(1,4*3600,commands.BucketType.user)
    async def work(self,ctx):
        earning_rates = [400, 900]
        fee = 20
        await db.open_account(ctx, ctx.author)

        users = await db.load_users()
        user = ctx.author

        user_balance = users[str(user.id)]["mewros"]

        if (fee > user_balance):
            await ctx.send("you are a broke boi")
            return False
        earnings = random.randint(earning_rates[0], earning_rates[1])

        users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]+earnings

        await db.dump_users(users)

        await ctx.send(f"{user.mention} worked hard and earned {earnings} mewros")
        return True
    
    @commands.command()
    async def slots(self,ctx):
        fee = 30
        reward = 1000

        user = ctx.author
        await db.open_account(ctx, user)
        users = await db.load_users()

        user_balance = users[str(user.id)]["mewros"]

        if (fee > user_balance):
            await ctx.send("you are a broke boi")
            return False
        users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]-fee
        symbols = ['🍒', '🍋', '🍊', '🔔']

        result = [random.choice(symbols) for _ in range(3)]

        if result[0] == result[1] == result[2]:
            users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]+reward
            await db.dump_users(users)
            await ctx.send(f"Jackpot! You won with {result[0]} - {result[1]} - {result[2]} and got {reward} mewros")
        else:
            await db.dump_users(users)
            await ctx.send(f"Sorry, you lost. Your result was {result[0]} - {result[1]} - {result[2]}")

    @commands.command()
    async def race(self,ctx):
        user = ctx.author

        await db.open_account(ctx, user)

        users = await db.load_users()
        items = await db.load_store("race_horse")

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
            await db.dump_users(users)

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
                        await db.dump_users(users)
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

    @commands.command()
    async def blackjack(self,ctx, pool):
        pool = int(pool)
        hidden_value = ["hidden"]

        user = ctx.author
        await db.open_account(ctx, user)
        
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

            users = await db.load_users()

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

            await db.dump_users(users)

        async def hit_callback(interaction):
            users = await db.load_users()

            new_user_card = random.choice(cards)

            users[str(user.id)]["blackjack"][0].append(new_user_card)

            await db.dump_users(users)

            await finale_callback(interaction)

        async def start_game_callback(interaction):
            await interaction.message.delete()
            users = await db.load_users()

            if (users[str(user.id)]["mewros"] < pool):
                await interaction.response.send_message("You are a broke boi")
                return

            users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]-pool

            user_cards = [random.choice(cards) for _ in range(2)]
            mercus_cards = [random.choice(cards) for _ in range(2)]

            users[str(user.id)]["blackjack"] = [user_cards, mercus_cards]

            await db.dump_users(users)

            game_view = View()
            game_view.add_item(hit_button)
            game_view.add_item(bust_button)
            game_view.add_item(cash_in_button)

            await interaction.response.send_message(f"{user.mention} has these cards:{user_cards} Mercus-Bot has these cards:{hidden_value+mercus_cards[1:]}", view=game_view)

        async def exit_game_callback(interaction):
            await interaction.message.delete()
            users = await db.load_users()
            users[str(user.id)]["blackjack"] = []
            await db.dump_users(users)

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

    @commands.command()
    async def pay_ubi(self,ctx):
        user = ctx.author
        await db.open_account(ctx, user)
        
        timezone = pytz.timezone(ctx.author.timezone)
        now = datetime.datetime.now(timezone)
        if now.hour < 20 or 21 < now.hour:
            await ctx.send("UBI is only available during 8 to 9 PM")
            return

        users = await db.load_users()

        users[str(user.id)]["mewros"] = users[user]["mewros"]+500
        await db.dump_users(users)
        await ctx.send(f"{user.mention} processed") 
async def setup(bot):
    await bot.add_cog(taps(bot))

if __name__ == "__main__":
    print("you are in taps interactive mode")