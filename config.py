import os

DISCORD_TOKEN = os.environ.get("Bottoken")
ROBLOX_API_KEY = os.environ.get("Apitoken")
RESTART_TOKEN = os.environ.get("Restarttoken")

GROUP_ID = 841435331
ALLOWED_ROLES = [] 
ACTIONS_LOG = 0
BUG_LOGS = 0

RANKS = {}       
VALID_RANKS = [] 
MAX_RANK_THRESHOLD = 200 # Установите число (0-255), ниже которого ранги считаются VALID
