import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import utils
import config

class PromoteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="promote", description="Promote a user in the Roblox group")
    async def promote(self, interaction: discord.Interaction, username: str):
        # 1. ПРОВЕРКА ПРАВ (Discord Roles)
        # Проверяем, есть ли у того, кто пишет команду, ID роли из списка разрешенных
        user_roles_ids = [role.id for role in interaction.user.roles]
        if not any(role_id in config.ALLOWED_ROLES for role_id in user_roles_ids):
            return await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)

        # Откладываем ответ, так как запросы к API занимают время
        await interaction.response.defer(ephemeral=True)

        # 2. ПОЛУЧАЕМ ДАННЫЕ ИЗ ROBLOX (через наш универсальный utils)
        user_id, current_role_id, _, error = await utils.get_roblox_member_data(username)
        
        if error:
            return await interaction.followup.send(f"❌ Error: {error}")

        # 3. ЛОГИКА ПОВЫШЕНИЯ ПО СПИСКУ
        # Берем список всех ID ролей из нашего словаря RANKS
        all_role_ids = list(config.RANKS.keys())
        
        try:
            current_index = all_role_ids.index(current_role_id)
        except ValueError:
            return await interaction.followup.send("❌ Current rank not found in the bot's database.")

        # Проверка на максимальный ранг
        if current_index >= len(all_role_ids) - 1:
            return await interaction.followup.send("❌ This user already has the maximum rank.")

        # Определяем ID новой роли и названия для эмбеда
        next_role_id = all_role_ids[current_index + 1]
        old_rank_name = config.RANKS[current_role_id]
        new_rank_name = config.RANKS[next_role_id]

        # 4. ЗАПРОС К ROBLOX API (Смена роли)
        url = f"https://groups.roblox.com/v1/groups/{config.RB_GROUP_ID}/users/{user_id}"
        headers = {"x-api-key": config.ROBLOX_API_KEY}
        payload = {"roleId": next_role_id}

        async with aiohttp.ClientSession() as session:
            async with session.patch(url, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    # Сообщение модератору в личку (так как ephemeral=True)
                    await interaction.followup.send(f"✅ **{username}** has been promoted to **{new_rank_name}**.")

                    # 5. ОТПРАВКА В ACTION_LOGS
                    log_channel = self.bot.get_channel(config.ACTION_LOGS)
                    if log_channel:
                        embed = discord.Embed(
                            title="📈 Rank Promotion",
                            color=0x00FF00 # Ярко-зеленый
                        )
                        embed.add_field(name="User", value=f"{username} | `{user_id}`", inline=False)
                        embed.add_field(name="Previous Rank", value=f"**{old_rank_name}**", inline=True)
                        embed.add_field(name="New Rank", value=f"**{new_rank_name}**", inline=True)
                        embed.set_footer(text=f"Promoted by: {interaction.user.display_name}")
                        
                        await log_channel.send(embed=embed)
                else:
                    error_text = await resp.text()
                    await interaction.followup.send(f"❌ Failed to promote. Roblox API error: {resp.status}")
                    print(f"Roblox API Error: {error_text}")

async def setup(bot):
    await bot.add_cog(PromoteCommand(bot))
