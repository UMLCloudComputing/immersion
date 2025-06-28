import discord
from discord.ext import commands
from discord import app_commands
import random
from dotenv import load_dotenv
import os
import aiohttp
import datetime
import typing
import time
import asyncio

class ImmersionBot(commands.Bot):
    client: aiohttp.ClientSession
    _uptime: datetime.datetime = datetime.datetime.now()
    _watcher = asyncio.Task

    def __init__(self, prefix: str, ext_dir: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(*args, **kwargs, command_prefix=commands.when_mentioned_or(prefix), intents=intents)
        self.ext_dir = ext_dir
        self.synced = False

    async def _load_extensions(self) -> None:
        if not os.path.isdir(self.ext_dir):
            print("Error!")
            return
        for filename in os.listdir(self.ext_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                try:
                    await self.load_extension(f"{self.ext_dir}.{filename[:-3]}")
                    print(f"Loaded extension {filename[:-3]}")
                except commands.ExtensionError as e:
                    print(f"Failed to load extension {filename[:-3]}::{e}")
    
    async def on_error(self, event_method: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        print(f"An error occured in {event_method}")

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} ({self.user.id})")

    async def setup_hook(self) -> None:
        self.client = aiohttp.ClientSession()
        await self._load_extensions()
        if not self.synced:
            await self.tree.sync()
            self.synced = not self.synced
            print("Synced command tree")
        self._watcher = self.loop.create_task(self._cog_watcher())
    
    async def close(self) -> None:
        await super().close()
        await self.client.close()
        
    def run(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        load_dotenv()
        try:
            super().run(str(os.getenv("DISCORD_TOKEN")), *args, **kwargs)
        except (discord.LoginFailure, KeyboardInterrupt):
            print("Exiting...")
            exit()

    async def _cog_watcher(self):
        print("Waiting for changes...")
        last = time.time()
        while True:
            extensions: set[str] = set()
            for name, module in self.extensions.items():
                if module.__file__ and os.stat(module.__file__).st_mtime > last:
                    extensions.add(name)
            for ext in extensions:
                try:
                    await self.reload_extension(ext)
                    print(f"Reloaded {ext}")
                except commands.ExtensionError as e:
                    print(f"Failed to reload {ext} :: {e}")
            last = time.time()
            await asyncio.sleep(1)

    @property
    def user(self) -> discord.ClientUser:
        assert super().user, "Bot is not ready yet"
        return typing.cast(discord.ClientUser, super().user)
    
    @property
    def uptime(self) -> datetime.timedelta:
        return datetime.datetime.now() - self.uptime
    
    
def main() -> None:
    bot = ImmersionBot(prefix="!", ext_dir="cogs")
    bot.run()

if __name__ == "__main__":
    main()
