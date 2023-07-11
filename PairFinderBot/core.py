import vk_api

from config import access_token
from vk_api.exceptions import ApiError
from datetime import datetime


class VkTools:

    def __init__(self, token):
        self.vkapi = vk_api.VkApi(token=token)

    def get_profile_info(self, user_id):

        try:
            info, = self.vkapi.method('users.get',
                                      {'user_id': user_id,
                                       'fields': 'sex, city, bdate'
                                       }
                                      )

        except ApiError as e:
            info = {}
            print(f'error = {e}')

        result = {'name': info['first_name'] + ' ' + info['last_name'] if
                  'first_name' in info and 'last_name' in info else None,
                  'sex': info.get('sex'),
                  'city': info.get('city')['title'] if info.get('city') is not None else None,
                  'bdate': info.get('bdate') if 'bdate' in info else None
                  }

        return result

    def search_users(self, options, offset):
        sex = 1 if options['sex'] == 2 else 2
        city = options['city']
        curent_year = datetime.now().year
        try:
            user_year = int(options['bdate'].split('.')[2])
        except AttributeError as e:
            print(f'error = {e}')
            user_year = options['bdate']
            if user_year is None:
                user_year = 0
        age = curent_year - user_year
        age_from = age - 5
        age_to = age + 5
        try:
            users = self.vkapi.method('users.search',
                                      {'count': 50,
                                       'offset': offset,
                                       'hometown': city,
                                       'sex': sex,
                                       'has_photo': True,
                                       'age_from': age_from,
                                       'age_to': age_to,
                                       'status': 6
                                       }
                                      )['items']
        except ApiError as e:
            print(f'error = {e}')
            return []
        res = []

        try:
            for user in users:
                if user['is_closed'] is False:
                    res.append({'id': user.get('id'),
                                'name': user['first_name'] + ' ' + user['last_name'] if
                                'first_name' in user and 'last_name' in user else None
                                }
                               )
        except TypeError as e:
            print(f'error = {e}')
            return res

        return res

    def get_photos(self, identifier):
        try:
            photos = self.vkapi.method('photos.get',
                                       {'user_id': identifier,
                                        'album_id': 'profile',
                                        'extended': 1
                                        }
                                       )['items']
        except ApiError as e:
            print(f'error = {e}')
            photos = []

        result = [{'owner_id': item['owner_id'],
                   'id': item['id'],
                   'likes': item['likes']['count'],
                   'comments': item['comments']['count']
                   } for item in photos
                  ]
        sort_result = sorted(result, key=lambda photo: int(photo['likes']) + int(photo['comments']), reverse=True)

        return sort_result


if __name__ == '__main__':
    profile_id = 162908903
    shift = 0
    tools = VkTools(access_token)
    params = tools.get_profile_info(profile_id)
    worksheets = tools.search_users(params, shift)
    worksheet = worksheets.pop()
    photos_user = tools.get_photos(worksheet['id'])
    print(params)
    print(worksheets)
    print(worksheet)
