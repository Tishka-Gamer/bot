from config import *
from telebot import types


import index
from index import *




# @bot.message_handler(commands=['start'])
# def send_welcome(message):
# 	bot.reply_to(message, "Howdy, how are you doing?",)
#
#
# @bot.message_handler(commands=['help'])
# def send_welcome(message):
# 	bot.reply_to(message, "You need help?",)
#
#
# @bot.message_handler(commands=['да'])
# def send_welcome(message):
# 	bot.reply_to(message, "50 рублей и все будет",)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	user = message.from_user.id
	us = index.finduser(user, connect)
	if us is None:
		index.registr(user, connect)
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	itemNews = types.KeyboardButton('Новости')
	itemSub = types.KeyboardButton('Подписки')
	itemCate = types.KeyboardButton('Категории')
	markup.add(itemCate, itemNews, itemSub)
	connect.commit()

	bot.reply_to(message, "Привет, чем помочь?", reply_markup=markup)

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
# 	user = message.from_user.id
# 	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
# 	itemNews = types.KeyboardButton('Новости✉️')
# 	itemSub = types.KeyboardButton('Подписки📱')
# 	itemCate = types.KeyboardButton('Категории📁')
#
# 	markup.add(itemCate, itemNews, itemSub)
# 	bot.reply_to(message, "Привет, чем помочь?", reply_markup = markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		commands = call.data.split(";")
		# print(commands)
		mess = commands[1]
		cail = commands[0]
		print(cail)
		# print(mess)
		user = finduser(call.from_user.id, connect)
		if call.message:
			if cail == 'good':
				print(user)
				id = index.findcat(mess, connect)
				us = index.findcatus(user[0], id[0], connect)

				if us is None:
					index.subcat(user[0], id[0], connect)
					bot.send_message(call.message.chat.id, 'Вы подписались')
					connect.commit()
				else:
					bot.send_message(call.message.chat.id, 'Вы уже подписаны')
			elif cail == "bad":
				id = index.findcat(mess, connect)
				us = index.findcatus(user[0], id[0], connect)
				if us is None:
					bot.send_message(call.message.chat.id, 'Вы не подписались')
				else:
					index.unsubcat(user[0], id[0], connect)
					bot.send_message(call.message.chat.id, 'Вы отписаны')
					connect.commit()
	except Exception as e:
		print(repr(e))

@bot.message_handler(content_types=['text'])
def bot_message(message):
	if message.chat.type == 'private':
		if message.text == 'Новости':
			user = message.from_user.id
			user_id = finduser(user, connect)
			us = index.seecub(user_id[0], connect)
			if us is None:
				bot.reply_to(message, "сначала подпишитесь")
			else:
				for i in us:
					top_headlines = newsapi.get_top_headlines(language='ru', category=str(i[1]), page_size=2, page=1)
					print(str(i[1]))
					# all_articles = newsapi.get_everything(from_param='2023-09-07',
					# 									  to='2023-09-08',
					# 									  category=str(i[1]),
					# 									  language='jp',
					# 									  page_size=2,
					# 									  page=1)
					print(top_headlines.values())
					bot.reply_to(message, f" {top_headlines['articles'][0]['title']} \n {top_headlines['articles'][0]['url']}")
					# /v2/top-headlines/sources
					sources = newsapi.get_sources()
			# markup2 = types.InlineKeyboardMarkup(row_width=1)
			# item1 = types.InlineKeyboardButton("Свежие новости???", callback_data='good')
			# item2 = types.InlineKeyboardButton("Вчерашние???", callback_data='bad')
			# markup2.add(item1, item2)
			# bot.reply_to(message, "Привет, чем помочь?", reply_markup=markup2)
		if message.text == 'Подписки':
			user = message.from_user.id
			user_id = finduser(user, connect)
			us = index.seecub(user_id[0], connect)
			markup2 = types.InlineKeyboardMarkup(row_width=2)
			if us is None:
				bot.reply_to(message, "сначала подпишитесь")
			else:
				for i in us:
					item1 = types.InlineKeyboardButton(str(i[1]), callback_data=f'bad;{str(i[1])}')
					markup2.add(item1)
				bot.reply_to(message, "Ваши подписки. При нажатии вы отписываетесь.", reply_markup=markup2)
				connect.commit()
		if message.text == 'Категории':
			alcat = catg(connect)
			markup2 = types.InlineKeyboardMarkup(row_width=2)
			for i in alcat:
				item1 = types.InlineKeyboardButton(str(i[1]), callback_data=f'good;{str(i[1])}')
				# item1 = types.InlineKeyboardButton("Подписаться???", callback_data=f'good;{str(i[1])}' )
				# item2 = types.InlineKeyboardButton("Отписаться???", callback_data=f'bad;{str(i[1])}')
				markup2.add(item1)
			bot.reply_to(message, "Категории. При нажатии вы подписываетесь", reply_markup=markup2)


bot.infinity_polling(none_stop = True)


