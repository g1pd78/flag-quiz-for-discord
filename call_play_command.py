# -*- coding: utf-8 -*-
import json #load countries indexes
import requests #requests whatever
from random import randint #4random
import shutil #2save pics localy
from os import remove#load just what i need
import discord

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

async def refresh_and_send_image(im, message):#refreshing info
	im.index = indexs[randint(0, countries_count - 1)]
	im.answer = countries[im.index]
	load_Image('https://flagcdn.com/w640/' + im.index + '.png')
	im.is_answered = False
	im.count_of_wrong_answers = 4

	print(im.answer) ###############################################


	return await message.channel.send(file=discord.File('img.png')), remove_Image()
	
async def print_variants(message, answer):#rename
	variant_list = []
	variant_list.append(answer)
	variants_count = 1
	while variants_count != 4:
		current_variant = countries[indexs[randint(0, countries_count - 1)]]
		if current_variant not in variant_list:
			variant_list.append(current_variant)
			variants_count += 1
	
	for i in range(4):
		print_cur_var = discord.Embed(color = discord.Colour.random(), description = variant_list[i])
		await message.channel.send(embed = print_cur_var)






print('play module ready!')