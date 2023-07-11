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

            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()
                if command == 'привет':
                    self.params = self.vk_tools.get_profile_info(event.user_id)
                    if self.params["name"] is not None:
                        self.message_send(event.user_id, f'Привет, {self.params["name"]}. '
                                                         f'Доступны команды:\nзадать поиск - Поиск,\n'
                                                         f'получить список понравившихся анкет - Лайки.')
                    else:
                        self.message_send(event.user_id, f'Привет, друг. '
                                                         f'Доступны команды:\nзадать поиск - Поиск,\n'
                                                         f'получить список понравившихся анкет - Лайки.')

                elif command == 'поиск':
                    self.message_send(event.user_id, 'Поиск начат.')
                    self.params = self.vk_tools.get_profile_info(event.user_id) if self.params is None else self.params

                    if self.params['sex'] is None:
                        self.message_send(event.user_id, 'Напишите какой у Вас пол: женский или жужской.')
                        ans_sex = self.get_message()
                        sex = 2 if ans_sex.lower() == 'жужской' else 1
                    else:
                        sex = self.params['sex']

                    if self.params['city'] is None:
                        self.message_send(event.user_id, 'Какой у Вас город проживания (полное название)?')
                        city = self.get_message().lower()
                    else:
                        city = self.params['city']

                    if self.params['bdate'] is None:
                        self.message_send(event.user_id, 'Какой у Вас год рождения?')
                        bdate = int(self.get_message())
                    else:
                        bdate = self.params['bdate']

                    search_option = {'sex': sex, 'city': city, 'bdate': bdate}
                    users = self.vk_tools.search_users(search_option, self.offset)
                    if not users:
                        self.message_send(event.user_id, f'Извините, команда Поиск пока не работает.'
                                                         f'Но вы можете посмотреть понравившиеся, отправив Лайки. ')
                    self.offset += 50
                    p_f_bot_db = BotDB()
                    profile_id_db = p_f_bot_db.add_profile(event.user_id)
                    while len(users) != 0:
                        user = users.pop()
                        photos_user = self.vk_tools.get_photos(user['id'])
                        attachment = ''
                        if not p_f_bot_db.get_worksheet(event.user_id, user['id']):
                            worksheet_id_db = p_f_bot_db.add_worksheet(user['name'], user['id'])
                            p_f_bot_db.add_viewed(profile_id_db, worksheet_id_db)
                            for photo in photos_user[:3]:
                                attachment += f'photo{photo["owner_id"]}_{photo["id"]},'
                            if attachment:
                                self.message_send(event.user_id,
                                                  f'Имя {user["name"]}, ссылка: https://vk.com/id{user["id"]} . '
                                                  f'Вам понравился этот человек? Напишите "да" или "нет".',
                                                  attachment=attachment
                                                  )
                                ans = self.get_message()
                                if ans == 'да':
                                    p_f_bot_db.add_liked(profile_id_db, worksheet_id_db)
                    p_f_bot_db.close()
                elif command == 'лайки':
                    p_f_bot_db_liked = BotDB()
                    tuple_liked = p_f_bot_db_liked.get_liked(event.user_id)
                    p_f_bot_db_liked.close()
                    if tuple_liked:
                        response_text = ''
                        for liked_user in tuple_liked:
                            response_text += f'Имя: {liked_user[0]}, ссылка: https://vk.com/id{liked_user[1]} ,\n'
                        self.message_send(event.user_id, response_text)
                    else:
                        self.message_send(event.user_id, 'У Вас нет понравившихся анкет.')

                elif command == 'пока':
                    self.message_send(event.user_id, 'До новых встеч.')

                else:
                    if command == 'да' or 'нет':
                        pass
                    else:
                        self.message_send(event.user_id, f'Команда не распознана. Отправьте слово "привет",'
                                                         f'чтобы получить список доступных команд.')


if __name__ == '__main__':
    bot = BotInterface(community_token)
    bot.event_handler()
