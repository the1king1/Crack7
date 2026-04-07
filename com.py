import os
import sys
import time
import asyncio
import webbrowser
import requests
import discord
from discord.ext import commands
from colorama import Fore, init, Style

# Initialize colorama
init(autoreset=True)

# Clear screen function
cls = lambda: os.system('cls' if os.name == 'nt' else 'clear')

# Set console title (Windows only)
if os.name == 'nt':
    mytitle = 'Casa Cloner - Developed by Noritem#6666 | Cracked by Nord'
    os.system('title ' + mytitle)

class Clone:
    """Clone class to handle server cloning operations"""
    
    @staticmethod
    async def guild_edit(guild_to, guild_from):
        """Edit guild settings"""
        try:
            await guild_to.edit(
                name=guild_from.name,
                icon=await guild_from.icon.read() if guild_from.icon else None
            )
            print(f'{Fore.GREEN}[+] Guild settings copied{Style.RESET_ALL}')
        except Exception as e:
            print(f'{Fore.RED}[-] Failed to edit guild: {e}{Style.RESET_ALL}')
    
    @staticmethod
    async def roles_delete(guild_to):
        """Delete all roles in target guild"""
        try:
            for role in guild_to.roles:
                if role.name != "@everyone":
                    await role.delete()
            print(f'{Fore.GREEN}[+] Roles deleted{Style.RESET_ALL}')
        except Exception as e:
            print(f'{Fore.RED}[-] Failed to delete roles: {e}{Style.RESET_ALL}')
    
    @staticmethod
    async def channels_delete(guild_to):
        """Delete all channels in target guild"""
        try:
            for channel in guild_to.channels:
                await channel.delete()
            print(f'{Fore.GREEN}[+] Channels deleted{Style.RESET_ALL}')
        except Exception as e:
            print(f'{Fore.RED}[-] Failed to delete channels: {e}{Style.RESET_ALL}')
    
    @staticmethod
    async def roles_create(guild_to, guild_from):
        """Create roles from source guild"""
        try:
            role_map = {}
            for role in reversed(guild_from.roles):
                if role.name != "@everyone":
                    new_role = await guild_to.create_role(
                        name=role.name,
                        permissions=role.permissions,
                        colour=role.colour,
                        hoist=role.hoist,
                        mentionable=role.mentionable
                    )
                    role_map[role.id] = new_role.id
            print(f'{Fore.GREEN}[+] Roles created{Style.RESET_ALL}')
            return role_map
        except Exception as e:
            print(f'{Fore.RED}[-] Failed to create roles: {e}{Style.RESET_ALL}')
            return {}
    
    @staticmethod
    async def categories_create(guild_to, guild_from):
        """Create categories from source guild"""
        try:
            category_map = {}
            for category in guild_from.categories:
                new_category = await guild_to.create_category(category.name)
                category_map[category.id] = new_category.id
            print(f'{Fore.GREEN}[+] Categories created{Style.RESET_ALL}')
            return category_map
        except Exception as e:
            print(f'{Fore.RED}[-] Failed to create categories: {e}{Style.RESET_ALL}')
            return {}
    
    @staticmethod
    async def channels_create(guild_to, guild_from):
        """Create channels from source guild"""
        try:
            for channel in guild_from.channels:
                if channel.type == discord.ChannelType.text:
                    await guild_to.create_text_channel(channel.name)
                elif channel.type == discord.ChannelType.voice:
                    await guild_to.create_voice_channel(channel.name)
                elif channel.type == discord.ChannelType.category:
                    continue  # Categories are handled separately
            print(f'{Fore.GREEN}[+] Channels created{Style.RESET_ALL}')
        except Exception as e:
            print(f'{Fore.RED}[-] Failed to create channels: {e}{Style.RESET_ALL}')

def print_logo():
    """Print the Casa Cloner logo"""
    print(f'{Fore.RED}\n            ██████╗ █████╗ ███████╗ █████╗      ██████╗██╗      ██████╗ ███╗   ██╗███████╗██████╗ {Style.RESET_ALL}')
    print(f'{Fore.RED}            ██╔════╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝██║     ██╔═══██╗████╗  ██║██╔════╝██╔══██╗{Style.RESET_ALL}')
    print(f'{Fore.RED}            ██║     ███████║███████╗███████║    ██║     ██║     ██║   ██║██╔██╗ ██║█████╗  ██████╔╝{Style.RESET_ALL}')
    print(f'{Fore.RED}            ██║     ██╔══██║╚════██║██╔══██║    ██║     ██║     ██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗{Style.RESET_ALL}')
    print(f'{Fore.RED}            ╚██████╗██║  ██║███████║██║  ██║    ╚██████╗███████╗╚██████╔╝██║ ╚████║███████╗██║  ██║{Style.RESET_ALL}')
    print(f'{Fore.RED}             ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝{Style.RESET_ALL}')
    print(f'{Fore.YELLOW}                                   ╔════════════════════════════════════════════════╗{Style.RESET_ALL}')
    print(f'{Fore.YELLOW}                                   ║     Cracked by Group.dll                            ║{Style.RESET_ALL}')
    print(f'{Fore.YELLOW}                                   ╚════════════════════════════════════════════════╝{Style.RESET_ALL}')
    print(f'                                        {Fore.MAGENTA}Developed by: Noritem#6666{Style.RESET_ALL}\n')

class DiscordCloner:
    def __init__(self):
        self.client = discord.Client(intents=discord.Intents.default())
        
    async def clone_server(self, token, source_guild_id, target_guild_id):
        """Main cloning function"""
        @self.client.event
        async def on_ready():
            cls()
            print(f'{Fore.GREEN}[+] Logged in as: {self.client.user}{Style.RESET_ALL}')
            print(f'{Fore.YELLOW}[*] Starting server cloning...{Style.RESET_ALL}')
            
            try:
                guild_from = self.client.get_guild(int(source_guild_id))
                guild_to = self.client.get_guild(int(target_guild_id))
                
                if not guild_from or not guild_to:
                    print(f'{Fore.RED}[-] Invalid guild ID(s){Style.RESET_ALL}')
                    await self.client.close()
                    return
                
                await Clone.guild_edit(guild_to, guild_from)
                await Clone.roles_delete(guild_to)
                await Clone.channels_delete(guild_to)
                await Clone.roles_create(guild_to, guild_from)
                await Clone.categories_create(guild_to, guild_from)
                await Clone.channels_create(guild_to, guild_from)
                
                print(f'{Fore.GREEN}[+] Server cloning completed!{Style.RESET_ALL}')
                
            except Exception as e:
                print(f'{Fore.RED}[-] Error during cloning: {e}{Style.RESET_ALL}')
            
            await asyncio.sleep(3)
            await self.client.close()
            main_answer()
        
        try:
            await self.client.start(token)
        except Exception as e:
            print(f'{Fore.RED}[-] Failed to connect: {e}{Style.RESET_ALL}')
            input(f'{Fore.YELLOW}[*] Press Enter to continue...{Style.RESET_ALL}')
            main_answer()

def validate_token(token):
    """Validate Discord token"""
    headers = {'Authorization': token}
    try:
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        return response.status_code == 200
    except:
        return False

def unfriender():
    """Clone server function"""
    cls()
    print_logo()
    
    token = input(f'{Fore.MAGENTA}[?] Your Discord Token > {Style.RESET_ALL}').strip()
    
    if not validate_token(token):
        print(f'{Fore.RED}[-] Invalid token!{Style.RESET_ALL}')
        input(f'{Fore.YELLOW}[*] Press Enter to continue...{Style.RESET_ALL}')
        main_answer()
        return
    
    print(f'{Fore.GREEN}[+] Token is valid!{Style.RESET_ALL}')
    
    source_guild = input(f'{Fore.MAGENTA}[?] Source Server ID (to copy from) > {Style.RESET_ALL}').strip()
    target_guild = input(f'{Fore.MAGENTA}[?] Target Server ID (to copy to) > {Style.RESET_ALL}').strip()
    
    if not source_guild.isdigit() or not target_guild.isdigit():
        print(f'{Fore.RED}[-] Invalid server ID format!{Style.RESET_ALL}')
        input(f'{Fore.YELLOW}[*] Press Enter to continue...{Style.RESET_ALL}')
        main_answer()
        return
    
    cls()
    cloner = DiscordCloner()
    asyncio.run(cloner.clone_server(token, source_guild, target_guild))

def casa():
    """Join Casa Discord server"""
    webbrowser.open_new('https://discord.gg/dyJuNuMzjF')
    print(f'{Fore.GREEN}[+] Opening Discord invite...{Style.RESET_ALL}')
    time.sleep(2)
    main_answer()

def no():
    """Open Noritem website"""
    webbrowser.open_new('https://noritem.de')
    print(f'{Fore.GREEN}[+] Opening website...{Style.RESET_ALL}')
    time.sleep(2)
    main_answer()

def main_answer():
    """Main menu function"""
    cls()
    print_logo()
    print(f'{Fore.CYAN}[1] > Clone Server{Style.RESET_ALL}')
    print(f'{Fore.CYAN}[2] > Join Casa{Style.RESET_ALL}')
    print(f'{Fore.CYAN}[3] > Noritem.de{Style.RESET_ALL}')
    print(f'{Fore.CYAN}[4] > Exit{Style.RESET_ALL}')
    print()
    
    answer = input(f'{Fore.RED}[>]{Style.RESET_ALL} Choose an option: ').strip()
    
    if answer == '1':
        unfriender()
    elif answer == '2':
        casa()
    elif answer == '3':
        no()
    elif answer == '4':
        print(f'{Fore.YELLOW}[*] Goodbye!{Style.RESET_ALL}')
        sys.exit(0)
    else:
        print(f'{Fore.RED}[-] Invalid option! Please choose 1-4{Style.RESET_ALL}')
        time.sleep(1.5)
        main_answer()

if __name__ == "__main__":
    try:
        main_answer()
    except KeyboardInterrupt:
        print(f'\n{Fore.YELLOW}[*] Exiting...{Style.RESET_ALL}')
        sys.exit(0)
    except Exception as e:
        print(f'{Fore.RED}[-] Fatal error: {e}{Style.RESET_ALL}')
        input(f'{Fore.YELLOW}[*] Press Enter to exit...{Style.RESET_ALL}')
        sys.exit(1)
