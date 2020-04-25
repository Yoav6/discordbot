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
