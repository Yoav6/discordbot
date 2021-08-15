from . import client, settings
from .utils import parse_duration
from asyncio import sleep
from datetime import datetime, timedelta
from discord.utils import get

rate_limits = {}

@client.register_command()
async def rate_limit(message, text):
    if not set(settings.RATE_LIMIT_ROLES) & set(x.name for x in message.author.roles):
        return await message.channel.send(f'Insufficient privileges')
    if not message.mentions:
        return await message.channel.send(f'Missing user parameter')
    if len(text.split()) == 2 and text.split()[1] == 'off':
        if (message.guild.id, message.mentions[0].id) in rate_limits:
            del rate_limits[(message.guild.id, message.mentions[0].id)]
            role = get(message.guild.roles, name=settings.RATE_LIMIT_MUTED_ROLE)
            await message.mentions[0].remove_roles(role, reason='rate limit')
            return await message.channel.send(f'Rate limiting stopped')
    if not len(text.split()) == 3:
        return await message.channel.send(f'Parameters: <user> <interval> <duration>')
    _, interval, duration = text.split()
    try:
        interval, duration = parse_duration(interval), parse_duration(duration)
    except ValueError:
        return await message.channel.send(f'Invalid parameters')
    rate_limits[(message.guild.id, message.mentions[0].id)] = {'interval': interval, 'expires': datetime.utcnow() + timedelta(seconds=duration)}
    await message.channel.send(f'Rate limiting {message.mentions[0].mention}')

@client.register_event(event='on_message')
async def on_message(message):
    if message.author and message.guild and (message.guild.id, message.author.id) in rate_limits:
        rate_limit = rate_limits[(message.guild.id, message.author.id)]
        if datetime.utcnow() >= rate_limit['expires']:
            del rate_limits[(message.guild.id, message.author.id)]
        else:
            role = get(message.guild.roles, name=settings.RATE_LIMIT_MUTED_ROLE)
            await message.author.add_roles(role, reason='rate limit')
            await sleep(rate_limit['interval'])
            await message.author.remove_roles(role, reason='rate limit')
