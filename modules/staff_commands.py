from discord.ext import commands
from datetime import datetime, date, timedelta
import discord
import asyncio
import robloxapi
import os
from dotenv import load_dotenv

load_dotenv()
COOKIE = os.getenv('ROBLOX_COOKIE')
roblox_client = robloxapi.Client(COOKIE)


class staff_commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="cooldown", aliases=['cd'])
    async def cooldown(self, context, member: discord.Member = 0):
        member_roles = context.author.roles
        pep_server = self.client.get_guild(481530361650741249)  # should = pep guild id
        role_object = pep_server.get_role(661426538943610880)  # should = evaluator id
        if role_object not in member_roles:
            await context.send(f'This command requires the ``Evaluator`` role to be used.')
            return
        if member == 0:
            await context.send(f'{context.author.mention} Command syntax: `$cooldown <@member>`')
            return
        current_time = str(datetime.now().time())
        author_name = context.author.display_name
        member_name = member.display_name
        current_hour = int(current_time[:2])
        current_minute = current_time[3:5]
        am = True
        channel = self.client.get_channel(722141971736559695)  # should = pep-bot-logs id
        if current_hour > 12:
            current_hour -= 12
            am = False
        current_hour += 1
        if not am:
            tod = 'PM'
        else:
            tod = 'AM'
        pep_discord = self.client.get_guild(717503158284189757)  # should = pep server id
        cooldown_role = pep_discord.get_role(732051972009754702)  # should = cooldown id
        await member.add_roles(cooldown_role)
        await context.send(
            f'Success! {member.mention} will be on cooldown until ``{current_hour}:{current_minute}{tod}`` '
            f'EST.')
        await member.send(
            f'Congratulations on passing your evaluation. You are now on cooldown, meaning you can attend '
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


def setup(client):
    client.add_cog(staff_commands(client))
