''' Бот для програмы OlegsBank_Bot на основе родной библиотеки telegram для мессенджера'''
import telegram
from telegram.error import NetworkError, Unauthorized
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram import ReplyKeyboardHide
import OleggBot_config
import datetime
import time

update_id = None

def qa (dictionary, question):
    if question in dictionary:
        return dictionary[question]
    else:
        return "Интересный вопрос.  Дай мне подумать! А пока спроси что-нибудь другое"

def replykeyboard_two():
    keyboard = [[KeyboardButton("Есть деньги"),
                 KeyboardButton("Нужны деньги")],

                [KeyboardButton("Карта"),
                 KeyboardButton("Обмен"),
                 KeyboardButton("Перевод")]]

    reply_markup = ReplyKeyboardMarkup(keyboard , resize_keyboard = True )
    return reply_markup

def replykeyboard_credit():
    keyboard = [[KeyboardButton("Жене сапоги"),
                 KeyboardButton("Авто"),
                 KeyboardButton("Хату")],                 

                [KeyboardButton("Хочу карту"),
                 KeyboardButton("Позвони мне", request_contact = True ),
                 KeyboardButton("Назад...")]]

    reply_markup = ReplyKeyboardMarkup(keyboard,  resize_keyboard = True  )
    return reply_markup

def replykeyboard_invest():
    keyboard = [[KeyboardButton("Вклад"),
                 KeyboardButton("Акции"),
                 KeyboardButton("ПИФы")],                 

                [KeyboardButton("Облигации"),
                 KeyboardButton("Назад...")]]

    reply_markup = ReplyKeyboardMarkup(keyboard,  resize_keyboard = True  )
    return reply_markup


def replykeyboard_obmen():
    keyboard = [[KeyboardButton("Где обменник близко?", request_location = True)],
                                  
                [KeyboardButton("Доллар"),
                 KeyboardButton("Евро"),
                 KeyboardButton("Фунт")],

                [KeyboardButton("Назад...")]]

    reply_markup = ReplyKeyboardMarkup(keyboard,  resize_keyboard = True  )
    return reply_markup

def replykeyboard_card():
    keyboard = [[KeyboardButton("Кредитная"),
                KeyboardButton("Дебетовая")],
                                  
                [KeyboardButton("В рублях"),
                 KeyboardButton("В валюте")],

                [KeyboardButton("Назад...")]]

    reply_markup = ReplyKeyboardMarkup(keyboard,  resize_keyboard = True  )
    return reply_markup


def replykeyboard_yesno():
    keyboard = [KeyboardButton("Да"),
                KeyboardButton("Нет"),       
                KeyboardButton("Не знаю")]

    reply_markup = ReplyKeyboardMarkup(keyboard,  resize_keyboard = True  )
    return reply_markup


def hidekeys(chat_id):
    bot.sendMessage(chat_id=chat_id,  text = 'Спросите меня о чем-нибудь', reply_markup = ReplyKeyboardHide (hide_keyboard = True))
    pass

def stat(time_of_start):
    time_of_work =  time_of_start - datetime.datetime.now()
    return ("Я уже работаю " + str(time_of_work))
 
def save_history (file, message_id, questnum, datestamp, question, answer,  chat_id, update_id, username, user_firstname, user_lastname, user_id):
    file.write("{ 'QuestionNum': %s, 'Message_id': %s,  'Date': %s, 'question': %s, 'answer' : %s, 'chat_id': %s, 'update_id': %s, 'username': %s, 'user_firstname': %s, 'user_lastname': %s, 'user_id': %s} \n" 
        % (questnum, message_id,  datestamp, question, answer,  chat_id, update_id, username, user_firstname, user_lastname, user_id))
 
def echo(bot, questnum , file):
    global update_id
    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        
        if type (update) == None:
            continue
        else:
            # сохранить всю запись Update в файл для  последующего анализа
            techfile = open ('OleggBot_file.json', 'a')
            techfile.write(str(update) + '\n')
            techfile.close()

            
            # chat_id is required to reply to any message
            chat_id = update.message.chat_id
            update_id = update.update_id + 1
            # Возьмем разную статистику-параметры с каждого сообщения в чате
            message_id = update.message.message_id
            datemsg = update.message.date
            
            # Получим инфо о пользователе,пославшем этот запрос
            username = update.message.from_user.username
            user_firstname = update.message.from_user.first_name
            user_lastname = update.message.from_user.last_name
            user_id = update.message.from_user.id
     
     
            if update.message:  # your bot can receive updates without messages
                # Reply to the message

                question = update.message.text
                
                while True:
                    if question == '/start':
                       otvet = 'Я все знаю про банки и про бабки. Mогу ответить на твои вопросы. Задавай любые'
                       bot.sendMessage(chat_id=chat_id, parse_mode  = 'Markdown', text = otvet, reply_markup = replykeyboard_two() )
                       return update.message.text
                    elif question == 'Ты кто?' or question == 'кто ты?' or question == 'как тебя зовут?' or question == 'Как тебя зовут?':
                       otvet = 'Я ж Олег. Не узнал? https://dl.dropboxusercontent.com/u/64262910/oleggbank/what_is_this_good.jpg'
                       bot.sendMessage(chat_id=chat_id, parse_mode  = 'Markdown', text = otvet, reply_markup = replykeyboard_two() )
                       return update.message.text
                    elif question == "/stat":
                       otvet = 'Я уже ответил на %s вопросов' % questnum 
                       bot.sendChatAction (chat_id=chat_id, action = 'typing')
                       bot.sendMessage(chat_id=chat_id, text= stat(time_of_start))
                       bot.sendMessage(chat_id=chat_id, parse_mode  = 'Markdown', text=otvet,  reply_markup=replykeyboard_two() )
                       # Стараемся записать в файл
                       save_history (file, questnum, message_id, datemsg, question, otvet,  chat_id, update_id, username, 
                        user_firstname, user_lastname, user_id)
                       return update.message.text
                    elif question == "/hide":
                       hidekeys(chat_id)
                       return update.message.text
                    elif update.message.location:
                       location = update.message.location
                       question = "{longitude: %s, 'latitude': %s }" % (location.longitude ,location.latitude)
                       otvet = 'Спасибо, что теперь я знаю где ты! Сейчас найду тебе обменник поблизости. https://dl.dropboxusercontent.com/u/64262910/oleggbank/fine2.jpg'
                       bot.sendMessage(chat_id=chat_id, text= otvet)
                       save_history(file, questnum, message_id, datemsg, question, otvet, chat_id, update_id, username, 
                        user_firstname, user_lastname, user_id)
                       return update.message.text
                    elif update.message.contact:
                       u = update.message.contact
                       question = "{'user_id': %s, 'phone_number': %s, 'first_name': %s, 'last_name': %s}" % (u.user_id, u.phone_number, u.first_name, u.last_name)
                       otvet = 'Спасибо за телефончик. Я передам девочкам из колл-центра. Они тебе устроят s.x по телефону https://dl.dropboxusercontent.com/u/64262910/oleggbank/everything_ok.jpg '
                       bot.sendMessage(chat_id=chat_id, text= otvet)
                       save_history(file, questnum, message_id, datemsg, question, otvet, chat_id, update_id, username, 
                        user_firstname, user_lastname, user_id)
                       return update.message.text
                    elif question == 'Есть деньги':
                       otvet = 'Поздравляю, счастливчик!  У  40% россиян их уже нет. Куда хочешь вложить?'  
                       bot.sendMessage(chat_id=chat_id, text = otvet, reply_markup=replykeyboard_invest() )
                       save_history(file, questnum, message_id, datemsg, question, otvet, chat_id, update_id, username, 
                        user_firstname, user_lastname, user_id)
                       return update.message.text                        
                    elif question == 'Нужны деньги':
                       otvet = 'Я тебя понимаю... Мне тоже нужны. А тебе на что?'  
                       bot.sendMessage(chat_id=chat_id, text = otvet, reply_markup=replykeyboard_credit() )
                       save_history(file, questnum, message_id, datemsg, question, otvet, chat_id, update_id, username, 
                        user_firstname, user_lastname, user_id)
                       return update.message.text                        
                    elif question == 'Обмен':
                       otvet = 'Валютку решил поменять... Ну что ж, выбирай:'   
                       bot.sendMessage(chat_id=chat_id, text = otvet, reply_markup=replykeyboard_obmen() )
                       save_history(file, questnum, message_id, datemsg, question, otvet, chat_id, update_id, username, 
                        user_firstname, user_lastname, user_id)
                       return update.message.text                        
                    elif question == 'Карта':
                       otvet = 'Выбери карту'   
                       bot.sendMessage(chat_id=chat_id, text = otvet, reply_markup=replykeyboard_card() )
                       save_history(file, questnum, message_id, datemsg, question, otvet, chat_id, update_id, username, 
                        user_firstname, user_lastname, user_id)
                       return update.message.text
                    elif question == 'Назад...':
                       otvet = 'Что у тебя снова?'
                       bot.sendMessage(chat_id=chat_id, text = otvet, reply_markup=replykeyboard_two() )
                       save_history(file, questnum, message_id, datemsg, question, otvet, chat_id, update_id, username, 
                        user_firstname, user_lastname, user_id)
                       return update.message.text
                    elif question == 'Не знаю':
                       otvet = '''Давай я научу.  "Всего банки решают пять типовых задач клиентов.
                                    1) есть деньги надо вложить, чтоб не пропали
                                    2) нет денег, надо занять
                                    3) перевести деньги жене, собаке, в Таджикистан, оплатить какую-нибудь фигню и т.п.
                                    4) поменять валюту
                                    5) ну и конечно карточку открыть. и конечно у Тинькова.
                                    Все понятно?'''
                       bot.sendMessage(chat_id=chat_id, text = otvet, reply_markup=replykeyboard_yesno() )
                       save_history(file, questnum, message_id, datemsg, question, otvet, chat_id, update_id, username, 
                        user_firstname, user_lastname, user_id)
                       return update.message.text   
                    elif question == 'счастливо' or question == 'пока' or question == 'до свидания' or question == 'прощай' or question == 'досвидос' or question == 'до завтра':
                       otvet = 'Давай, до свиданья.  https://dl.dropboxusercontent.com/u/64262910/oleggbank/go_there.jpg'
                       bot.sendMessage(chat_id=chat_id, text = otvet, reply_markup=hidekeys() )
                       save_history(file, questnum, message_id, datemsg, question, otvet, chat_id, update_id, username, 
                        user_firstname, user_lastname, user_id)
                       return update.message.text

                    else: 
                       otvet = qa(OleggBot_config.VALBOT, question)
                       bot.sendMessage(chat_id=chat_id, parse_mode  = 'Markdown', text= otvet)
                       # Стараемся записать в файл
                       save_history(file, questnum, message_id, datemsg, question, otvet, chat_id, update_id, username, user_firstname, user_lastname, user_id)
                       return update.message.text
    

                bot.sendMessage(chat_id=chat_id, text=update.message.text)





if __name__ == '__main__':
    time_of_start = datetime.datetime.now()
    global update_id
    # Telegram Bot Authorization Token - ОТ МОЕГО бота  Valutas
    bot = telegram.Bot(OleggBot_config.token)
 
    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    
    questnum = 0
    try:
        update_id = bot.getUpdates()[0].update_id

    
    except IndexError:
        update_id = None
    
    while True:
        try:
            # Здесь добавляем запись в файл истории вопросов-ответов
            history = open ('OlegBot_History.txt', 'a' )
            
            echo(bot, questnum, history)
            questnum += 1
            history.close()

            
        except NetworkError:
            time.sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1
    
