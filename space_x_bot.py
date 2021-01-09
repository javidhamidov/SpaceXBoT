import telebot
import requests
import json

API_TOKEN = ''

launches_link = 'https://api.spacexdata.com/v4/launches'
payloads_link = 'https://api.spacexdata.com/v4/payloads/'
crew_link = 'https://api.spacexdata.com/v4/crew'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['latest'])
def five_last_launches(message):
    text = message.text.split(" ")
    if len(text) == 1:
        chat_id = message.chat.id
        response = requests.get(launches_link)
        launches = json.loads(response.text)
        first_five = []
        for launch in launches[:5]:
            first_five.append(launch)
        for launch in first_five:
            text = 'Name: {}\nLink: {}\nID: {}'.format(launch['name'], launch['links']['wikipedia'], launch['id'])
            bot.send_message(chat_id, text)
    else:
        bot.reply_to(message, "You do not have to give me any other details")

@bot.message_handler(commands=['launch'])
def launch_id(message):
    text = message.text.split(" ")
    if len(text) == 2:
        chat_id = message.chat.id
        response = requests.get(launches_link)
        launches = json.loads(response.text)
        launch_name = ''
        launch_description = ''
        launch_payload = ''
        launch_image_link = ''
        for launch in launches:
            if launch['id'] == text[1]:
                launch_name = launch['name']
                launch_description = launch['details']
                launch_image_link = launch['links']['patch']['small']
                launch['total_mass'] = 0
                for payload in launch['payloads']:
                    final_payloads_link = payloads_link + payload
                    response = requests.get(final_payloads_link)
                    payload_data = json.loads(response.text)
                if payload_data['mass_kg']:
                    launch['total_mass'] += payload_data['mass_kg']
                launch_payload = launch['total_mass']
        text = 'Name: {}\nDescription: {}\nTotal payload: {}'.format(launch_name, launch_description, launch_payload)
        r = requests.get(launch_image_link)
        bot.send_photo(chat_id, r.content)
        bot.send_message(chat_id, text)
    else:
        bot.reply_to(message, "Incorrect structure of the message!\nIt should be : /launch id")

@bot.message_handler(commands=['crew'])
def crew_members_info(message):
    text = message.text.split(" ")
    if len(text) == 1:
        chat_id = message.chat.id
        response = requests.get(crew_link)
        crew_members = json.loads(response.text)
        for crew_member in crew_members:
            r = requests.get(crew_member['image'])
            text = 'Name: {}\nWikipedia: {}'.format(crew_member['name'], crew_member['wikipedia'])
            bot.send_photo(chat_id, r.content)
            bot.send_message(chat_id, text)
    else:
        bot.reply_to(message, "You do not have to give me any other details")

bot.polling()