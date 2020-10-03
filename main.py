import os
import json
import random
import discord
from discord.ext import commands, tasks


# Load config file.
with open("source/config.json", encoding='utf-8') as s:
    settings = json.load(s)


# Variables
token = settings["config"]["token"]
prefix = settings["config"]["prefix"]
owner_id = settings["config"]["owner_id"]
bot = commands.Bot(command_prefix=prefix, owner_id=owner_id)


async def record_commands(ctx):  # Record and print the commands to console.
    print(f"{ctx.author} used a command. ==> {ctx.command}")


async def is_owner(ctx):
    return ctx.author.id == owner_id


def random_game():
    return random.choice(settings["games"])


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random_game()))
    splash = open("source/splash.txt", mode="r", encoding="ascii")
    s_art = splash.read()
    print(f"{s_art}")
    splash.close()
    print(f"{bot.user.name} - {bot.user.discriminator}")
    print(f"ID: {bot.user.id}")
    print("-----------------------------")


@bot.group()
async def cog(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send_help("cog")


@cog.command()
@commands.check(is_owner)
@commands.before_invoke(record_commands)
async def load(ctx, extension):
    """Loads the cog"""
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"**{extension.capitalize()}** loaded.")
    # Write to json file.
    _load = {"cogs": {extension: "loaded"}}
    with open("source/cogs.json", "w+") as conf:
        json.dump(_load, conf, indent=4, sort_keys=True)
    # with open("source/cogs.json", "w+") as load:
    #     _load = json.load(load)
    #     _load["cogs"][extension] = "loaded"
    #     unload.seek(0)
    #     json.dump(_load, load, indent=4, sort_keys=True)
    #     load.truncate()


@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing argument.")


@cog.command()
@commands.check(is_owner)
@commands.before_invoke(record_commands)
async def unload(ctx, extension):
    """Unloads the cog"""
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"**{extension.capitalize()}** unloaded.")
    # Edit JSON file.
    with open("source/cogs.json", "w+") as unload:
        _unload = json.load(unload)
        _unload["cogs"][extension] = "unloaded"
        unload.seek(0)
        json.dump(_unload, unload, indent=4, sort_keys=True)
        unload.truncate()


@unload.error
async def unload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing argument.")


@cog.command(aliases=["restart"])
@commands.check(is_owner)
@commands.before_invoke(record_commands)
async def reload(ctx, extension):
    """Reloads the cog"""
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded **{extension.capitalize()}** cog.")


@reload.error
async def unload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing argument.")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"There is no cog named like that.")


@cog.command(name="list")
@commands.check(is_owner)
@commands.before_invoke(record_commands)
async def cogs(ctx):
    """Lists available cogs"""
    cog_list = list()
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_list.append(filename[:-3])

    if len(cog_list) >= 2:
        await ctx.send(f"There are {len(cog_list)} cogs.")
        capital = [cog.capitalize() for cog in cog_list]
        await ctx.send("Cogs: {}".format(", ".join(capital)))

    elif len(cog_list) == 0:
        await ctx.send("There are no cogs.")

    else:
        await ctx.send(f"There is {len(cog_list)} cog.")
        await ctx.send(*cog_list)


@bot.command(aliases=["close"])
@commands.check(is_owner)
@commands.before_invoke(record_commands)
async def shutdown(ctx):
    await ctx.send("Cya! Shutting down the bot.")
    await bot.close()


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        # Cut last three characters. (Exclude the ".py" at the end of the file)
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(token)
