import os
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot
import asyncio
from datetime import datetime
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = Bot(command_prefix='$')


@client.event
async def on_ready():
    print(f'Login successful; {client.user}')
    client.pep_discord = client.get_guild(481530361650741249)  # should = pep server id


@client.command(name="cooldown", aliases=['cd'])
async def cooldown(context, member: discord.Member = 0):
    if member == 0:
        await context.send(f'{context.author.mention} Command syntax: `$cooldown <@member>`')
    current_time = str(datetime.now().time())
    author_name = context.author.display_name
    member_name = member.display_name
    current_hour = int(current_time[:2])
    current_minute = current_time[3:5]
    am = True
    channel = client.get_channel(753386440133574827)  # should = pep-bot-logs id
    if current_hour > 12:
        current_hour -= 12
        am = False
    current_hour += 1
    if not am:
        tod = 'PM'
    else:
        tod = 'AM'
    cooldown_role = client.pep_discord.get_role(714194832251158720)  # should = cooldown id
    await member.add_roles(cooldown_role)
    await context.send(f'Success! {member.mention} will be on cooldown until ``{current_hour}:{current_minute}{tod}`` '
                       f'EST.')
    await member.send(f'Congratulations on passing your evaluation. You are now on cooldown, meaning you can attend '
                      f'your next evaluation at ``{current_hour}:{current_minute}{tod} EST`` tomorrow.')
    embed = discord.Embed(title='Cooldown Begun', color=0x33ff5a)
    embed.add_field(name="Evaluator", value=f'{author_name}', inline=True)
    embed.add_field(name='Attendee', value=f'{member_name}', inline=True)
    embed.add_field(name='Scheduled to End', value=f'{current_hour}:{current_minute}{tod} EST')
    message = await channel.send(embed=embed)
    await asyncio.sleep(86400)
    await member.remove_roles(cooldown_role)
    await member.send(f'Your cooldown in PEP has concluded. Good luck, we hope to see you in PHANTOM soon.')
    await message.add_reaction(emoji='\U0000274c')
    embed = discord.Embed(title='Cooldown Concluded', color=0xFF3333)
    embed.add_field(name='Evaluator', value=f'{author_name}', inline=True)
    embed.add_field(name='Attendee', value=f'{member_name}', inline=True)
    await channel.send(embed=embed)

client.run(TOKEN)
