import os
# important keys
BOT_TOKEN = os.environ.get("BotToken")
CLOUD_API = os.environ.get("CloudAPI")
RESTART_TOKEN = os.environ.get("RestartToken")
ROVER_API = os.environ.get("RoverAPI")
MONGO_URL = os.environ.get("MONGO_URL")
SHEET_KEY = os.environ.get("SheetKey")
# Maintenance
GROUP_ID = 0
# Logging Channels
ALT_DETECTION = 0
ERROR_LOGS = 0
PROMOTION_LOGS = 0
# Permissions set up
PERMITTED_ROLES = [] # Write ", " between each discord role ID
# Roblox Group Related Roles
ROLES_LIST = []
VALID_ROLES = []
