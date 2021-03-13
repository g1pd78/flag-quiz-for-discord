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

TOKEN = ''

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




game_status = False
count = 0

bot = commands.Bot(command_prefix='/')




@bot.command(pass_context=True)
async def play(ctx, prm):

	global game_status 
	global count
	count = int(prm)
	game_status = True
	print('ya')




class image(object):

	def __init__(self, index, answer, is_answered):
		self.index = index
		self.answer = answer
		self.is_answered = is_answered

im = image('a', 'a', True)


async def send_im(ctx):
	await ctx.channel.send('asd')

@bot.event
async def on_message(message):

	
	if message.author.id == bot.user.id: #he shouldn reply himself
		return

	global game_status #make it global 2 make it usable in async
	global count

	if message.content == '/play' and game_status:
		print('Trying to play 2gamez in one')
		return

	await bot.process_commands(message)#after exeptions


	def game():
		im.index = indexs[randint(0, countries_count - 1)]
		im.answer = countries[im.index]
		load_Image('https://flagcdn.com/w640/' + im.index + '.png')
		im.is_answered = False
		
		

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
				await message.channel.send("Yup, " + str(message.author).split('#')[0])
				im.is_answered = True
				count-=1
			else:
				await message.channel.send("Nope")
		if(im.is_answered and count):
			game()
			await message.channel.send(file=discord.File('img.png'))
			remove_Image()
		if not count:
			await message.channel.send("Game Over")
		


	


	
bot.run(TOKEN)


