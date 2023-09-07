from telethon.sync import TelegramClient
import csv

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

api_id = ''
api_hash = ''
phone = ''

client = TelegramClient(phone, api_id, api_hash)
client.start()
chats = []
last_date = None
size_chat = 200
groups = []

result = client(GetDialogsRequest(offset_date=last_date,
                                  offset_id=0,
                                  offset_peer=InputPeerEmpty(),
                                  limit=size_chat,
                                  hash=0))
chats.extend(result.chats)
for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

g = 0
for i in groups:
    print('Узнаём пользователей...')
    all_participants = []
    all_participants = client.get_participants(i)
    g+=1

    print('Сохраняем данные в файл...')
    file = str(g) + ".csv"
    with open(file, "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['id', 'username', 'name', 'phone'])
        for user in all_participants:
            if user.id:
                id = user.id
            else:
                id = "ID"
            if user.username:
                username = user.username
            else:
                username = "USERNAME"
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            if user.phone:
                phone = user.phone
            else:
                phone = "NONE"
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([id, username, name, phone, i.title])
    print(f'Парсинг участников группы {i.title} успешно выполнен.')
