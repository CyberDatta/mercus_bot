import os
import json


HOSD = []
HOSG = []
HOSS = []
CF = []
PERSONALITY = []


async def load_users():
    filepath = os.path.join(os.getcwd(), "db/users.json")
    with open(filepath, "r") as f:
        users = json.load(f)
        return users

async def dump_users(users):
    filepath = os.path.join(os.getcwd(), "db/users.json")
    with open(filepath, "w") as f:
        json.dump(users, f)
    return True



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

if __name__ == "__main__":
    print("you are in db interactive mode")