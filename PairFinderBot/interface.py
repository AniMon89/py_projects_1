import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.exceptions import ApiError
from core import VkTools
from data_store import BotDB

from config import community_token, access_token


class BotInterface:

    def __init__(self, token):
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VkTools(access_token)
        self.params = None
        self.offset = 0

    def message_send(self, user_id, message, attachment=None):
        try:
            self.vk.method('messages.send',
                {'user_id': user_id,
                'message': message,
                'attachment': attachment,
                'random_id': get_random_id()
                 }
                )
        except ApiError as e:
            print(f'error = {e}')
            return None

    def get_message(self):
        try:
            longpoll = VkLongPoll(self.vk)

            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    text = event.text.lower()
                    return text
        except ApiError as e:
            print(f'error = {e}')
            return None

    def event_handler(self):

        for event in self.longpoll.listen():

            if self.get_message().lower() == 'привет':
                self.params = self.vk_tools.get_profile_info(event.user_id)
                if self.params["name"] is not None:
                    self.message_send(event.user_id, f'Привет, {self.params["name"]}.')
                else:
                    self.message_send(event.user_id, 'Привет, друг.')

            elif self.get_message().lower() == 'поиск':
                self.message_send(event.user_id, 'Поиск начат.')
                self.params = self.vk_tools.get_profile_info(event.user_id) if self.params is None else self.params
                search_option = self.vk_tools.check_user_info(self.params, event.user_id)
                users = self.vk_tools.search_users(search_option, self.offset)
                self.offset += 10
                p_f_bot_db = BotDB()
                profile_id_db = p_f_bot_db.add_profile(self.params['name'], event.user_id)
                while len(users) != 0:
                    user = users.pop()
                    photos_user = self.vk_tools.get_photos(user['id'])
                    attachment = ''
                    if p_f_bot_db.get_worksheet(event.user_id, user['id']):
                        pass
                    else:
                        worksheet_id_db = p_f_bot_db.add_worksheet(user['name'], user['id'])
                        p_f_bot_db.add_viewed(profile_id_db, worksheet_id_db)
                        for photo in photos_user[:3]:
                            attachment += f'photo{photo["owner_id"]}_{photo["id"]},'
                        self.message_send(event.user_id,
                                        f'Имя {user["name"]}, ссылка: https://vk.com/id{user["id"]} . '
                                        f'Вам понравился этот человек? Напишите "да" или "нет".',
                                        attachment=attachment
                                        )
                        ans = self.get_message()
                        if ans == 'да':
                            p_f_bot_db.add_liked(profile_id_db, worksheet_id_db)
                p_f_bot_db.close()
            elif self.get_message().lower() == 'понравившиеся':
                p_f_bot_db_liked = BotDB()
                tuple_liked = p_f_bot_db_liked.get_liked(event.user_id)
                if tuple_liked:
                    response_text = ''
                    for (liked_user,) in tuple_liked:
                        response_text += f'Имя {(liked_user,)[0]}, ссылка: https://vk.com/id{(liked_user,)[1]} ,'
                    self.message_send(event.user_id, response_text)
                else:
                    self.message_send(event.user_id, 'У Вас нет понравившихся анкет.')

            elif self.get_message().lower() == 'пока':
                self.message_send(event.user_id, 'До новых встеч.')
            else:
                self.message_send(event.user_id, 'Команда не распознана.')


if __name__ == '__main__':
    bot = BotInterface(community_token)
    bot.event_handler()
