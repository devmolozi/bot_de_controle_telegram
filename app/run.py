import time
from telebot import types
import re
import asyncio
from telebot.async_telebot import AsyncTeleBot
from config import TOKEN_TELEGRAM, ID_ADMIN

bot = AsyncTeleBot(TOKEN_TELEGRAM)

advertencias = {}


@bot.message_handler(commands=['ajuda'])
async def ajuda(message):
	user_first_name = message.from_user.first_name
	
	text = f'<b>1% - AJUDA</b>\n\n'
	text += f'Olá {user_first_name}, fui Desenvolvido para te ajudar!\n\n'
	text += '× /ajuda\n'
	text += '× /id\n'
	text += '× /regras\n'
	#text += '× /insta\n'
	await bot.reply_to(message, text, parse_mode="HTML")


@bot.message_handler(commands=['regras'])
async def regras(message):
	regra = f'<b>1% - Regras</b>\n\n'
	regra += f'Regras para manter o Grupo em ordem.\n\n'
	regra += '× Evite mandar links (Sujeito a expulsão);\n'
	regra += '× Não aceitamos a falta de respeito no grupo;\n'
	regra += '× Evite iniciar conversas que não agregam valor;\n'
	regra += '× Evite flood de mensagens, seja objetivo.\n\n'
	regra += '× Qualquer dúvida marcar os Admins.\n\n'
	regra += '× Admins: @onepercenty & @Derick_Teixeira'
	await bot.reply_to(message, regra, parse_mode="HTML")


@bot.message_handler(commands=['id'])
async def my_id(message):
	user_id = message.from_user.id
	first_name = message.from_user.first_name
	text = f'Olá {first_name}, seu ID é → ```{user_id}``` ←'
	await bot.reply_to(message, text, parse_mode="Markdown")


"""# Comando /insta
@bot.message_handler(commands=['insta'])
def send_insta_link(message):

	keyboard = types.InlineKeyboardMarkup()

	instagram_button = types.InlineKeyboardButton("Siga-nos no Instagram", url="https://www.instagram.com/onepercenty/")
	keyboard.add(instagram_button)

	bot.send_message(message.chat.id, "Clique no botão abaixo para nos seguir no Instagram:", reply_markup=keyboard)
"""

lista_url = ['.com', '.cloud', '.xyz', '.pro', '.link', '.app', '.org', '.fun', '.br', '.net', '.edu', '.gov', '.mil', '.tech', '.int', '.eu', '.aero', '.museum', '.io', '.coop', '.gg', '.mobi', '.asia', '.name', '.pro', '.biz', '.info', '.xxx', '.tel', '.jobs', '.travel', '.mobi', '.cat', '.post', '.tel', '.museum', '.arpa', '.local']


@bot.message_handler(func=lambda message: any(keyword in message.text.lower() for keyword in lista_url))
async def delete_fun(message):
	chat_id = message.chat.id
	user_id = message.from_user.id
	first_name = message.from_user.first_name
	message_id = message.message_id
	user_name = message.from_user.username
	
	if user_id in ID_ADMIN:
		print(f'Admin @{user_name} enviando mensagem.')
	else:
		matched_keywords = [keyword for keyword in lista_url if keyword in message.text.lower()]
		
		advertencias.setdefault(user_id, 0)
		advertencias[user_id] += 1
		
		if advertencias[user_id] >= 3:
			await bot.reply_to(message, 'Você foi banido por enviar links após 3 advertências.')
			await bot.kick_chat_member(chat_id, user_id)
			advertencias[user_id] = 0
		else:
			perfil_link = f'<a href="https://t.me/{user_name}">{first_name}</a>'
			mensagem = (
				f'<b>{perfil_link}</b> - Você recebeu ({advertencias[user_id]}/3) Advertências. Evite mandar links!'
				f'\n\nLeia as Regras do Grupo para evitar ser punido.')
			await bot.reply_to(message, mensagem, parse_mode="HTML")
			await asyncio.sleep(1)
			await bot.delete_message(chat_id, message_id)


@bot.message_handler(func=lambda message: message.chat.type == 'group' or message.chat.type == 'supergroup')
async def handle_group_message(message):
	chat_id = message.chat.id
	user_id = message.from_user.id
	user_name = message.from_user.username
	first_name = message.from_user.first_name
	message_id = message.message_id
	
	if user_id in ID_ADMIN:
		print(f'Admin @{user_name} enviando mensagem.')
	else:
		
		if re.search(r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.text.lower()):
			advertencias.setdefault(user_id, 0)
			advertencias[user_id] += 1
			
			if advertencias[user_id] >= 3:
				await bot.reply_to(message, 'Você foi banido por enviar links após 3 advertências.')
				await bot.kick_chat_member(chat_id, user_id)
				advertencias[user_id] = 0
			else:
				perfil_link = f'<a href="https://t.me/{user_name}">{first_name}</a>'
				mensagem = (
					f'<b>{perfil_link}</b> - Você recebeu ({advertencias[user_id]}/3) Advertências. Evite mandar links!'
					f'\n\nLeia as Regras do Grupo para evitar ser punido.')
				await bot.reply_to(message, mensagem, parse_mode="HTML")
				time.sleep(1)
				await bot.delete_message(chat_id, message_id)


print("ONLINE CHEF")

asyncio.run(bot.polling())
