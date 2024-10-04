import discord
from discord.ext import commands
import db_interaction as db


class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="!inventory or !inventory category")
    async def inventory(self,ctx, category="all"):

        user = ctx.author
        await db.open_account(ctx, user)
        users = await db.load_users()
        items = {}
        if (category != "all"):
            items = await db.load_store(category)
        else:
            items = await db.load_store()

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


    @commands.command(help="!shop or !shop category")
    async def shop(self,ctx, category="all"):
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
            embed.add_field(name="ID", value=item, inline=False)
            embed.add_field(name="Name", value=items[item]["name"], inline=True)
            embed.add_field(name="Cost", value=items[item]["cost"], inline=True)
            embed.add_field(name="Category",
                            value=items[item]["category"], inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(help="!leaderboard or !leaderboard position")
    async def leaderboard(self,ctx,position=15):
        user = ctx.author

        await db.open_account(ctx, user)

        users = await db.load_users()

        sorted_items = sorted(
            users.items(), key=lambda x: x[1]['mewros'], reverse=True)
        sorted_values = [[item[0], item[1]["mewros"]] for item in sorted_items]

        leaderboard_message = "**Leaderboard**\n"
        
        limit=0
        for i in range(len(sorted_values)):
            if(limit==position):
                break
            limit=limit + 1
            if (users[sorted_values[i][0]]["visible"]=="False"):
                continue
            leaderboard_message += f"{i+1}. {users[sorted_values[i][0]]['name']}\n"
        await ctx.send(leaderboard_message)

    @commands.command(help="!give_mewros @user amount")
    async def give_mewros(self,ctx, payee: discord.Member, amount):
        amount = int(amount)
        benefactor = ctx.author
        await db.open_account(ctx, benefactor)
        await db.open_account(ctx, payee)
        users = await db.load_users()
        benefactor_balance = users[str(benefactor.id)]["mewros"]
        if (benefactor_balance < amount):
            await ctx.send(f"Transaction from {benefactor.mention} to {payee.mention} for {amount} mewros rejected due to insufficient mewros")
            return False
        else:
            users[str(benefactor.id)]["mewros"] = benefactor_balance-amount
            users[str(payee.id)]["mewros"] = users[str(payee.id)]["mewros"]+amount
            await db.dump_users(users)
            await ctx.send(f"Transaction from {benefactor.mention} to {payee.mention} for {amount} mewros is successful")

    @commands.command(help="!mewros")
    async def mewros(self,ctx):
        user = ctx.author
        await db.open_account(ctx, user)
        users = await db.load_users()
        balance = users[str(user.id)]["mewros"]
        em = discord.Embed(title=f"For {user.name}", color=discord.Color.red())
        em.add_field(name="Balance:", value=f"{str(balance)} mewros")
        await ctx.send(embed=em)       
        
    @commands.command(help="!gmintern")
    async def gmintern(self,ctx):
        user = ctx.author
        await db.open_account(ctx, user, message_status=False,gmintern=True)
        await ctx.send(f"{user.mention} has unlocked mercus bot")
    
    @commands.command(help="!visible")
    async def visible(self,ctx):
        user = ctx.author
        await db.open_account(ctx, user, message_status=False,gmintern=True)
        
        users=await db.load_users()
        status="False"
        if(users[str(user.id)]["visible"] == "False"):
            users[str(user.id)]["visible"] = "True"
            status="True"
        else:
            users[str(user.id)]["visible"] = "False"
            status="False"
        
        await db.dump_users(users)
        await ctx.send(f"For {user.mention}, is visible on leaderboard set to: {status}")
        
    @commands.command(help="!update_role")
    async def update_role(self,ctx):
        user = ctx.author
        await db.open_account(ctx, user, message_status=False,gmintern=True)
        
        users=await db.load_users()
        roles=user.roles
        role_ids = [role.id for role in roles]
            
        users[str(user.id)]["rank"] = 0
        if db.HOSD[0] in role_ids:
            users[str(user.id)]["rank"] = db.HOSD[0]
        elif db.HOSG[0] in role_ids:
            users[str(user.id)]["rank"] = db.HOSG[0]
        elif db.HOSS[0] in role_ids:
            users[str(user.id)]["rank"] = db.HOSS[0]
        elif db.CF[0] in role_ids:
            users[str(user.id)]["rank"] = db.CF[0]
        else:
            for person in db.PERSONALITY:
                if person in role_ids:
                    users[str(user.id)]["rank"] = person
        await db.dump_users(users)
        await ctx.send("Rank Logged")
        
async def setup(bot):
    await bot.add_cog(economy(bot))
    
    
if __name__ == "__main__":
    print("you are in economy interactive mode")