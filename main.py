# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as BS #for parsing/ dunno 4wat i use it here

import discord #for my bot
from discord.ext import commands

import json #load countries indexes
import requests #requests whatever
import shutil #2save pics localy
from random import randint #4random

from os import remove#load just what i need

import sqlite3 #4sqlite

TOKEN = ''

response = requests.get("https://flagcdn.com/en/codes.json")
countries = json.loads(response.text)
indexs = list(countries.keys())
countries_count = len(indexs)
game_status = False
count = 0



def load_Image(url):

	response = requests.get(url, stream=True)
	with open('img.png', 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	del response

def remove_Image():
	remove('img.png')






bot = commands.Bot(command_prefix = '/', help_command = None)

@bot.command(pass_context = True)
async def help(ctx, *args):
	st = discord.Embed(title = 'Можем сыграть',
	 description = 
	 '''
	 	Присутствуют следующие режимчики:

	 	1)квиз на 5 вопросиков - short
	 	2)квиз на 10 вопросиков - long
	 	3)квиз на желаемое число вопросов - custom
	 	Запускаемся, значится, командой - /play %вариант игры%

	 	На вопросик дается 5 попыточек
	 ''',
	 color = 0xFF5733)
	await ctx.send(embed=st)

@bot.command(pass_context=True)
async def play(ctx, prm, *args):

	global game_status 
	global count
	#param = int(prm)

	#print(args)
	###################### 4 testing made it 1

	if prm == 'short':
		count = 1
		game_status = True
	elif prm == 'long':
		count == 10
		game_status = True
	elif prm == 'custom':
		count = int(args[0])
		game_status = True
	else:
		await ctx.send('You shoulda read /help info first!')




#make class for easier usage 
class image(object):

	def __init__(self, index, answer, is_answered, count_of_wrong_answers):
		self.index = index
		self.answer = answer
		self.is_answered = is_answered
		self.count_of_wrong_answers = count_of_wrong_answers

im = image('a', 'a', True, 0)
players_list = {}



@bot.event
async def on_message(message):

	
	if message.author.id == bot.user.id: #he shouldn reply himself
		return

	global game_status #make it global 2 make it usable in async
	global count
	global players_list

	if message.content == '/play' and game_status:#/play control
		await message.channel.send('Nah, you are already playing!')
		return

	if message.content == '/help' and game_status:#/help control
		await message.channel.send('If you figured how to start - you can finish a game first, just try to answer!')
		return

	await bot.process_commands(message)#after exeptions


	def game():#refreshing info
		im.index = indexs[randint(0, countries_count - 1)]
		im.answer = countries[im.index]
		load_Image('https://flagcdn.com/w640/' + im.index + '.png')
		im.is_answered = False
		im.count_of_wrong_answers = 0
		

		print(im.answer) ###############################################


	'''
	print(bot)
	print(message.author)
	print(im.answer)
	print(game_status)
	print(count)
	print(im.is_answered)
	'''


	if game_status:

		if not im.is_answered:
			if message.content == im.answer:
				message_author = str(message.author)

				if message_author in players_list:
					players_list[message_author] += 1
				else:
					players_list.update({message_author:1})


				await message.channel.send("Yup, " + message_author.split('#')[0] + ', excelent!')
				im.is_answered = True
				count-=1
			else:
				await message.channel.send("Nope")
				im.count_of_wrong_answers += 1
				if im.count_of_wrong_answers == 5: #attempts border
					im.is_answered = True
					count -= 1
					await message.channel.send("Too many attempts for one question!")

		if im.is_answered and count:
			game()#reload image information
			await message.channel.send(file=discord.File('img.png'))
			remove_Image()

		if not count:
			players_list = dict(sorted(players_list.items(), key = lambda item: item[1], reverse = False))#sort by points
			await message.channel.send("Game Over!")

			players_list_keys = list(players_list.keys())
			players_list_values = list(players_list.values())

			if players_list_values[0] == players_list_values[1]:#check it with someone else or create another account //later
				await message.channel.send("It isnt the END! It is a tie! One more flag!")
				count += 1 
				game_status = True

			winner_mes = discord.Embed(color = 0xFF5733, description = players_list_keys[0].split('#')[0] + ' is a winner!')
			await message.channel.send(embed = winner_mes)#print a winner
			#write result into sql dbase
			connect = sqlite3.connect('players.sql')
			cur = connect.cursor()
			print(players_list_values[0])
			cur.execute("INSERT INTO players(id, score) values(:id, :score);", (players_list_keys + players_list_values))
			connect.commit()

			#i shoulda review tie variants ----- still player who isnt a potential winnner can answer!!!!!!!!!
			players_list.clear()#remove players from dict
		


	


	
bot.run(TOKEN)


#add exeptions like count < 0 and add sql or json table with players 
#create own table 4every chat or create prm with id of the chat
#insert into tbl1 values('hello!',10);



#lambda functions