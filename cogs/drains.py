from discord.ext import commands
import db_interaction as db

class drains(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="!buy item-id")
    async def buy(self,ctx, item_id):
        user = ctx.author
        await db.open_account(ctx, user)

        users = await db.load_users()
        balance = users[str(user.id)]["mewros"]

        items = await db.load_store()
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

        await db.dump_users(users)
        await ctx.send(f"Congratulations {user.mention} you are now the proud owner of a {item_name}")

async def setup(bot):
    await bot.add_cog(drains(bot))
    
if __name__ == "__main__":
    print("you are in drains interactive mode")