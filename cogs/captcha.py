import datetime

import discapty
import discord
from discord.ext import commands
import asyncio


class Captcha(commands.Cog, name="captcha"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="verifymsg")
    @commands.has_permissions(administrator=True)
    async def verifymsg(self, ctx):
        await ctx.send(embed=discord.Embed(
            title="Welcome to Boosting Academy",
            description="\n**Guidelines**\n"
                        "• Don't beg for free boosts\n"
                        "• Don't spam tickets\n"
                        "• If staff aren't online, do not spam, wait until they are active\n"
                        "• No asking for booster role, we will create applications if we are in need\n"
                        "• If you need support, create a ticket in <#831337959961264149> and staff will further assist you\n"
                        "• No mentioning the **@Support Team**\n"
                        "• No illegal content\n"
                        "• 2 **Warns** = Perm **Ban**\n\n"
                        "**How to Verify**\n"
                        "• Please use the `-verify` command in <#946819028570210325> channel. Our bot will send you a **captcha**\n"
                        "• Upon solving the captcha, you'll be **verified**",
            color=0x036bfc,
            timestamp=datetime.datetime.now()
        ))

    @staticmethod
    async def delete_msgs(queue):
        for i in queue:
            try:
                await i.delete()
            except:
                continue

    @commands.command(name='verify', description="Gives you a Captcha")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def verify(self, ctx):
        role = 831334682858750042
        if role in [role.id for role in ctx.author.roles]:
            await ctx.reply(content=ctx.author.mention, embed=discord.Embed(
                    title="You are already **verified**!"))
            return
        captcha = discapty.Captcha("wheezy")
        captcha_image = discord.File(captcha.generate_captcha(), filename="captcha.png")
        captcha_embed = captcha.generate_embed(ctx.guild.name)
        delete_queue = [ctx.message]
        captcha_embed.description = "This captcha is **Case Sensitive**." \
                                    " You have **120 seconds** and **3 tries** to solve the captcha."
        captcha_embed.set_thumbnail(url=ctx.author.avatar_url)
        captcha_msg = await ctx.reply(content=ctx.author.mention, embed=captcha_embed, file=captcha_image)
        delete_queue.append(captcha_msg)

        def check(msg):
            return msg.channel.id == ctx.channel.id and msg.author == ctx.message.author

        verified = False
        i = 3
        while not verified and i >= 1:
            try:
                message = await self.bot.wait_for("message", timeout=120, check=check)
            except:
                msg = await ctx.channel.send(content=ctx.author.mention, embed=discord.Embed(
                    description="**Your 120 seconds are up.** Please request a new captcha.",
                    color=0xff0000).set_thumbnail(url=ctx.author.avatar_url))
                await self.delete_msgs(delete_queue)
                await asyncio.sleep(5)
                await msg.delete()
                return

            if captcha.verify_code(message.content):
                msg = await ctx.channel.send(content=ctx.author.mention, embed=discord.Embed(
                    description="You are now **verified**.").set_thumbnail(url=ctx.author.avatar_url))
                await self.delete_msgs(delete_queue)
                await asyncio.sleep(5)
                await msg.delete()
                await ctx.message.author.add_roles(ctx.guild.get_role(role))
                try:
                    await ctx.message.author.remove_roles(ctx.guild.get_role(946806692534968321))
                except:
                    return
            else:
                i -= 1
                if i == 0:
                    msg = await captcha_msg.reply(content=ctx.author.mention, embed=discord.Embed(
                        description="**3 incorrect tries.** You have run out of trials."
                                    " Please return to server and request a new captcha.",
                        color=0xff0000).set_thumbnail(url=ctx.author.avatar_url))
                    await self.delete_msgs(delete_queue)
                    await asyncio.sleep(5)
                    await msg.delete()
                    return
                else:
                    delete_queue.append(await captcha_msg.reply(content=ctx.author.mention, embed=discord.Embed(
                        description=f"Incorrect. Please try again. **Trials remaining: {i}/3**",
                        color=0xff0000).set_thumbnail(url=ctx.author.avatar_url)))

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, (commands.CommandNotFound, discord.HTTPException)):
            return

        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description="You don't have the permission to use this command."))
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=discord.Embed(
                title="Error",
                description=f"You forgot to provide an argument,"
                            f" please do it like: `{ctx.command.name} {ctx.command.usage}`"))


def setup(bot):
    bot.add_cog(Captcha(bot))
