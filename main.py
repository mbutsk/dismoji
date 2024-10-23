from pyrogram import Client, filters, types
from configparser import ConfigParser
from time import sleep
from pyrogram.errors import AboutTooLong
import re
from pyrogram.enums import MessageEntityType
import json
import os
import logging
import sys

if not os.path.isfile("emojis.json"):
    with open("emojis.json", "w") as file:
        json.dump({}, file)


# config init
config = ConfigParser()

config.read('config.ini')
api_id = config.get('pyrogram', 'api_id')
api_hash = config.get('pyrogram', 'api_hash')

print("bot has been started")

app = Client('my_account', api_id, api_hash)

@app.on_message(filters.me & filters.command("add_emoji"))
def add_emoji(client_object, message: types.Message):
    emoji = message.text.split(" ")[1]
    emoji_name = message.text.replace(f"/add_emoji {emoji} ", "")
    emoji_id = message.entities[0].custom_emoji_id

    with open('emojis.json', encoding="UTF-8") as file:
        emoji_dict = json.load(file)
    
    emoji_dict[emoji_name] = [emoji, emoji_id]
    with open('emojis.json', 'w') as file:
        json.dump(emoji_dict, file)
    app.send_message(message.chat.id, f"Успешно добавлен эмодзи {emoji} с названием {emoji_name}", entities=[types.MessageEntity(
                type=MessageEntityType.CUSTOM_EMOJI,
                offset=24,
                length=2,
                custom_emoji_id=emoji_id
                )])

    

@app.on_message(filters.me)
def dismoji(client_object, message: types.Message):
    with open('emojis.json', encoding="UTF-8") as file:
        emoji_dict = json.load(file)
    entities = []
    increase = 0
    new_text = message.text
    for emoji, emoji_list in emoji_dict.items():
        if emoji in message.text:
            for i in range(message.text.count(emoji)):
                entities.append(types.MessageEntity(
                        type=MessageEntityType.CUSTOM_EMOJI,
                        offset=new_text.find(f":{emoji}:") + increase,
                        length=2,
                        custom_emoji_id=emoji_list[1]
                        ))
                new_text = new_text.replace(f":{emoji}:", emoji_list[0])
                increase+=1
    print(entities)
    message.edit_text(text=new_text, entities=entities)
    
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
app.run()