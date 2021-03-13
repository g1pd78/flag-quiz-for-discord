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
answer = ""


bot = commands.Bot(command_prefix='/')





@bot.command(pass_context=True)
async def play(ctx):

	index = indexs[randint(0, countries_count - 1)]
	global answer
	global game_status 
	game_status = True
	answer = countries[index]
	load_Image('https://flagcdn.com/w640/' + index + '.png')
	await ctx.send(file=discord.File('img.png'))
	remove_Image()

	print(answer) ###############################################



@bot.event
async def on_message(message):
	if message.author.id == bot.user.id: #he shouldn reply himself
		return

	global game_status #make it global 2 make it usable in async
	global answer

	if message.content == '/play' and game_status:
		print('Trying to play 2gamez in one')
		return

	print(bot)
	print(message.author)
	print(answer)

	if game_status:
		if message.content == answer:
			await message.channel.send("Yup")
			game_status = False
		else:
			await message.channel.send("Nope")


	await bot.process_commands(message)


	
bot.run(TOKEN)


