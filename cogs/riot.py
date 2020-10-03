import json
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError


with open("source/config.json") as s:
    settings = json.load(s)
    owner_id = settings["config"]["owner_id"]
    riot_api_key = settings["api"]["riot_api"]
    lol = LolWatcher(riot_api_key)


async def is_owner(ctx):
    return ctx.author.id == owner_id


class Riot(commands.Cog, name="Riot API"):

    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Riot cog is ready.")

    @commands.command()
    async def summoner(self, ctx, region, summoner_name):
        "Summoner info."
        summoner_info = lol.summoner.by_name(region, summoner_name)
        await ctx.send(f"```apache\nName: {summoner_info['name']}\nLevel: {summoner_info['summonerLevel']}\n```")


def setup(bot):
    bot.add_cog(Riot(bot))
