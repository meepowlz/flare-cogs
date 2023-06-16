import discord
from redbot.core.errors import CogLoadError

from .threadbumper2 import ThreadBumper2


async def setup(bot):
    await bot.add_cog(ThreadBumper2(bot))
