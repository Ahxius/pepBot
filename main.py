import os
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot
import asyncio
from datetime import datetime
from discord.ext import commands
import robloxapi
import sys

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COOKIE = os.getenv('ROBLOX_COOKIE')

client = Bot(command_prefix='$')

for cog in os.listdir('modules'):
    if not cog.endswith('.py'):
        continue
    try:
        client.load_extension(f'modules.{cog[:-3]}')
    except SyntaxError as es:
        print(f'Failed to load module {cog} due to a syntax error.')
    except ImportError as ei:
        print(f'Failed to load module {cog} due to an import error.')


@client.event
async def on_ready():
    print(f'Login successful; {client.user}')


@client.command(name='shutdown')
@commands.is_owner()
async def shutdown(context):
    await context.message.add_reaction(client.check)
    sys.exit()


client.run(TOKEN)
