import vk_api, json, random, unicodedata, requests, sqlite3
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import database
from config import vk_token


def write_msg(user_id, message, random_id):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64)})

def sender(id, text):
    vk.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : 0, 'keyboard' : keyboard})
		

def normalize_caseless(text):
    return unicodedata.normalize("NFKD", text.casefold())

def prov(left, right):
    return normalize_caseless(left) == normalize_caseless(right)


# API
token = vk_token
vk = vk_api.VkApi(token=token)
random_id = random.getrandbits(64)

def get_but(text, color):
	return {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"" + "1" + "\"}",
                    "label": f"{text}"
                },
                "color": f"{color}"
            }

def main_keyboard():
    keyboard = {
	    "one_time" : False,
	    "buttons" : [
	            [get_but('Регистрация', 'positive')],
                    [get_but('Информация', 'positive')], 
                    [get_but('Дискорд канал' , 'positive')],
                    [get_but('Тех. поддержка' , 'secondary')]
	            
	    ]
    }
    
    keyboard = json.dumps(keyboard, ensure_ascii = False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))   
    return keyboard

def reg_keyboard():
    keyboard = {
                "one_time" : False,
                "buttons" : [
                    [get_but('Dota id', 'positive')],
                    [get_but('Discord', 'positive')],
                    [get_but('Подтверждение регистрации', 'positive')],
                    [get_but('Назад' , 'negative')]
            
                ]
            }
    
    keyboard = json.dumps(keyboard, ensure_ascii = False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard

def agree_keyboard():
    keyboard = {
                "one_time" : False,
                "buttons" : [
                    [get_but('Всё верно', 'positive')],
                    [get_but('Изменить' , 'negative')]
            
                ]
            }
    
    keyboard = json.dumps(keyboard, ensure_ascii = False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard

keyboard = main_keyboard()

#работа с сообщениями
longpoll = VkLongPoll(vk)

for event in longpoll.listen():
    
    if event.type == VkEventType.MESSAGE_NEW:
	
        if event.to_me:

            request = event.text
            vk_id = event.user_id
	    
            con = sqlite3.connect("users.db")
            cur = con.cursor()            
            database.db_create(cur)
	    
            if prov(request,'Регистрация'):
                database.db_vkid(vk_id, cur, con)
                keyboard = reg_keyboard()	
                sender(event.user_id, "Выберите нужный раздел регистрации. \n \n Когда вы введете dota id и дискорд, то нажмите на кнопку 'Подтверждение регистрации'. \n Берите в учет, что после подтверждения регистрации вы больше не сможете изменить свой дискорд и dota id, поэтому заранее убедитесь что правильно ввели данные.")
	    
	    #____________Dota id____________
            elif prov(request, 'Dota id'):
		
                if database.db_dotaid_check(vk_id, '0', cur, con) == True:
                    sender(event.user_id, "Напишите ваш id в такой формате (Dota id 'Ваш id')")
                    vk.method("messages.send", {"peer_id": event.user_id,"attachment": 'photo-213981306_457239050', "random_id": 0})		    
		    
                else:
                    dota_id = database.db_dotaid_check(vk_id, '0', cur, con)
                    sender(event.user_id, f"Вы уже зарегеистрировали свой дота id ({dota_id}). \n \n В случае ошибки можете удалить его написав 'Dota id delete' и вписать верный.")
	    
            elif prov(request[0:7], 'Dota id') and request[8:].isdigit() == True:
		
                dota_id = request[8:]
                if database.db_dotaid(vk_id, dota_id, cur, con) == False:
                    sender(event.user_id, "Вы уже зарегеистрировали свой дота id. \n \n В случае ошибки можете удалить его написав 'Dota id delete' и вписать верный.")
                
                elif database.db_dotaid_check(vk_id, dota_id, cur, con) == 'Have':
                    sender(event.user_id, 'Такой Dota id уже зарегестрирован другим пользователем')		
                
                else:
                    sender(event.user_id, 'Вы успешно зарегестрировали свой dota id.')
		    
            elif prov(request, 'Dota id delete'):
                if database.db_dota_id_del(vk_id, cur, con) == False:
                    sender(event.user_id, 'Вы уже подтвердили регистрацию и не можете изменить dota id. \n \n Вы также можете обратиться в тех. поддержку для решения этой проблемы, но будьте готовы, что вам могут отказать в повторной замене')
                else:
                    sender(event.user_id, 'Вы успешно отчистили свой dota id. \n \n Теперь можете повторно ввести его.')

            #____________Discord id____________
            elif prov(request, 'Discord'):
		
                if database.db_dsid_check(vk_id, '0', cur, con) == True:
                    sender(event.user_id, "Напишите ваш Discord в такой формате (Discord 'Ваш ник и id')")
                    vk.method("messages.send", {"peer_id": event.user_id,"attachment": 'photo-213981306_457239051', "random_id": 0})
                else:
                    ds_id = database.db_dsid_check(vk_id, '0', cur, con)
                    sender(event.user_id, f"Вы уже зарегеистрировали свой Дискорд ({ds_id}). \n \n В случае ошибки можете удалить его написав 'Discord delete' и вписать верный.")
  
            elif prov(request[0:7], 'Discord'):
		
                ds_id = request[8:]
                if database.db_dsid(vk_id, ds_id, cur, con) == False:
                    sender(event.user_id, "Вы уже зарегеистрировали свой Дискорд. \n \n В случае ошибки можете удалить его написав 'Discord delete' и вписать верный.")
                
                elif database.db_dsid_check(vk_id, ds_id, cur, con) == 'Have':
                    sender(event.user_id, 'Такой Discord уже зарегестрирован другим пользователем')
                
                else:
                    sender(event.user_id, 'Вы успешно зарегестрировали свой Discord.')
		    
            elif prov(request, 'Discord delete'):
                if database.db_ds_id_del(vk_id, cur, con) == False:
                    sender(event.user_id, 'Вы уже подтвердили регистрацию и не можете изменить дискорд. \n \n Вы также можете обратиться в тех. поддержку для решения этой проблемы, но будьте готовы, что вам могут отказать в повторной замене')
                else:
                    sender(event.user_id, 'Вы успешно отчистили Discord. \n \n Теперь можете повторно ввести его.')	    

            elif prov(request, 'Дискорд канал'):
                sender(event.user_id, 'https://discord.gg/FDpnaEjfvq')  
		
            elif prov(request,'Информация'):
                sender(event.user_id, "После того как ты введешь свой дс, то будешь добавлен в вайт лист на дискорд сервере. Когда ты на него зайдешь тебе будет выдана роль участника в турнире")
	    
            elif prov(request, 'Тех. поддержка'):
                sender(event.user_id, "Если вы столкнулись с какой-либо проблемой, то предлагаем вам прочитать FAQ по турниру: \n https://vk.com/topic-213981306_49083515 \n \n В случае если в FAQ сказано обратиться в [id196550371|тех. поддержку], либо же вашего вопроса нет в руководстве, то сделайте это.")
		
            elif prov(request, 'Подтверждение регистрации'):
                check = database.agree_reg_check(vk_id, cur, con)
                if check == False:
                    sender(event.user_id, "Вы пока не зарегистрировали dota id и/или дискорд.")
                elif check == 'Have':
                    sender(event.user_id, "Вы уже подтвердили регистрацию.")
                else:
                    keyboard = agree_keyboard()
                    sender(event.user_id, f"Вы уверены в правильности введенных данных? \n \n dota id - {check[0][2]} \n Discord - {check[0][1]} \n \n Предупреждаем, что после подтверждения вы больше не сможете изменить данные.")
	    
            elif prov(request, 'Всё верно'):
                check = database.agree_reg(vk_id, cur, con)
                if check == False:
                    sender(event.user_id, "Вы прошли не зарегестрировали dota id или дискорд.")
                elif check == 'Have':
                    sender(event.user_id, "Вы уже подтвердили регистрацию.")
                elif check == 'Agree':
                    keyboard = main_keyboard()
                    sender(event.user_id, "Вы успешно подтвердили регистрацию")
		    
            elif prov(request, 'Изменить'):
                keyboard = reg_keyboard()
                sender(event.user_id, "Ждем твоего возвращения.")
		
            elif prov(request,'Назад'):
                keyboard = main_keyboard()
                sender(event.user_id, 'Возвращаемся обратно.')
		
            else:
                keyboard = main_keyboard()
                sender(event.user_id, 'Команда не найдена')
		