# -*- coding: utf-8 -*-
from call_help_command import help_command
from call_play_command import *
from database_module import *

import discord #for my bot
import asyncio


TOKEN = ''



#make class for easier Image usage 
class image(object):

	def __init__(self, index, answer, count_of_wrong_answers):
		self.index = index
		self.answer = answer
		self.count_of_wrong_answers = count_of_wrong_answers

im = image('', '', 0)

show_variants = True
game_status = False








class myBot(discord.Client):
	


	async def on_ready(self):
		print('Bot ready!')
	

	


	async def on_message(self, message):
		if message.author.id == self.user.id: #he shouldn reply himself
			return

		#here i can place my commands / shoulda check em with /stratswith()


		global game_status



		if message.content.startswith('/help') and not game_status:
			await help_command(message)
			#help.py file




		if message.content.startswith('/play') and not game_status:

			
			count = count_calculation(message.content.split(' '))
			game_status = True





			while count:
				#reaction = await self.wait_for('reaction')
				#print(reaction)

				await refresh_and_send_image(im, message)#reload image information and send it/ then remove


				if show_variants:
					await print_variants(message, im.answer)


				while im.count_of_wrong_answers:


					try:
						guess = await self.wait_for('message', check = lambda message: message.author.id != self.user.id, timeout = 10.0)
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

				#need just keys here

			
			await message.channel.send("Game Over!")

			
			'''
				if players_list_values[0] == players_list_values[1]:#check it with someone else or create another account //later
					await message.channel.send("It isnt the END! It is a tie! One more flag!")
					count += 1 
					game_status = True
					return
				'''

			#print(players_list_values)
			
			await game_finnished(message)
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