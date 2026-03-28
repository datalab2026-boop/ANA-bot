import os
import aiohttp
import asyncio

# --- Настройки из окружения ---
DISCORD_TOKEN = os.environ.get("Bottoken")
ROBLOX_API_KEY = os.environ.get("Apitoken")
RESTART_TOKEN = os.environ.get("Restarttoken")

# --- Константы группы ---
RB_GROUP_ID = 841435331
ALLOWED_ROLES = 1479884336051388604
ACTIONS_LOG = 1481718190961590392
BUG_LOGS = 1487248340252098770

# --- Динамические данные (заполняются через setup) ---
RANKS = {}        
VALID_RANKS = []  
MAX_RANK_THRESHOLD = 200
MIN_RANK_THRESHOLD = 1

async def load_roblox_ranks():
    """
    Парсит роли напрямую из API Roblox и сохраняет в переменные конфига.
    """
    url = f"https://groups.roblox.com/v1/groups/{RB_GROUP_ID}/roles"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    roles = data.get("roles", [])
                    
                    # Очищаем на случай повторного вызова
                    RANKS.clear()
                    VALID_RANKS.clear()
                    
                    for role in roles:
                        rank_val = role["rank"]
                        role_name = role["name"]
                        role_id = role["id"]
                        
                        RANKS[rank_val] = role_name
                        VALID_RANKS.append(rank_val)
                    
                    VALID_RANKS.sort()
                    print(f"[Config] successfully loaded {len(RANKS)} ranks.")
                else:
                    print(f"[Config Error] API Status return: {response.status}")
        except Exception as e:
            print(f"[Config Critical] requset failure {e}")
