import asyncio
import discord
import logging
from . import settings
from collections import defaultdict

log = logging.getLogger(__name__)

class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        self.custom_events = defaultdict(list)
        self.custom_commands = {}
        super().__init__(*args, **kwargs)

    def dispatch(self, event, *args, **kwargs):
        super().dispatch(event, *args, **kwargs)
        method = 'on_' + event
        log.debug('dispatch %s', method)
        for coro in self.custom_events[method]:
            self._schedule_event(coro, method, *args, **kwargs)

    def register_event(self, event=None):
        def decorator(coro):
            if not asyncio.iscoroutinefunction(coro):
                raise TypeError('custom event registered must be a coroutine function')
            self.custom_events[event or coro.__name__].append(coro)
            log.debug('%s has successfully been registered as a custom event', event or coro.__name__)
            return coro
        return decorator

    def register_command(self, name=None):
        def decorator(coro):
            if not asyncio.iscoroutinefunction(coro):
                raise TypeError('custom command registered must be a coroutine function')
            self.custom_commands[name or coro.__name__] = coro
            log.debug('%s has successfully been registered as a custom command', name or coro.__name__)
            return coro
        return decorator

    def run(self):
        return super().run(settings.TOKEN)

client = Client(**settings.CLIENT_PARAMS)

@client.register_event()
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(settings.COMMAND_PREFIX):
        parts = message.content.split(maxsplit=1)
        if len(parts) == 2:
            command, arg = parts
        else:
            command, arg = (parts[0], '')
        command = command[len(settings.COMMAND_PREFIX):]
        if command in client.custom_commands:
            try:
                await client.custom_commands[command](message, arg)
            except asyncio.CancelledError:
                pass
            except Exception:
                log.exception(f'Ignoring exception in custom command {f}')
