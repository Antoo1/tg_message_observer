from typing import Callable

from telethon import events

from telegram_message_remover.app.client import client
from telegram_message_remover.services.models.users import Subscription
from telegram_message_remover.services.services.event_handler import EventHandler


def handler_factory(subscription: Subscription) -> Callable:
    # event_handler = EventHandler(subscription)

    async def handler(event: events.NewMessage):
        msg = event.message.to_dict()['message']
        # event_handler.check_if_message_suitable(msg)
        # chat = await event.get_chat()
        # sender = await event.get_sender()
        # chat_id = event.chat_id
        # sender_id = event.sender_id
        # await event.forward_to(subscription.forward_to, event.message)
        await event.message.forward_to(subscription.forward_to)
        print('here')

    return handler


def create_event(subscription: Subscription):
    handler = handler_factory(subscription)
    client.on(
        events.NewMessage(chats=subscription.group, pattern=subscription.expr_rule)
        # events.NewMessage(pattern=subscription.expr_rule)
    )(handler)


def add_event():
    pass


# @client.on(events.NewMessage)
# async def my_event_handler(event):
#     if 'hello' in event.raw_text:
#         await event.reply('hi!')
