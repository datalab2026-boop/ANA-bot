import discord
from discord.ext import commands, tasks
import aiohttp
import asyncio
import os

# Твои файлы
import config
import utils

class MyBot(commands.Bot):
    def __init__(self):
        # Настраиваем интенты
        intents = discord.Intents.default()
        # Для работы со слеш-командами префикс не важен, ставим None
        super().__init__(command_prefix=None, intents=intents)

    async def setup_hook(self):
        """Выполняется ПЕРЕД тем, как бот выйдет в онлайн"""
        
        # В будущем здесь будет код для загрузки твоих Cogs из папки commands
        # await self.load_extension('commands.название_файла')
        
        # Синхронизируем команды (чтобы они появились в Discord)
        await self.tree.sync()
        
        # Запускаем фоновую задачу проверки состояния
        self.status_check.start()

    @tasks.loop(minutes=1.0)
    async def status_check(self):
        # Пустая задача раз в минуту, как ты просил
        pass

    @status_check.before_loop
    async def before_status_check(self):
        await self.wait_until_ready()

# Создаем объект бота
bot = MyBot()

@bot.event
async def on_ready():
    """Событие: Бот успешно подключился к Discord Gateway"""
    
    # 1. Загрузка данных из Roblox через твой config.py
    try:
        await config.load_roblox_ranks()
        roblox_status = "with all Roblox ranks"
    except Exception as e:
        roblox_status = "but Roblox ranks FAILED"
        print(f"Ошибка загрузки рангов: {e}")

    # 2. Отправка зеленого эмбеда в ACTIONS_LOG
    channel = bot.get_channel(config.ACTIONS_LOG)
    
    if channel:
        embed = discord.Embed(
            description=f"✅ Bot successfully loaded to discord gateway {roblox_status}",
            color=0x00FF00
        )
        await channel.send(embed=embed)
    
    print(f"--- [ONLINE] {bot.user} запущен ---")

# Запуск программы
if __name__ == "__main__":
    if config.DISCORD_TOKEN:
        bot.run(config.DISCORD_TOKEN)
    else:
        print("КРИТИЧЕСКАЯ ОШИБКА: DISCORD_TOKEN не найден в config.py!")
