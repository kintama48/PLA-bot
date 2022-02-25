import json
import os
import sys

import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    # ping a bot to check if it's alive or not
    @commands.command(name="ping", description="Check if the bot is alive")
    async def ping(self, context):
        embed = discord.Embed(
            title="🏓 Pong (◕‿◕)",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0xD5059D
        )
        await context.reply(embed=embed)

    # makes bot say whatever u want
    @commands.command(name="say", description="Makes bot say whatever you want")
    async def say(self, context, message):
        try:
            await context.reply(content=f"{message} (′ꈍωꈍ‵)")
        except discord.Forbidden:
            await context.send(content=f"{message} (′ꈍωꈍ‵)")

    # makes bot say whatever u want in an embed
    @commands.command(name="embed", description="Makes bot say whatever u want in an embed")
    async def say_embed(self, context, message):
        embed = discord.Embed(
            description=f"{message} ⎝⊜ω⊜⎠",
            color=0xD5059D
        )
        try:
            await context.reply(embed=embed)
        except discord.Forbidden:
            await context.reply(embed=embed)

    # give role
    @commands.command(name="addrole", description="Give role to a member")
    async def add_role(self, context, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await context.reply(
            embed=discord.Embed(description=f"`{member.display_name}` has been given role: **{role.name}** ◕ᗜ◕",
                                color=0xD5059D))


def setup(bot):
    bot.add_cog(general(bot))
