# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as BS #for parsing/ dunno 4wat i use it here

import discord #for my bot
from discord.ext import commands

import json #load countries indexes
import requests #requests whatever
import shutil #2save pics localy
from random import randint #4random
import asyncio
from os import remove#load just what i need
import sqlite3 #4sqlite

TOKEN = 'ODIxMzM2OTcyODIzODg3ODcz.YFCPqg.mq1BfL4pGYhJC3NsO4pBYnsgPSA'

response = requests.get("https://flagcdn.com/en/codes.json")
countries = json.loads(response.text)
indexs = list(countries.keys())
countries_count = len(indexs)

def load_Image(url):

	response = requests.get(url, stream=True)
	with open('img.png', 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	del response

def remove_Image():
	remove('img.png')

#make class for easier usage 
class image(object):

	def __init__(self, index, answer, is_answered, count_of_wrong_answers):
		self.index = index
		self.answer = answer
		self.is_answered = is_answered
		self.count_of_wrong_answers = count_of_wrong_answers

im = image('a', 'a', True, 0)

show_variants = False
game_status = False
players_list = {}







class myBot(discord.Client):
	async def on_ready(self):
		print('im ready!')
	

	


	async def on_message(self, message):
		if message.author.id == self.user.id: #he shouldn reply himself
			return

		#here i can place my commands / shoulda check em with /stratswith()
		ctx = message.content

		global game_status
		global players_list


		'''
		#dunno shoulda i use it if i check this in guess part
		if ctx.startswith('/help') or ctx.startswith('/play') and game_status:
			print('chicha')
			return'''

		if message.content.startswith('/help') and not game_status:
			st = discord.Embed(title = 'Можем сыграть',
	 		description = 
	 		'''
	 		Присутствуют следующие режимчики:

	 		1)квиз на 5 вопросиков - short - Default
	 		2)квиз на 10 вопросиков - long
	 		3)квиз на желаемое число вопросов - custom %желаемое количество вопросов%
	 		Запускаемся, значится, командой - /play 

	 		!Включить варианты - /variants ON 
	 		!Выключить варианты - /variants OFF
	 		!Default = False

	 		>За правильный ответ в игре без вариантов дается 3 балла
	 		>За правильный ответ в игре с вариантами дается 1 балл
	 		>За неправильный ответ в игре с вариантами забирается 2 балла


	 		Обкашлять вопросик дается 5 попыточек и 10 секунд
	 		''',
	 		color = 0xFF5733)
			await message.channel.send(embed=st)





		if message.content.startswith('/play') and not game_status:

			
			count = 0
			if len(message.content.split(' ')) > 1:
				param = message.content.split(' ')[1]

				if param == 'short':
					count = 5
				elif param == 'long':
					count = 10
				elif param == 'custom':
					if len(message.content.split(' ')) > 2:
						param_custom = message.content.split(' ')[1]
						if param_custom.isdigit():
							count = int(param)
						else:
							print('Ne chislo')
					else:
						print('gde parametr')
			else:
				count = 5
			
			game_status = True

			def game():#refreshing info
				im.index = indexs[randint(0, countries_count - 1)]
				im.answer = countries[im.index]
				load_Image('https://flagcdn.com/w640/' + im.index + '.png')
				im.is_answered = False
				im.count_of_wrong_answers = 4

				print(im.answer) ###############################################
				
			def print_variants():#rename
				variant_list = []
				variant_list.append(im.answer)
				variants_count = 1
				while variants_count != 4:
					current_variant = countries[indexs[randint(0, countries_count - 1)]]
					if current_variant not in variant_list:
						variant_list.append(current_variant)
						variants_count += 1
				
				return variant_list

			message_author = str(message.author)
			points_per_question = 1 if show_variants else 3#points depends by variants


			while count:
				#reaction = await self.wait_for('reaction')
				#print(reaction)

				game()#reload image information
				await message.channel.send(file=discord.File('img.png'))
				remove_Image()

				if show_variants:
					variant_list = print_variants()
					for i in range(4):
						print_cur_var = discord.Embed(color = discord.Colour.random(), description = variant_list[i])
						await message.channel.send(embed = print_cur_var)

				while im.count_of_wrong_answers:


					try:
						guess = await self.wait_for('message', check = lambda message: message.author.id != self.user.id, timeout = 10.0)
						#чтобы не отвечал на вэйтфоры сам себе


						if guess.content.startswith('/help') or guess.content.startswith('/play'):
							await message.channel.send('Sorry, your shoulda finnish game at first!')
						else:



							print(guess)
							if guess and guess.content == im.answer:
								await message.channel.send('Yup')
								im.count_of_wrong_answers = 0#to end game
								if message_author in players_list:
									players_list[message_author] += points_per_question
								else:
									players_list.update({message_author:points_per_question})

							else:
								await message.channel.send('Nope')
								im.count_of_wrong_answers -= 1
								if im.count_of_wrong_answers == 0:
									await message.channel.send('Sorry, your attempts over! It was {}.'.format(im.answer))



							




					except asyncio.TimeoutError:
						im.count_of_wrong_answers = 0
						await message.channel.send('Sorry, you took too long it was {}.'.format(im.answer))



					

				count -= 1


			players_list = dict(sorted(players_list.items(), key = lambda item: item[1], reverse = False))#sort by points
			await message.channel.send("Game Over!")

			players_list_keys = list(players_list.keys())
			players_list_values = list(players_list.values())
			'''
				if players_list_values[0] == players_list_values[1]:#check it with someone else or create another account //later
					await message.channel.send("It isnt the END! It is a tie! One more flag!")
					count += 1 
					game_status = True
					return
				'''

			#print(players_list_values)
			if players_list_keys:
				winner_mes = discord.Embed(color = 0xFF5733, description = players_list_keys[0].split('#')[0] + ' is a winner!')
				await message.channel.send(embed = winner_mes)#print a winner
			#write result into sql dbase
				connect = sqlite3.connect('players.sql')
				cur = connect.cursor()
				#print(players_list_values[0])
				cur.execute("INSERT INTO players(id, score) values(:id, :score);", (players_list_keys + players_list_values))
				connect.commit()

			#i shoulda review tie variants ----- still player who isnt a potential winnner can answer!!!!!!!!!
				players_list.clear()#remove players from dict



			game_status = False

'''
	async def on_reaction_add(client, mes, author):
		print(author.id)
		#print(author.name)
		#print(author)
		#print(m.emoji)
		'''


		#!!!!!!!!!!!!!!!!!!!!!!!!!!

bot = myBot()
bot.run(TOKEN)