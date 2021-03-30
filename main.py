# -*- coding: utf-8 -*-
from call_help_command import help_command
from call_play_command import *


import discord #for my bot



TOKEN = ''


#servers = {}
#servers[''] = {}
#game_statuses = {[]	, ''}
servers = {}








class myBot(discord.Client):
	
	#def __init__(self, show_variants, game_status):


	async def on_ready(self):
		print('Bot ready!')
	

	


	async def on_message(self, message):
		if message.author.id == self.user.id: #he shouldn reply himself
			return

		#here i can place my commands / shoulda check em with /stratswith()

		global servers




		guild = message.guild.id
		if not guild in servers:
			servers[guild] = ''
			init_variant_and_img_prm(guild)

		
		if message.content.startswith('/help') and not servers[guild]:
			await help_command(message)
			#help.py file


		if message.content.startswith('/variants') and not servers[guild]:
			await change_var_param(message, guild)



		if message.content.startswith('/score') and not servers[guild]:
			await show_score(message)


		if message.content.startswith('/play') and not servers[guild]:
			servers[guild] = True
			await play_command(message, self, guild)
			await message.channel.send("Game Over!")
			servers[guild] = False


#ответы привязать к сервер айди

'''
	async def on_reaction_add(client, mes, author):
		#print(client.asd)
		check_reaction(mes.message.id)
		#print(mes.message.id)
		#print(author.asdasd)
		#print(author.name)
		#print(author)
		#print(m.emoji)
'''


		#!!!!!!!!!!!!!!!!!!!!!!!!!!

bot = myBot()
bot.run(TOKEN)

#доделать /варианты и ничью, а потом к реакциям!
#is_system()
#/top
