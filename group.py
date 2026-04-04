import os
import requests
import config

GROUP_ID = config.GROUP_ID

def get_group_roles():
    url = f"https://groups.roblox.com/v1/groups/{GROUP_ID}/roles"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            roles = data.get('roles', [])
            
            sorted_roles = sorted(roles, key=lambda x: x['rank'])
            
            print(f"--- Roles for Group {GROUP_ID} ---")
            for role in sorted_roles:
                print(f"Rank: {role['rank']: <3} | ID: {role['id']: <12} | Name: {role['name']}")
        else:
            print(f"API Error: {response.status_code}")
                
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    get_group_roles()
  
