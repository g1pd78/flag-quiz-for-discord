# -*- coding: utf-8 -*-
import json #load countries indexes
import requests #requests whatever
from random import randint #4random    $default python module
from shutil import copyfileobj #2save pics localy $ default python module
from os import remove#load just what i need    $ default python module
import discord
import asyncio #$default python module
from  database_module import *




response = requests.get("https://flagcdn.com/en/codes.json")
countries = json.loads(response.text)
indexs = list(countries.keys())
countries_count = len(indexs)




show_variants = {}
images = {}

class image(object):

	def __init__(self, index, answer, count_of_wrong_answers):
		self.index = index
		self.answer = answer
		self.count_of_wrong_answers = count_of_wrong_answers


#im = image('', '', 0)

def init_variant_and_img_prm(guild):
	show_variants[guild] = False
	images[guild] = image('', '', 0)

async def change_var_param(message, guild):
	global show_variants
	msg = message.content.split(' ')
	if len(msg) >= 2:
		if msg[1].upper() == 'ON':
			show_variants[guild] = True

			await message.add_reaction('✅')
		elif msg[1].upper() == 'OFF':
			show_variants[guild] = False
			await message.add_reaction('✅')
		else:
			await message.add_reaction('❌')






def load_Image(url):

	response = requests.get(url, stream=True)
	with open('img.png', 'wb') as out_file:
		copyfileobj(response.raw, out_file)
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
	guild = message.guild.id
	images[guild].index = indexs[randint(0, countries_count - 1)]
	images[guild].answer = countries[images[guild].index]
	load_Image('https://flagcdn.com/w640/' + images[guild].index + '.png')
	images[guild].is_answered = False
	images[guild].count_of_wrong_answers = 4

	print(images[guild].answer) ###############################################


	msg = await message.channel.send(file=discord.File('img.png'))

	remove_Image()
	
	'''
async def reaction_check(client):
	def check(reaction, user):
		print('asd')
		return str(reaction.emoji) == '✅'

	try: 	
		reaction, user = await client.wait_for('reaction_add', check = check, timeout=60.0)
	except asyncio.TimeoutError:
		print('nah')
		'''
#msg_id = []###################################################################
async def print_variants(message):

	#global msg_id

	#global show_variants
	variant_list = []
	variant_list.append(images[message.guild.id].answer)
	variants_count = 1
	while variants_count != 4:
		current_variant = countries[indexs[randint(0, countries_count - 1)]]
		if current_variant not in variant_list:
			variant_list.append(current_variant)
			variants_count += 1
	
	for i in range(4):
		print_cur_var = discord.Embed(color = discord.Colour.random(), description = variant_list[i])
		msg = await message.channel.send(embed = print_cur_var)
		#msg_id.append(msg.id)
	#print(msg_id)
		#await reaction_check(client)
		



async def play_command(message, client, guild):
	#global show_variants
	count = count_calculation(message.content.split(' '))
	game_status = True

	while count:
		#reaction = await self.wait_for('reaction')
		#print(reaction)
		await refresh_and_send_image(message)#reload image information and send it/ then remove


		if show_variants[guild]:
			await print_variants(message)


		def check(mes: discord.Message):
			return message.channel == mes.channel and mes.author.id != client.user.id

		while images[guild].count_of_wrong_answers:


			try:
				guess = await client.wait_for('message', check = check)#, timeout = 10.0)
				print(guess.author)
				#чтобы не отвечал на вэйтфоры сам себе


				if guess.content.startswith('/help') or guess.content.startswith('/play'):
					await message.channel.send('Sorry, your shoulda finnish game at first!')
				else:



					#print(guess)
					if guess and guess.content == images[guild].answer:
						await message.channel.send('Yup')
						images[guild].count_of_wrong_answers = 0#to end game
						point_calculation(str(guess.author), show_variants[guild], True)
					else:
						await message.channel.send('Nope')
						point_calculation(str(guess.author), show_variants[guild], False)
						images[guild].count_of_wrong_answers -= 1
						if images[guild].count_of_wrong_answers == 0:
							await message.channel.send('Sorry, your attempts over! It was {}.'.format(im.answer))



					




			except asyncio.TimeoutError:
				images[guild].count_of_wrong_answers = 0
				await message.channel.send('Sorry, you took too long it was {}.'.format(images[guild].answer))

		count -= 1

		#tie
		if not count and await tie_checker(message):
			count += 1
			print('tie!')

	await game_finnished(message)



print('play module ready!')