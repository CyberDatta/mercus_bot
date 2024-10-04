import discord
from discord.ext import commands
import db_interaction as db

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="!remove_mewros @user amount")
    @commands.has_permissions(administrator=True)
    async def remove_mewros(self,ctx, user: discord.Member, amount):
        amount = int(amount)
        await db.open_account(ctx, ctx.author)
        await db.open_account(ctx, user)

        users = await db.load_users()

        if (amount > users[str(user.id)]["mewros"]):
            await ctx.send(f"{user.name} does not have that many mewros")
            return False

        users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]-amount
        await db.dump_users(users)
        await ctx.send(f"{ctx.author.mention} removed {amount} mewros from {user.mention}")


    @commands.command(help="!add_mewros @user amount") 
    @commands.has_permissions(administrator=True)
    async def add_mewros(self,ctx, user: discord.Member, amount):
        amount = int(amount)
        await db.open_account(ctx, ctx.author)
        await db.open_account(ctx, user)

        users = await db.load_users()

        users[str(user.id)]["mewros"] = users[str(user.id)]["mewros"]+amount

        await db.dump_users(users)

        await ctx.send(f"{ctx.author.mention} gifted {amount} mewros to {user.mention}")
async def setup(bot):
    await bot.add_cog(admin(bot))

if __name__ == "__main__":
    print("you are in admin interactive mode")