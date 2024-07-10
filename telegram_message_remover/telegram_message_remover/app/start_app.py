import asyncio
from contextlib import suppress
from typing import List

from telegram_message_remover.app.client import client

# from telegram_message_remover.services.models.users import ParsedSubscription, Subscription
from telegram_message_remover.services.services.main_cycle import main
# from telethon.tl.functions.messages import DeleteMessages


async def main_loop():
    async with client:
        await client.start()
        await client.send_message('me', 'Hello, myself!')
        await main()
        await client.run_until_disconnected()


async def not_main():
    async with client:
        await client.start()
        async for dialog in client.iter_dialogs():
            print(dialog.__dict__)
            chat = await dialog.message.get_chat()
            if dialog.name == 'Антон':
                messages_to_delete = []
                async for message in client.iter_messages(chat, from_user='me'):
                    messages_to_delete.append(message)

                await client.delete_messages(None, [x.id for x in messages_to_delete])
                await client.send_message(chat, 'Hello, myself!')
            if dialog.name == 'test_group':
                messages_to_delete = []
                async for message in client.iter_messages(chat, from_user='me'):
                    messages_to_delete.append(message)

                await client.delete_messages('me', [x.id for x in messages_to_delete])
                await client.send_message(chat, 'Hello, myself!')


# async def parse_subscriptions(client: client, subscriptions: List[Subscription]) -> List[ParsedSubscription]:
#     dialogs = {}
#     parsed_subscription = []
#     async for dialog in client.iter_dialogs():
#         dialogs[dialog.name] = await dialog.message.get_chat()
#
#     for subscription in subscriptions:
#         with suppress(KeyError):
#             parsed_subscription.append(
#                 ParsedSubscription(
#                     group=dialogs[subscription.group],
#                     expr_rule=subscription.expr_rule,
#                     forward_to=dialogs[subscription.forward_to],
#                 )
#         )
#     return parsed_subscription


if __name__ == '__main__':
    from telegram_message_remover.app.logging_configuration import init_logging
    init_logging()
    # asyncio.run(main_loop())
    asyncio.run(not_main())
