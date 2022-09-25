import telebot
import json
import io

json_PATH = ''  # Path to json with coordinates
bot_TOKEN = ''  # Token of Telegram Bot.


def CheckJson(id, coordinates, user):
    with io.open(json_PATH, encoding='utf-8') as my_file:
        json_raw = my_file.read()
    json_decoded = json.loads(json_raw)
    json_features = json_decoded['features']
    is_founded = False
    for x in json_features:
        if x['id'] == id:
            x['geometry']['coordinates'] = coordinates
            is_founded = True

    if is_founded == False:
        new_user = ({"type": "Feature",
                     "id": id,
                     "geometry": {
                         "type": "Point",
                         "coordinates": coordinates
                     },
                     "properties": {
                         "balloonContent": "На базе",
                         "clusterCaption": user,
                         "hintContent": user,
                         "iconCaption": user
                     },
                     "options": {
                         "iconLayout": "default#image",
                         "iconImageHref": "/ПАТРИОТ.png",
                         "iconImageSize": [70, 40],
                         "iconImageOffset": [-25, -10]
                     }
                     })
        json_decoded['features'].append(new_user)

    json_encoded = json.dumps(json_decoded, indent=4)
    return json_encoded


def UpdateFile(message):
    location = [message.location.latitude, message.location.longitude]  # getting options for checking
    id = message.from_user.id
    user = message.from_user.username

    with open(json_PATH, "w") as my_file:  # updating json file
        my_file.write(CheckJson(id, location, user))
        print('Updated')


bot = telebot.TeleBot(bot_TOKEN)


@bot.message_handler(commands=["start"])  # start message
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )')


@bot.edited_message_handler(content_types=["location"])  # handling all messages with location type
def handle_text(message):
    UpdateFile(message)


bot.polling(none_stop=True, interval=0)
