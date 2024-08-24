from pyrogram import Client, filters, types
from configparser import ConfigParser
from time import sleep
from pyrogram.errors import AboutTooLong
import re
from pyrogram.enums import MessageEntityType
# config init
config = ConfigParser()

config.read('config.ini')
api_id = config.get('pyrogram', 'api_id')
api_hash = config.get('pyrogram', 'api_hash')

print("bot has been started")

app = Client('my_account', api_id, api_hash)

emoji_dict = {
    ":smak:":     ["🤤", 5352935251310040127],
    ":clueless:": ["😐", 5352809039401079217]
}

@app.on_message(filters.me)
def chat_id(client_object, message: types.Message):
    for emoji, list in emoji_dict.items():
        if emoji in message.text:
            message.edit_text(text=message.text.replace(emoji, list[0]), entities=[types.MessageEntity(
                type=MessageEntityType.CUSTOM_EMOJI,
                offset=message.text.find(emoji),
                length=2,
                custom_emoji_id=list[1]
                )])

app.run()