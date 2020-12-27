#! /usr/bin/env python
# -*- coding: utf-8 -*-
#vim:fileencoding=utf-8
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from leafCheck import leafCheck
from processLeaf import process
from RUclassifyLeaf import classify

import random

model_name = 'KNN'

def my_help(update: Update, context):
    a = """
    /start - начать чат
    /help - список существующих команд
    /trees_list - известные мне деревья
    /model - вывести текущую модель
    Если лист дерева сложный (состоит из нескольких маленьких), сфотографируйте только верхний листик, пожалуйста
    """
    update.message.reply_text(a)


def start(update, context):
    update.message.reply_text('Отправьте мне фото листа на светлом нейтральном фоне. Я постараюсь определить, какому дереву он принадлежал :)')


def get_image(update: Update, context):
    file_id = update.message.photo[-1].file_id
    photo = context.bot.getFile(file_id)
    photo.download(file_id+'.png')
    checkedImage,cnt,coord = leafCheck(file_id+'.png')
    os.remove(file_id+'.png')
    if type(checkedImage) != str:
        update.message.reply_text(random.choice([
            'Отличное фото!',
            'Минутку, посмотрю в справочнике',
            'Всё в порядке, обрабатываю',
        ]))
        features = process(checkedImage,cnt,coord)
        result1 = classify(features, model_name)
        keyboard = [[InlineKeyboardButton(result1.capitalize(), 
                                          callback_data=result1)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Скорее всего, это ' + result1 +
                                  '. Подробнее об этом виде:', reply_markup=reply_markup)
    else:
        update.message.reply_text(checkedImage)


def reply_text(update, context):
    global model_name
    ch = update.message.text[0]
    if ch == '1':
        model_name = 'KNN'
        update.message.reply_text('Модель изменена на K-Nearest Neighbors')
    elif ch == '2':
        model_name = 'DTC'
        update.message.reply_text('Модель изменена на Decision Tree')
    elif ch == '3':
        model_name = 'GNB'
        update.message.reply_text('Модель изменена на Gaussian Naive Bayes')
    elif ch == '4':
        model_name = 'RFC'
        update.message.reply_text('Модель изменена на Random Forest')
    elif ch == '5':
        model_name = 'SVC'
        update.message.reply_text('Модель изменена на C-Support Vector Classification')
    else:
        update.message.reply_text(random.choice([
            'Следите, чтобы пальцы не попали в кадр',
            'Хотите узнать, какое рядом с вами дерево?',
            'Погода отличная, пора в парк!',
            'Пожалуйста, отправьте мне фото листика'
        ]))


def trees_list(update, context):
    myfile = open("trees.txt")
    msg = myfile.read()
    myfile.close()
    keyboard = list(map(create_button, msg.split('\n')))
    keyboard = keyboard[1:20]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(u'Виды деревьев:', reply_markup=reply_markup)


def create_button(name):
    return InlineKeyboardButton(name.capitalize(), callback_data = name),


def on_press_button(update, context):
    query = update.callback_query

    myfile = open(u"trees/" + query.data + ".txt")
    msg = myfile.read()
    myfile.close()

    context.bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def get_files(update, context):
    msg = os.listdir('/home/ifmoadmin')
    update.message.reply_text(msg)


def model(update, context):
    update.message.reply_text(
                f'Текущая модель: {model_name}\n'+
                'Чтобы сменить модель, отправьте число:\n'+
                '1. K-Nearest Neighbors\n'+
                '2. Decision Tree\n' +
                '3. Gaussian Naive Bayes\n' +
                '4. Random Forest\n' +
                '5. C-Support Vector Classification\n')

def main():
    token = open("./t.txt", "r")
    t = token.readline()[:-1]
    print(t)
    token.close()
    updater = Updater(t, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help',my_help))
    updater.dispatcher.add_handler(CallbackQueryHandler(on_press_button))
    updater.dispatcher.add_handler(CommandHandler('get_files', get_files))
    updater.dispatcher.add_handler(CommandHandler('trees_list', trees_list))
    updater.dispatcher.add_handler(CommandHandler('model', model))
    updater.dispatcher.add_handler(MessageHandler(filters.Filters.photo, get_image))
    updater.dispatcher.add_handler(MessageHandler(filters.Filters.text, reply_text))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
