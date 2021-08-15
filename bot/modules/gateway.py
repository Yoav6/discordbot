from . import client

@client.register_command()
async def gateway(message, text):
    if message.channel_mentions:
        gateway_to = message.channel_mentions[0]
        if message.author.permissions_in(gateway_to).send_messages:
            from_message = await message.channel.send(f'Creating a gateway to {gateway_to.mention}...')
            to_message = await gateway_to.send(f'{message.author.mention} created gateway from {message.channel.mention}\n{from_message.jump_url}')
            await from_message.edit(content=f'{message.author.mention} created gateway to {gateway_to.mention}\n{to_message.jump_url}')
