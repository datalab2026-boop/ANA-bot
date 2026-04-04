import discord
from discord.ext import commands
import config
import datetime
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.loaded_files = []
        self.startup_errors = []

    async def setup_hook(self):
        # Библиотека сама создаст сессию, мы просто подгружаем файлы
        if not os.path.exists('./commands'):
            os.makedirs('./commands')
        
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                module_name = filename[:-3]
                try:
                    await self.load_extension(f'commands.{module_name}')
                    self.loaded_files.append(module_name)
                except Exception as e:
                    self.startup_errors.append(f"{module_name}: {e}")

    async def on_ready(self):
        log_channel = self.get_channel(config.LOGS_CHANNEL)
        error_channel = self.get_channel(config.ERROR_CHANNEL)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        tasks = []
        if log_channel:
            embed_log = discord.Embed(
                title="System Online",
                description=f"Core linked. Modules: **{', '.join(self.loaded_files) or 'None'}**",
                color=discord.Color.green()
            )
            tasks.append(log_channel.send(embed=embed_log))

        if error_channel and self.startup_errors:
            embed_err = discord.Embed(
                title="Startup Issues",
                description="\n".join(self.startup_errors),
                color=discord.Color.orange()
            )
            tasks.append(error_channel.send(embed=embed_err))

        if tasks:
            await asyncio.gather(*tasks)
        
        print(f"[{timestamp}] Connected as {self.user}")

bot = MyBot()

def start():
    # bot.run сам обрабатывает переподключения при сбоях сети
    bot.run(config.BOT_TOKEN)

if __name__ == "__main__":
    start()
  
