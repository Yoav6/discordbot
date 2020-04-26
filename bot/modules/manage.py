from . import client, settings
from discord.errors import Forbidden

@client.register_command(allow_private=True)
async def what_is_my_id(message, text):
    await message.channel.send(f'{message.author.id}')

@client.register_command(admin=True)
async def set_nickname(message, nickname):
    try:
        await message.guild.me.edit(nick=nickname)
        await message.channel.send('Nickname changed successfully')
    except Forbidden:
        await message.channel.send('Unable to change nickname, the server does not allow it')

@client.register_command(admin=True, allow_private=True)
async def set_server_nickname(message, text):
    try:
        guild_id, nickname = text.split(maxsplit=1)
    except ValueError:
        return await message.channel.send(f'Please specify a guild ID and nickname')
    try:
        guild = client.get_guild(int(guild_id))
        assert guild
    except (ValueError, AssertionError):
        await message.channel.send(f'Invalid guild ID')
    try:
        await guild.me.edit(nick=nickname)
        await message.channel.send('Nickname changed successfully')
    except Forbidden:
        await message.channel.send('Unable to change nickname, the server does not allow it')

@client.register_command(admin=True, allow_private=True)
async def list_servers(message, text):
    guilds = '\n'.join([f'{guild.id} - {guild.name}' for guild in client.guilds])
    await message.channel.send(f'```{guilds}```')

@client.register_command(admin=True, allow_private=True)
async def list_server_channels(message, guild_id):
    if not guild_id:
        await message.channel.send(f'Please specify the guild ID')
    try:
        guild = client.get_guild(int(guild_id))
        assert guild
    except (ValueError, AssertionError):
        await message.channel.send(f'Invalid guild ID')
    else:
        channels = sorted(guild.channels, key=lambda x: x.position)
        chunks = 30
        for i in range(0, len(channels), chunks):
            s = '\n'.join([f'{channel.id} - {channel.name}' for channel in channels[i:i + chunks]])
            await message.channel.send(f'```{s}```')

@client.register_command(admin=True, allow_private=True)
async def send_message(message, text):
    try:
        channel_id, text = text.split(maxsplit=1)
    except ValueError:
        return await message.channel.send(f'Please specify a channel ID and text to send')
    try:
        channel = client.get_channel(int(channel_id))
        assert channel
    except (ValueError, AssertionError):
        await message.channel.send(f'Invalid channel ID')
    else:
        await channel.send(text)
