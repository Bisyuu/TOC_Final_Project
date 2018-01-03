import json
import requests
import time
import urllib

from FSM import *
from DB_keyboard import *

TOKEN = '488534319:AAG-mAJxomYbuFwqfVNBMv2vVAP4aLd6SOM'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
    

def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    content = requests.get(url).content.decode("utf8")
    js = json.loads(content)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def send_message(text,chat_id,keyboard = None):
    url = URL + "sendMessage?text={}&chat_id={}".format(text,chat_id)
    if keyboard:
        url += "&reply_markup={}".format(keyboard)
    requests.get(url)


def send_result(information,chat_id):
    if information['Service'] == 'Search image':
        ID = Character_id[information['Character']]
        text = 'http://game-a.granbluefantasy.jp/assets/img/sp/assets/npc/zoom/' + ID
        if information['Level'] == "★ 1":
            text += '_01.png'
        elif information['Level'] == "★ 3":
            text += '_02.png'
        url = URL + "sendPhoto?photo={}&chat_id={}".format(text,chat_id)
        requests.get(url)
    elif information['Service'] == 'Search wiki':
        text = 'https://gbf.wiki/' + information['Character']
        send_message(text,chat_id)
    elif information['Service'] == 'Search gamewith':
        text = 'https://xn--bck3aza1a2if6kra4ee0hf.gamewith.jp/article/show/'
        text += Gamewith_id[information['Character']]
        send_message(text,chat_id)


def Initialize():
    updates = get_updates()
    if len(updates["result"]) > 0:
        last_update_id = get_last_update_id(updates) + 1
        url = URL + "getUpdates" + "?offset={}".format(last_update_id)
        requests.get(url)


def State_handler(machine, update, information):
    STATE = machine.state
    text = update["message"]["text"]
    chat_id = update["message"]["chat"]["id"]


    if STATE == 'Set_service':
        if text == "/start":
            send_message("Welcome,please choose the service",chat_id,Service_keyboard)
            return
        elif text == 'Select language':
            machine.Select_language()
        elif text == 'Search image':
            information['Service'] = 'Search image'
            machine.Image_set()
            machine.Element_SELECT()
        elif text == 'Search wiki':
            information['Service'] = 'Search wiki'
            machine.Wiki_set()
            machine.Element_SELECT()
        elif text == 'Search gamewith':
            information['Service'] = 'Search gamewith'
            machine.Gamewith_set()
            machine.Element_SELECT()
        else :
            send_message("No such command,use \"/start\" to start",chat_id)
            return
        send_message("Please select element of the character",chat_id,Element_keyboard)

    elif STATE == 'Set_element':
        if text == 'Back':
            machine.Reset()
            send_message("Welcome,please choose the service",chat_id,Service_keyboard)
        elif text in Element_list:
            information['Element'] = text
            machine.Element_OK()
            send_message("Please select character",chat_id,Character_keyboard[information['Element']])
        else :
            send_message("Please select element of the character",chat_id,Element_keyboard)

    elif STATE == 'Set_character':
        if text == 'Reset':
            machine.Reset()
            send_message("Welcome,please choose the service",chat_id,Service_keyboard)
        elif text == 'Back':
            machine.Element_REDO()
            send_message("Please select element of the character",chat_id,Element_keyboard)
        elif text in Character_list:
            information['Character']=text
            machine.Character_OK()
            if information['Service'] == 'Search image':
                send_message("Please select level",chat_id,Level_keyboard)
            else :
                send_result(information,chat_id)
                send_message("Finished. Use \"/start\" for next search.",chat_id)
                machine.Level_OK()
        else :
            send_message("Please select character",chat_id,Character_keyboard[information['Element']])

    elif STATE == 'Set_level':
        if text == 'Reset':
            machine.Reset()
            send_message("Welcome,please choose the service",chat_id,Service_keyboard)
        elif text == 'Back':
            machine.Character_REDO()
            send_message("Please select character",chat_id,Character_keyboard[information['Element']])
        else:
            information['Level'] = text
            machine.Level_OK()
            send_result(information,chat_id)
            send_message("Finished. Use \"/start\" for next search.",chat_id)
        
class Data:
    machine = StateMachine(states = states, transitions = transitions, initial = 'Set_service')
    information = {'Service': 'None', 'Element': 'None', 'Character': 'None', 'Level': 'None'}


def main():
    UserDict = {}
    last_update_id = None

    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            for update in updates["result"]:
                chat_id = update["message"]["chat"]["id"]
                if chat_id not in UserDict:
                    UserDict[chat_id] = Data()
                print(chat_id)
                State_handler(UserDict[chat_id].machine, update, UserDict[chat_id].information)
            last_update_id = get_last_update_id(updates) + 1
        time.sleep(0.5)


if __name__ == '__main__':
    Initialize()
    main()
