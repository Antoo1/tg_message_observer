from async_lru import alru_cache
from telethon.tl.types import Chat

from telegram_message_remover.services.models.users import Users
from telegram_message_remover.app.client import client


@alru_cache(ttl=100)
async def get_users() -> Users:
    return Users.parse_obj({'users': [{
        'tg_id': '369008786',
        'subscriptions': [{
            'group': get_chat_by_name('Антон'),
            'expr_rule': 'lalala',
            'forward_to': get_chat_by_id(872990685)
        }]
    }]})


@alru_cache(ttl=100)
async def get_chat_by_name(name: str) -> Chat:
    async for dialog in client.iter_dialogs():
        if dialog.name == name:
            return await dialog.message.get_chat()


@alru_cache(ttl=100)
async def get_chat_by_id(id_: int) -> Chat:
    async for dialog in client.iter_dialogs():
        if dialog.id == id_:
            return await dialog.message.get_chat()


# dict(id=369008786, is_self=False, contact=False, mutual_contact=False, deleted=False, bot=False,
#      bot_chat_history=False, bot_nochats=False, verified=False, restricted=False, min=False,
#      bot_inline_geo=False, support=False, scam=False, apply_min_photo=False, fake=False,
#      bot_attach_menu=False, premium=False, attach_menu_enabled=False,
#      access_hash=-834185691868042394, first_name='Антон', last_name=None, username='litvinan',
#      phone='79871507055') < telethon.tl.types.UserProfilePhoto object at 0x105b04990 >, 'status': <telethon.tl.types.UserStatusRecently object at 0x105b04910 >, 'bot_info_version': None, 'restriction_reason': None, 'bot_inline_placeholder': None, 'lang_code': None, 'emoji_status': None, 'usernames': None}

# {'id': 369008786, 'is_self': False, 'contact': False, 'mutual_contact': False, 'deleted': False, 'bot': False, 'bot_chat_history': False, 'bot_nochats': False, 'verified': False, 'restricted': False, 'min': False, 'bot_inline_geo': False, 'support': False, 'scam': False, 'apply_min_photo': False, 'fake': False, 'bot_attach_menu': False, 'premium': False, 'attach_menu_enabled': False, 'access_hash': -834185691868042394, 'first_name': 'Антон', 'last_name': None, 'username': 'litvinan', 'phone': '79871507055', 'photo': <telethon.tl.types.UserProfilePhoto object at 0x105b05b50>, 'status': <telethon.tl.types.UserStatusRecently object at 0x105b05810>, 'bot_info_version': None, 'restriction_reason': None, 'bot_inline_placeholder': None, 'lang_code': None, 'emoji_status': None, 'usernames': None}

# {'id': 872990685, 'title': 'test__', 'photo': <telethon.tl.types.ChatPhotoEmpty object at 0x10548e290>, 'participants_count': 2, 'date': datetime.datetime(2023, 1, 17, 18, 35, 49, tzinfo=datetime.timezone.utc), 'version': 1, 'creator': True, 'left': False, 'deactivated': False, 'call_active': False, 'call_not_empty': False, 'noforwards': False, 'migrated_to': None, 'admin_rights': None, 'default_banned_rights': <telethon.tl.types.ChatBannedRights object at 0x10548c990>}
# {'id': 369008786, 'is_self': False, 'contact': True, 'mutual_contact': True, 'deleted': False, 'bot': False, 'bot_chat_history': False, 'bot_nochats': False, 'verified': False, 'restricted': False, 'min': False, 'bot_inline_geo': False, 'support': False, 'scam': False, 'apply_min_photo': False, 'fake': False, 'bot_attach_menu': False, 'premium': False, 'attach_menu_enabled': False, 'access_hash': -834185691868042394, 'first_name': 'Антон', 'last_name': None, 'username': 'litvinan', 'phone': '79871507055', 'photo': <telethon.tl.types.UserProfilePhoto object at 0x105a85410>, 'status': <telethon.tl.types.UserStatusRecently object at 0x105a86990>, 'bot_info_version': None, 'restriction_reason': None, 'bot_inline_placeholder': None, 'lang_code': None, 'emoji_status': None, 'usernames': None}
