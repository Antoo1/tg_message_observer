from telegram_message_remover.services.db_queries.user import get_users
from telegram_message_remover.services.services.event_registrator import create_event


async def main():
    users = await get_users()
    for user in users.users:
        for subscription in user.subscriptions:
            create_event(subscription)
