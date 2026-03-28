import os
import aiohttp
import asyncio

# --- Настройки из окружения ---
DISCORD_TOKEN = os.environ.get("Bottoken")
ROBLOX_API_KEY = os.environ.get("Apitoken")
RESTART_TOKEN = os.environ.get("Restarttoken")

# --- Константы группы ---
RB_GROUP_ID = 841435331
ALLOWED_ROLES = [1479884336051388604] 
ACTIONS_LOG = 1481718190961590392
BUG_LOGS = 1487248340252098770

# --- Динамические данные ---
RANKS = {}        
VALID_RANKS = []  
MAX_RANK_THRESHOLD = 200
MIN_RANK_THRESHOLD = 1

async def load_roblox_ranks():
    """
    Парсит роли напрямую из API Roblox.
    Возвращает строку с отчетом для логов.
    """
    url = f"https://groups.roblox.com/v1/groups/{RB_GROUP_ID}/roles"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    roles = data.get("roles", [])
                    
                    RANKS.clear()
                    VALID_RANKS.clear()
                    
                    report_lines = []
                    for role in roles:
                        rank_val = role["rank"]
                        role_info = {
                            "name": role["name"],
                            "id": role["id"]
                        }
                        
                        RANKS[rank_val] = role_info
                        
                        # Проверка на вхождение в диапазон
                        is_valid = MIN_RANK_THRESHOLD <= rank_val <= MAX_RANK_THRESHOLD
                        status_icon = "✅" if is_valid else "⚪"
                        
                        if is_valid:
                            VALID_RANKS.append(rank_val)
                        
                        report_lines.append(f"{status_icon} **{rank_val}**: {role['name']} (`{role['id']}`)")
                    
                    VALID_RANKS.sort()
                    return "\n".join(report_lines)
                else:
                    return f"❌ API Error: Status {response.status}"
        except Exception as e:
            return f"❌ Critical Error: {e}"
