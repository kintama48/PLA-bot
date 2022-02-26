import datetime

import discord
from discord.ext import commands
import asyncio


class Captcha(commands.Cog, name="captcha"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="new", description="")
    @commands.has_permissions(administrator=True)
    async def new(self, ctx):
        questions = ['Boost Info?', 'Pay?', 'Delivery?']

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        index = 1
        answers = []
        question_message = None
        for question in questions:
            embed = discord.Embed(
                title="New Request ヽ(o⌣oヾ)",
                description=question,
                color=0x036bfc
            ).set_footer(icon_url=self.bot.user.avatar_url, text="Giveaway !")
            if index == 1:
                question_message = await ctx.reply(embed=embed)
            else:
                await question_message.edit(embed=embed)

            try:
                user_response = await self.bot.wait_for("message", timeout=120, check=check)
                await user_response.delete()
            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(
                    title="Error",
                    color=0x036bfc,
                    description="You took too long to answer this question"
                ))
                return
            else:
                answers.append(user_response.content)
                index += 1

        boost_info = answers[0]
        pay = answers[1]
        delivery = answers[2]