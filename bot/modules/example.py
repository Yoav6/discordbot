from . import client

# simple event handler
@client.register_event()
async def on_ready():
    print(f'We have logged in as {client.user}')

# additional handler for on_ready
@client.register_event(event='on_ready')
async def another_on_ready():
    print(f'Second event for logging in as {client.user}')

# simple command
@client.register_command()
async def test1(message, text):
    await message.channel.send('it worked')

# command with custom name
@client.register_command(name='test2')
async def test_another(message, text):
    await message.channel.send('it also worked')

# command with rate limit of 3 calls in 10 seconds
@client.register_command(rate_limit=(3, 10))
async def test_rate(message, text):
    await message.channel.send('success')

# private only command
@client.register_command(allow_private=True, allow_public=False)
async def test_private(message, text):
    await message.channel.send('works')

# private and public command
@client.register_command(allow_private=True, allow_public=True)
async def test_private_and_public(message, text):
    await message.channel.send('works')
