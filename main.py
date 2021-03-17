# -*- coding: utf-8 -*-
from call_help_command import help_command
from call_play_command import *


import discord #for my bot



TOKEN = ''



#make class for easier Image usage 



show_variants = True
game_status = False








class myBot(discord.Client):
	
	#def __init__(self, show_variants, game_status):


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

			await play_command(message, show_variants, self)

			await message.channel.send("Game Over!")
						await game_finnished(message)
			game_status = False

			
			'''
			#tie variant
				if players_list_values[0] == players_list_values[1]:#check it with someone else or create another account //later
					await message.channel.send("It isnt the END! It is a tie! One more flag!")
					count += 1 
					game_status = True
					return
				'''

			#print(players_list_values)



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