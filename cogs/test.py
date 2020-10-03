import json
import discord
import asyncio
import time
from random import choice
from discord.ext import commands


with open("source/config.json") as s:
    settings = json.load(s)


async def is_owner(ctx):
    return ctx.author.id == owner_id


class Test(commands.Cog, name="Test"):

    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_ready(self):
        #name = commands.Command.cog_name
        print(f"Test cog is ready.")

    @commands.command()
    async def ping(self, ctx):
        "Show the ping of the bot."
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    @commands.command(name="test")
    async def _test(self, ctx, *arguments):
        "This is a test command."
        await ctx.send(f"You passed {len(arguments)} arguments. {arguments}")

    @commands.command(name="game")
    # Add status to arguments. Like watching and streaming.
    async def change_game(self, ctx, status, *, game):
        if status == "watch":
            await self.client.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.watching))
        elif status == "listen":
            await self.client.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.listening))
        elif status == "play":
            await self.client.change_presence(activity=discord.Game(name=game))

    @change_game.error
    async def game_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing argument.")  # or await ctx.send(error)


def setup(bot):
    bot.add_cog(Test(bot))
