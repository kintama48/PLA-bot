import datetime

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import asyncio
import json
import os
import random
import sys
from googleapiclient.discovery import build


if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

google_api_key = "AIzaSyCvde8W6fc5B87Qg6VqX8sbJROMPQ-nwqw"


class Games(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dailyfact", description="Gives a daily fact to every user if called ")
    @commands.cooldown(1, 86400, BucketType.user)
    async def dailyfact(self, context):  # dailyfact command can be executed only once per day per user
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=f"**{data['text']}** ヽ(o⌣oヾ)", color=0x8233FF)
                    await context.reply(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error",
                        description="I failed to get a new fact for you ( ´◡`)",
                        color=0xE02B2B
                    )
                    await context.send(embed=embed)
                    self.dailyfact.reset_cooldown(context)

    @commands.command(name="show", description="Searches for an image on Google")
    async def show(self, ctx, search):
        ran = random.randint(0, 9)
        resource = build("customsearch", "v1", developerKey=google_api_key).cse()
        result = resource.list(
            q=f"{search}", cx="<YOUR SEARCH ENGINE ID>", searchType="image"
        ).execute()
        url = result["items"][ran]["link"]
        embed1 = discord.Embed(title=f"I found this for you on Google ヘ(♥﹏♥ヘ)")
        embed1.set_image(url=url)
        await ctx.reply(embed=embed1)

    @commands.command(name="hug", description="Hugs back")
    async def hug(self, context):
        await context.reply(embed=discord.Embed(title=f"{context.author.mention} * hugs back * ＼( ^o^ )／"))

    @commands.command(name="roll", description="Rolls a dice")
    async def roll(self, context):
        await context.reply(content=f"🎲 Rolled a dice for you ( ^_^ )\n\n*You got {random.randint(1, 6)}*")

    @commands.command(name="rpc", description="Play rock paper scissors with the bot")
    async def rock_paper_scissors(self, context):
        choices = {
            0: "rock",
            1: "paper",
            2: "scissors"
        }
        reactions = {
            "🪨": 0,
            "🧻": 1,
            "✂": 2
        }
        embed = discord.Embed(title="Please choose", color=0xDC33FF)
        embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
        choose_message = await context.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == context.message.author and str(reaction) in reactions

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            bot_choice_emote = random.choice(list(reactions.keys()))
            bot_choice_index = reactions[bot_choice_emote]

            result_embed = discord.Embed(color=0x42F56C)
            result_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.clear_reactions()

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0xF59E42
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            else:
                result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0xE02B2B
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = discord.Embed(title="Too late", color=0xE02B2B)
            timeout_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.edit(embed=timeout_embed)


def setup(bot):
    bot.add_cog(Games(bot))
