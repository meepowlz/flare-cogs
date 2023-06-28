import logging

import discord
from discord.ext import tasks
from redbot.core import Config, commands

log = logging.getLogger("red.flare.threadbumper")


CAKEY_THREAD_ID = 1057089253135351940


class ThreadBumper(commands.Cog):
    __version__ = "1.0.0"
    __author__ = "meepowlz"

    def format_help_for_context(self, ctx):
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\nCog Version: {self.__version__}\nAuthor: {self.__author__}"

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not store any data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not store any data
        pass

    @tasks.loop(hours=168)
    async def bump_threads(self):
        config = await self.config.all_guilds()
        for guild_id, guild_data in config.items():
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                continue

            for thread_id in guild_data["threads"]:
                thread = guild.get_thread(thread_id)
                if thread is None:
                    continue
                else:
                    if thread_id == CAKEY_THREAD_ID:
                        await thread.send(":boxing_glove:")
                    else:
                        await thread.send(":punch:")
                    await thread.edit(archived=False, auto_archive_duration=10080)
                    log.debug(f"Thread {thread.id} was bumped")


    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1398467138476, force_registration=True)
        self.config.register_guild(threads=[])
        self.bump_threads.start()

    def cog_unload(self):
        self.bump_threads.cancel()

    @commands.command()
    async def bumpall(self, ctx):
        """
        Bumps all threads currently being kept-alive
        """
        await self.bump_threads()

    @commands.command()
    async def checkalive(self, ctx):
        """
        Lists threads currently being kept-alive.
        """

        await ctx.send(self.config.guild(ctx.guild).threads())


    @commands.command()
    @commands.bot_has_permissions(manage_threads=True)
    async def keepalive(self, ctx, thread: discord.Thread):
        """
        Sends a ping to the thread to keep it alive.
        """
        async with self.config.guild(ctx.guild).threads() as threads:
            if thread.id in threads:
                threads.remove(thread.id)
                await ctx.send(
                    f"{thread.mention} under {thread.parent.mention} is no longer being bumped."
                )
            else:
                threads.append(thread.id)
                await ctx.send(
                    f"{thread.mention} under {thread.parent.mention} is now being bumped."
                )


