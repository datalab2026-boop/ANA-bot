import discord
import aiohttp
import config

async def get_player_role_id(bot, username: str):
    """
    Получает уникальный ID роли игрока в целевой группе.
    """
    user_id_url = "https://users.roblox.com/v1/usernames/users"
    groups_url = "https://groups.roblox.com/v1/users/{user_id}/groups/roles"

    async with aiohttp.ClientSession() as session:
        try:
            # --- 1. НИК -> USER ID ---
            payload = {"usernames": [username], "excludeBannedUsers": True}
            async with session.post(user_id_url, json=payload) as resp:
                data = await resp.json()
                
                if not data.get("data") or len(data["data"]) == 0:
                    return None, "Пользователь не найден в Roblox"
                
                user_id = data["data"][0]["id"]

            # --- 2. ПОЛУЧАЕМ РОЛИ ПОЛЬЗОВАТЕЛЯ ---
            async with session.get(groups_url.format(user_id=user_id)) as resp:
                if resp.status != 200:
                    return None, f"Ошибка API (Статус: {resp.status})"
                
                groups_data = await resp.json()

            # --- 3. ИЩЕМ НУЖНЫЙ ROLE ID ---
            for entry in groups_data.get("data", []):
                if entry["group"]["id"] == config.RB_GROUP_ID:
                    # Возвращаем уникальный ID роли (например: 92837465)
                    return entry["role"]["id"], None
            
            # Если игрока нет в группе
            return 0, "Игрок не состоит в группе"

        except Exception as e:
            # Логируем ошибку в консоль и возвращаем текст
            print(f"[Ошибка utils]: {e}")
            return None, "Системная ошибка запроса"
