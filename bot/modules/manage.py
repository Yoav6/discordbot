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
async def list_servers(message, text):
    guilds = await client.fetch_guilds(limit=150).flatten()
    guilds = '\n'.join([guild.name for guild in guilds])
    await message.channel.send(f'```{guilds}```')
