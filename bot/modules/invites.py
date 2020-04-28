import logging
from . import client, settings
from time import time
from datetime import datetime, timedelta
from .utils.db import JSONDatabase
from contextlib import contextmanager
from discord.errors import Forbidden

log = logging.getLogger(__name__)

class RequestOngoing(Exception):
    pass

class InvitesDB(JSONDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {int(k): v for k, v in self.data.items()}
        self.ongoing_requests = []

    def get_history(self, user_id, since_ts):
        return sorted([x for x in self.data.get(user_id, []) if x > since_ts])

    @contextmanager
    def initiate_request(self, user_id):
        if user_id in self.ongoing_requests:
            raise RequestOngoing
        try:
            self.ongoing_requests.append(user_id)
            yield
        finally:
            self.ongoing_requests.remove(user_id)

    def add_request(self, user_id):
        self.data[user_id] = self.get_history(user_id, time() - settings.INVITE_QUOTA_HISTORY) + [time()]
        self.save()

invites_db = InvitesDB(settings.INVITE_DB_PATH)

@client.register_command()
async def request_invite(message, text):
    delta = datetime.utcnow() - message.author.joined_at
    if delta.total_seconds() < settings.INVITE_JOIN_TIME_REQUIREMENT:
        return await message.channel.send(f'{message.author.mention} only users who have been in this server for {settings.INVITE_JOIN_TIME_REQUIREMENT_READABLE} can request invites, please try again in {delta}.')
    quota_num, quota_seconds = settings.INVITE_QUOTA
    try:
        with invites_db.initiate_request(message.author.id):
            history = invites_db.get_history(message.author.id, time() - quota_seconds)
            if len(history) >= quota_num:
                delta = timedelta(seconds=quota_seconds - int(time() - history[-quota_num:][0]))
                return await message.channel.send(f'{message.author.mention} you have reached your quota, please try again in {delta}')
            try:
                invite = await message.channel.create_invite(max_age=settings.INVITE_MAX_AGE, max_uses=settings.INVITE_MAX_USES, unique=True)
            except Forbidden:
                return await message.channel.send('Unable to create invite, permission denied')
            log.info('invite created for user %s (%s): %s', message.author.name, message.author.id, invite.id)
            await message.author.send(f'Invite link: {invite.url}')
            invites_db.add_request(message.author.id)
            await message.channel.send(f'{message.author.mention} an invite link has been sent to you')
    except RequestOngoing:
        log.error('request_invite prevented, a request was already submitted by the user')
