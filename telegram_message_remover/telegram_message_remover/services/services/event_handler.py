""" обоабатывает каждое сообщение на регексп из тасок """
from telegram_message_remover.services.models.users import Subscription


class EventHandler:
    def __init__(self, subscription: Subscription):
        self._subscription = subscription

    def check_if_message_suitable(self, str):
        pass


