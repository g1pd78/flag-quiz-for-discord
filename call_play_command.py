# -*- coding: utf-8 -*-
import json #load countries indexes
import requests #requests whatever
from random import randint #4random
import shutil #2save pics localy
from os import remove#load just what i need
import discord
import asyncio
from  database_module import *



response = requests.get("https://flagcdn.com/en/codes.json")
countries = json.loads(response.text)
indexs = list(countries.keys())
countries_count = len(indexs)


class image(object):

	def __init__(self, index, answer, count_of_wrong_answers):
		self.index = index
		self.answer = answer
		self.count_of_wrong_answers = count_of_wrong_answers

im = image('', '', 0)



def load_Image(url):

	response = requests.get(url, stream=True)
	with open('img.png', 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	del response


def remove_Image():
	remove('img.png')


def count_calculation(msg: list) -> int:
	count = 0

	if len(msg) > 1:
		param = msg[1]

		if param == 'short':
				count = 5
		elif param == 'long':
			count = 10
		elif param == 'custom':
			if len(msg) > 2:
				param_custom = msg[2]
				if param_custom.isdigit():
					count = int(param_custom)
				else:
					print('Ne chislo')
			else:
				print('gde parametr')
		else:
			print('net takih')
	else:
		count = 5


	return count

async def refresh_and_send_image(message):#refreshing info
	im.index = indexs[randint(0, countries_count - 1)]
	im.answer = countries[im.index]
	load_Image('https://flagcdn.com/w640/' + im.index + '.png')
	im.is_answered = False
	im.count_of_wrong_answers = 4

	print(im.answer) ###############################################


	return await message.channel.send(file=discord.File('img.png')), remove_Image()
	
async def print_variants(message):#rename
	variant_list = []
	variant_list.append(im.answer)
	variants_count = 1
	while variants_count != 4:
		current_variant = countries[indexs[randint(0, countries_count - 1)]]
		if current_variant not in variant_list:
			variant_list.append(current_variant)
			variants_count += 1
	
	for i in range(4):
		print_cur_var = discord.Embed(color = discord.Colour.random(), description = variant_list[i])
		await message.channel.send(embed = print_cur_var)



async def play_command(message, show_variants, client):
	count = count_calculation(message.content.split(' '))
	game_status = True
	while count:
		#reaction = await self.wait_for('reaction')
		#print(reaction)
		await refresh_and_send_image(message)#reload image information and send it/ then remove


		if show_variants:
			await print_variants(message)


		while im.count_of_wrong_answers:


			try:
				guess = await client.wait_for('message', check = lambda message: message.author.id != client.user.id, timeout = 10.0)
				#чтобы не отвечал на вэйтфоры сам себе


				if guess.content.startswith('/help') or guess.content.startswith('/play'):
					await message.channel.send('Sorry, your shoulda finnish game at first!')
				else:



					#print(guess)
					if guess and guess.content == im.answer:
						await message.channel.send('Yup')
						im.count_of_wrong_answers = 0#to end game
						point_calculation(str(message.author), show_variants)
					else:
						await message.channel.send('Nope')
						im.count_of_wrong_answers -= 1
						if im.count_of_wrong_answers == 0:
							await message.channel.send('Sorry, your attempts over! It was {}.'.format(im.answer))



					




			except asyncio.TimeoutError:
				im.count_of_wrong_answers = 0
				await message.channel.send('Sorry, you took too long it was {}.'.format(im.answer))
		count -= 1


print('play module ready!')