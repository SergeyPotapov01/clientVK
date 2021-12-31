import os

import vk_api

from vk_api.utils import get_random_id


class ClientVK:
    def __init__(self):
        vk = vk_api.VkApi(login='login', password='password', app_id=2685278)
        vk.auth()
        self.vk = vk.get_api()
        self.audio = os.listdir('audio')

    def clearTerminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _getChats(self):
        """
        Получение массив последних 20 диалогов
        """
        filthyJson = self.vk.messages.getConversations()
        chats = []
        for i in filthyJson['items']:
            if i['conversation']['peer']['type'] == 'user':
                userInfo = self.vk.users.get(user_ids=i['conversation']['peer']['id'])
                chats.append((userInfo[0]['first_name'], userInfo[0]['last_name'], i['conversation']['peer']['id']))
            elif i['conversation']['peer']['type'] == 'group':
                chats.append((self.vk.groups.getById(group_ids=i['conversation']['peer']['id'] * (-1))[0]['name'],
                                                       i['conversation']['peer']['id']))
            elif i['conversation']['peer']['type'] == 'chat':
                chats.append((i['conversation']['chat_settings']['title'], i['conversation']['peer']['id']))
        return chats

    def _sendAudioMessage(self, file: str, id: str) -> int:
        """
        1   путь к файлу

        2
            Для пользователя:
            id пользователя.

            Для групповой беседы:
            (2000000000: int + id: int) беседы. id беседы для каждого пользователя уникально из-за особенности вк

            Для сообщества:
            -id сообщества.

        :return: id сообщения
        """
        json = vk_api.upload.VkUpload(self.vk).audio_message(r'{0}'.format(file), id)
        return self.vk.messages.send(peer_id=int(id),
                                   attachment='audio_message{0}_{1}>'.format(str(json['audio_message']['owner_id']),
                                                                             str(json['audio_message']['id'])),
                                   random_id=get_random_id())

    def gui(self):
        while True:
            self.clearTerminal()
            inquiry = input('1 - Отправить ГС\nВыбор действия: ')
            if inquiry == '1':
                chats = self._getChats()

                self.clearTerminal()
                for i in range(len(chats)):
                    print(i, chats[i])
                try:
                    id = chats[int(input('Кому отправить?: '))][-1]
                except:
                    continue

                self.clearTerminal()
                for i in range(len(self.audio)):
                    print(i, self.audio[i])

                try:
                    file = 'audio/' + self.audio[int(input('Что отправить?: '))]
                except:
                    continue
                self._sendAudioMessage(file, id)

    def main(self):
        self.gui()

if __name__ == '__main__':
    ClientVK().main()